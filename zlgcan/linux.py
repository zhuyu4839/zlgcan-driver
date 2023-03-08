"""
by zhuyu4839@gmail.com
reference: https://manual.zlg.cn/web/#/188/6982
config: https://manual.zlg.cn/web/#/42/1710
"""
import os
import yaml

from ctypes import *
from ._common import _ZLGCAN, _library_check_run, ZCANDeviceType, ZCANCanMode, ZCANCanFilter, ZCANMessageType, ZCAN_DEVICE_INFO, ZCANException, \
    _arch, _curr_path

if _arch == '64bit':
    _lib_path = os.path.join(_curr_path, 'linux/x86_64/zlgcan/libusbcanfd.so')
else:
    _lib_path = None
if _lib_path:
    _library = cdll.LoadLibrary(_lib_path)

ON = c_int(1)
OFF = c_int(0)
CMD_CAN_FILTER = 0x14
CMD_CAN_SKD_SEND = 0x16
CMD_CAN_SKD_SEND_STATUS = 0x17
CMD_CAN_RES = 0x18
CMD_CAN_TIMEOUT = 0x44

try:
    with open(os.path.join(_curr_path, 'linux/baudrate.conf.yaml'), 'r', encoding='utf-8') as stream:
        _baudrate_config = yaml.full_load(stream)
except (FileNotFoundError, PermissionError, ValueError, yaml.YAMLError) as e:
    raise ZCANException(e)

class ZCANInitSet(Structure):
    _fields_ = [('tseg1', c_ubyte),
                ('tseg2', c_ubyte),
                ('sjw', c_ubyte),
                ('smp', c_ubyte),
                ('brp', c_ushort)]

class ZCAN_MSG_INFO(Structure):
    _pack_ = 1
    _fields_ = [('mode', c_uint, 4),  # 发送方式，0为正常模式，2为自发自收（仅用于自测）
                ('is_fd', c_uint, 4),  # 0-CAN帧，1-CANFD帧
                ('is_remote', c_uint, 1),  # 0-数据帧，1-远程帧
                ('is_extend', c_uint, 1),  # 0-标准帧，1-扩展帧
                ('is_error', c_uint, 1),  # 0-正常帧，1-错误帧
                ('bitrate_switch', c_uint, 1),  # 0-CANFD不加速，1-CANFD加速
                ('error_status', c_uint, 1),  # 错误状态，0-积极错误，1-消极错误
                ('pad', c_uint, 19)]

class ZCAN_MSG_HEADER(Structure):
    _fields_ = [('timestamp', c_uint),  # timestamp
                ('id', c_uint),  # can id
                ('info', ZCAN_MSG_INFO),  # msg info
                ('pad', c_ushort),  # reversed
                ('channel', c_ubyte),  # channel
                ('dlc', c_ubyte)]  # dlc

    def __repr__(self):
        return f'timestamp     : {self.timestamp} \n' \
               f'msg_id        : {"0x%04X" % self.id} \n' \
               f'mode          : {self.info.mode} \n' \
               f'is_fd         : {bool(self.info.is_fd)} \n' \
               f'is_remote     : {bool(self.info.is_remote)} \n' \
               f'is_extend     : {bool(self.info.is_extend)} \n' \
               f'is_error      : {bool(self.info.is_error)} \n' \
               f'bitrate_switch: {bool(self.info.bitrate_switch)} \n' \
               f'error_status  : {self.info.error_status} \n' \
               f'channel       : {self.channel} \n' \
               f'length        : {self.dlc} \n'

class ZCAN_FILTER(Structure):
    _fields_ = [('type', c_ubyte),  # /**< 0-std_frame, 1-ext_frame */
                ('pad', c_ubyte * 3),
                ('sid', c_uint),  # /**< start-id */
                ('eid', c_uint)]  # /**< end-id */

class ZCAN_FILTER_TABLE(Structure):
    _fields_ = [('size', c_uint),
                ('table', ZCAN_FILTER * 64)]

class ZCAN_CAN_FRAME(Structure):               # ZCAN_CAN_FRAME
    _fields_ = [('header', ZCAN_MSG_HEADER),
                ('data', c_ubyte * 8)]

    def __repr__(self):
        return str(self.header) + \
               'data          : ' + \
               ' '.join('%02X' % i for i in self.data)

class ZCAN_CANFD_FRAME(Structure):             # ZCAN_CANFD_FRAME
    _fields_ = [('header', ZCAN_MSG_HEADER),
                ('data', c_ubyte * 64)]

    def __repr__(self):
        return str(self.header) + \
               'data          : ' + \
               ' '.join('%02X' % self.data[i] for i in range(self.header.dlc))

class ZCAN_CHANNEL_ERR_INFO(Structure):           # ZCAN_CHANNEL_ERR_INFO
    _fields_ = [('header', ZCAN_MSG_HEADER),
                ('data', c_ubyte * 8)]

class ZCAN_CHANNEL_STATUS(Structure):         # ZCAN_CHANNEL_STATUS
    _fields_ = [('IR', c_ubyte),                    # /**< not used(for backward compatibility) */
                ('MOD', c_ubyte),                   # /**< not used */
                ('SR', c_ubyte),                    # /**< not used */
                ('ALC', c_ubyte),                   # /**< not used */
                ('ECC', c_ubyte),                   # /**< not used */
                ('EWL', c_ubyte),                   # /**< not used */
                ('RXE', c_ubyte),                   # /**< RX errors */
                ('TXE', c_ubyte),                   # /**< TX errors */
                ('PAD', c_uint)]

class ZCAN_TTX(Structure):
    _fields_ = [('interval', c_uint),             # 定时发送周期，单位百微秒
                ('repeat', c_ushort),               # 发送次数，0等于无线循环发
                ('index', c_ubyte),                 # 定时发送列表的帧索引号，也就是第几条定时发送报文
                ('flags', c_ubyte),                 # 0-此帧禁用定时发送，1-此帧使能定时发送
                ('msg', ZCAN_CANFD_FRAME)]

class ZCAN_TTX_TABLE(Structure):
    _fields_ = [('size', c_uint),
                ('table', ZCAN_TTX * 8)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):       # ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [('clock', c_uint),
                ('mode', c_uint),
                ('aset', ZCANInitSet),
                ('dset', ZCANInitSet)]

class _ZCANLinux(_ZLGCAN):

    def __init__(self, resend):
        if _library is None:
            raise ZCANException(
                        "The ZLG-CAN driver could not be loaded. "
                        "Check that you are using 64bit Python on Linux."
                    )
        super().__init__(resend)

    def _get_can_init_config(self, mode, filter, **kwargs):
        # print(mode, filter, kwargs)
        config = ZCAN_CHANNEL_INIT_CONFIG()
        clock = kwargs.get('clock', None)
        arb_tseg1 = kwargs.get('arb_tseg1', None)
        arb_tseg2 = kwargs.get('arb_tseg2', None)
        arb_sjw = kwargs.get('arb_sjw', None)
        arb_smp = kwargs.get('arb_smp', 0)
        arb_brp = kwargs.get('arb_brp', None)
        data_tseg1 = kwargs.get('data_tseg1', arb_tseg1)
        data_tseg2 = kwargs.get('data_tseg2', arb_tseg2)
        data_sjw = kwargs.get('data_sjw', arb_sjw)
        data_smp = kwargs.get('data_smp', arb_smp)
        data_brp = kwargs.get('data_brp', arb_brp)
        assert clock is not None \
            and arb_tseg1 is not None and arb_tseg2 is not None and arb_sjw is not None and arb_smp is not None \
            and arb_brp is not None
        config.mode = mode
        config.clock = clock
        config.aset.tseg1 = arb_tseg1
        config.aset.tseg2 = arb_tseg2
        config.aset.sjw = arb_sjw
        config.aset.smp = arb_smp
        config.aset.brp = arb_brp
        config.dset.tseg1 = data_tseg1
        config.dset.tseg2 = data_tseg2
        config.dset.sjw = data_sjw
        config.dset.smp = data_smp
        config.dset.brp = data_brp
        return config

    def ResistanceStatus(self, channel, status=None):
        channel = self._get_channel_handler('CAN', channel)
        if status is not None:
            self._SetReference(channel, CMD_CAN_RES, byref(c_int(status)))
        return self._GetReference(channel, CMD_CAN_RES)

    # EXTERN_C U32 ZCAN_API VCI_SetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def _SetReference(self, channel, ref_code, data):
        _library_check_run(_library, 'VCI_SetReference',
                           self._dev_type, self._dev_index, channel, ref_code, data)

    # EXTERN_C U32 ZCAN_API VCI_GetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def _GetReference(self, channel, ref_code):
        if self._dev_type in [ZCANDeviceType.ZCAN_CANETUDP, ZCANDeviceType.ZCAN_CANETE, ZCANDeviceType.ZCAN_CANETTCP,
                              ZCANDeviceType.ZCAN_CANDTU_NET, ZCANDeviceType.ZCAN_CANDTU_NET_400]:
            result = c_int()
            _library_check_run(_library, 'VCI_SetReference',
                               self._dev_type, self._dev_index, channel, ref_code, cast(byref(result), c_void_p))
            return result

    def Debug(self, level):
        _library_check_run(_library, 'VCI_Debug', level)

    def SetFilters(self, channel, filters=None):
        channel = self._get_channel_handler('CAN', channel)
        _filter = ZCAN_FILTER_TABLE()
        if filters is None:
            _filter.size = sizeof(ZCAN_FILTER) * 2
            _filter.table[0].type = 0
            _filter.table[0].sid = 0x0
            _filter.table[0].eid = 0xffffffff
            _filter.table[1].type = 1
            _filter.table[1].sid = 0x0
            _filter.table[1].eid = 0xffffffff
        else:
            if len(filters) > 64:
                filters = filters[:64]
            _filter.size = sizeof(ZCAN_FILTER) * len(filters)
            for index, item in enumerate(filters):
                mode = item[0]
                start = item[1]
                end = item[2]
                _filter.table[index].type = mode
                _filter.table[index].sid = start
                _filter.table[index].eid = end
        _library_check_run(_library, 'VCI_SetReference', self._dev_index, channel, CMD_CAN_FILTER, byref(_filter))

    # EXTERN_C U32 ZCAN_API VCI_OpenDevice(U32 Type, U32 Card, U32 Reserved);
    def OpenDevice(self, dev_type: ZCANDeviceType, dev_index=0, reserved=0):
        self._dev_handler = _library_check_run(_library, 'VCI_OpenDevice', dev_type, dev_index, reserved)
        self._dev_index = dev_index
        self._dev_type = dev_type
        # matched = re.findall(r'[.](\w*?),', inspect.getframeinfo(inspect.currentframe().f_back)[3][0])
        # assert len(matched) > 0
        # self._dev_type_name = matched[0]
        self._dev_info = self.GetDeviceInf()
        channels = self._dev_info.can_num
        self._channels = tuple(i for i in range(channels))
        self._dev_is_canfd = 'CANFD' in self._dev_info.hw_type

    # EXTERN_C U32 ZCAN_API VCI_CloseDevice(U32 Type, U32 Card);
    def CloseDevice(self):
        can_channels = self._channel_handlers['CAN']
        lin_channels = self._channel_handlers['LIN']
        for channel, _ in can_channels.items():
            self.ResetCAN(channel)
        # for channel in lin_channels:
        #     self.ResetLIN(channel)
        _library_check_run(_library, 'VCI_CloseDevice', self._dev_type, self._dev_index)
        can_channels.clear()
        lin_channels.clear()

    # EXTERN_C U32 ZCAN_API VCI_ReadBoardInfo(U32 Type, U32 Card, ZCAN_DEV_INF *pInfo);
    def GetDeviceInf(self) -> ZCAN_DEVICE_INFO:
        dev_info = ZCAN_DEVICE_INFO()
        _library_check_run(_library, 'VCI_ReadBoardInfo',
                           self._dev_type, self._dev_index, byref(dev_info))
        return dev_info

    # EXTERN_C U32 ZCAN_API VCI_InitCAN(U32 Type, U32 Card, U32 Port, ZCAN_INIT *pInit);
    def InitCAN(self, channel, mode: ZCANCanMode = ZCANCanMode.NORMAL,
                filter: ZCANCanFilter = ZCANCanFilter.DOUBLE,
                **kwargs):
        """
        初始化CAN(FD)通道
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param mode: CAN(FD)模式, 可选值0: 正常模式, 1: 只听(只读)模式, 默认0
| mode        | 通道工作模式         | 0 - 正常模式 <br/> 1 - 只听模式 |     |
        :param filter: CAN(FD)滤波方式, 可选值0: 双滤波, 1: 单滤波, 默认0
        :param kwargs: 其他关键字参数, 说明如下:
| 名称          | 功能             | 值说明                     | 默认值 | 备注            |
|-------------|----------------|-------------------------|-----|---------------|
| acc_code    | SJA1000的帧过滤验收码 | 推荐设置为0x0                |     |               |
| acc_mask    | SJA1000的帧过滤屏蔽码 | 推荐设置为0xffffffff         |     |               |
| filter      | 滤波方式           | 0 - 双滤波 <br/> 1 - 单滤波   | 0   |               |
| brp         | 滤波预分频因子        | 设置为0                    |     | 仅CANFD, 影响波特率 |
| abit_timing | ignored        | NA                      | NA  | 仅CANFD        |
| dbit_timing | ignored        | NA                      | NA  | 仅CANFD        |

        :return: None
        """
        # config = self._get_can_init_config(mode, filter, **kwargs)
        config = self._get_can_init_config(mode, filter, **_baudrate_config.get('bitrate').get(kwargs.get('bitrate')),
                                           **(_baudrate_config.get('data_bitrate') or {}).get(kwargs.get('data_bitrate'), {}))
        _library_check_run(_library, 'VCI_InitCAN', self._dev_type, self._dev_index, channel, byref(config))
        self._channel_handlers['CAN'][channel] = channel
        self.ResistanceStatus(channel, kwargs.get('initenal_resistance', 1))

    # EXTERN_C U32 ZCAN_API VCI_StartCAN(U32 Type, U32 Card, U32 Port);
    def StartCAN(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_check_run(_library, 'VCI_StartCAN', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ResetCAN(U32 Type, U32 Card, U32 Port);
    def ResetCAN(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_check_run(_library, 'VCI_ResetCAN', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ClearBuffer(U32 Type, U32 Card, U32 Port);
    def ClearBuffer(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_check_run(_library, 'VCI_ClearBuffer', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ReadErrInfo(U32 Type, U32 Card, U32 Port, ZCAN_ERR_MSG *pErr);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        channel = self._get_channel_handler(chl_type, channel)
        error_info = ZCAN_CHANNEL_ERR_INFO()
        ret = _library.VCI_ReadErrInfo(self._dev_type, self._dev_index, channel, byref(error_info))
        if ret:
            return error_info

    # EXTERN_C U32 ZCAN_API VCI_ReadCANStatus(U32 Type, U32 Card, U32 Port, ZCAN_STAT *pStat);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        channel = self._get_channel_handler(chl_type, channel)
        status_info = ZCAN_CHANNEL_STATUS()
        _library_check_run(_library, 'VCI_ReadCANStatus',
                           self._dev_type, self._dev_index, channel, byref(status_info))
        return status_info

    # EXTERN_C U32 ZCAN_API VCI_GetReceiveNum(U32 Type, U32 Card, U32 Port);
    def GetReceiveNum(self, channel, msg_type: ZCANMessageType = ZCANMessageType.CAN):
        """
        获取指定通道已经接收到消息数量
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msg_type: 消息类型: 0 - CAN; 1 - CANFD; '-1' - LIN
        :return: 消息数量
        """
        channel = self._get_channel_handler('CAN', channel)
        if msg_type == ZCANMessageType.CANFD:
            channel |= 0x80000000
        return _library.VCI_GetReceiveNum(self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_TransmitFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count);
    def TransmitFD(self, channel, msgs, size=None):
        channel = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = _library.VCI_TransmitFD(self._dev_type, self._dev_index, channel, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCAN_CANFD_FRAME expect: {_size}, actual: {ret}')
        return ret

    # EXTERN_C U32 ZCAN_API VCI_ReceiveFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count, U32 Time);
    def ReceiveFD(self, channel, size=1, timeout=-1):
        channel = self._get_channel_handler('CAN', channel)
        if timeout is not None:
            timeout = int(timeout)
        can_msgs = (ZCAN_CANFD_FRAME * size)()
        ret = _library.VCI_ReceiveFD(self._dev_type, self._dev_index, channel, byref(can_msgs), size, timeout)
        self._logger.debug(f'ZLG: Receive ZCAN_CANFD_FRAME expect: {size}, actual: {ret}')
        for i in range(ret):
            yield can_msgs[i]

    # EXTERN_C U32 ZCAN_API VCI_Transmit(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count);
    def Transmit(self, channel, msgs, size=None):
        """
        发送CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msgs: 消息报文
        :param size: 报文大小
        :return: 实际发送报文长度
        """
        channel = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = _library.VCI_Transmit(self._dev_type, self._dev_index, channel, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCAN_CAN_FRAME expect: {_size}, actual: {ret}')
        return ret

    # EXTERN_C U32 ZCAN_API VCI_Receive(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count, U32 Time);
    def Receive(self, channel, size=1, timeout=-1):
        """
        接收CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param size: 期待接收报文个数
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        channel = self._get_channel_handler('CAN', channel)
        if timeout is not None:
            timeout = int(timeout)
        can_msgs = (ZCAN_CAN_FRAME * size)()
        ret = _library.VCI_Receive(self._dev_type, self._dev_index, channel, byref(can_msgs), size, timeout)
        for i in range(ret):
            yield can_msgs[i]

    def TransmitInterval(self, channel, interval_msgs=None):
        """
        定时发送消息
        :param channel: 通道号, 从0开始
        :param interval_msgs: 周期消息, 以字典列表的形式传入, 最大长度8, 超过8的截取前8个
            Windows下:
                字典内容为:
                    enable: [可选, 默认值0] 0-此帧禁用定时发送, 1-此帧使能定时发送
                    index: [可选, 自动根据列表顺序编号]定时发送帧索引, 即第几条定时发送报文
                    interval: [可选, 默认值0] 发送间隔, 单位ms
                    trans_type: [可选, 默认值0] 0=正常发送, 1=单次发送, 2=自发自收, 3=单次自发自收
                    msg: [必须] ZCAN_CANFD_FRAME|ZCAN_CAN_FRAME
                    delay: [可选, 默认值None], 延迟发送时间, 单位ms
            Linux下:
                字典内容为:
                    enable: [可选, 默认值0] 0-此帧禁用定时发送, 1-此帧使能定时发送
                    index: [可选, 自动根据列表顺序编号]定时发送帧索引, 即第几条定时发送报文
                    interval: [可选, 默认值0] 发送间隔, 单位0.1ms
                    repeat: [可选, 默认值0] 发送次数, 0则表示无限次数
                    msg: [必须] ZCAN_CANFD_FRAME 报文内容
        :return: None
        """
        # TODO 清空自动发送列表(怎么做)
        channel = self._get_channel_handler('CAN', channel)
        _library_check_run(_library, 'VCI_SetReference',
                           self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND_STATUS,
                           byref(c_int(0)))           # TODO 不使用结构体行不行
        if interval_msgs:
            if len(interval_msgs) > 8:
                interval_msgs = interval_msgs[:8]
            table = ZCAN_TTX_TABLE()
            table.size = len(interval_msgs)
            for index, msg_dict in enumerate(interval_msgs):
                table.table[index].msg = msg_dict['msg']
                table.table[index].flags = msg_dict.get('enable', 0)
                table.table[index].index = msg_dict.get('index', index)
                table.table[index].interval = msg_dict.get('interval', 0)
                table.table[index].repeat = msg_dict.get('repeat', 0)
            _library_check_run(_library, 'VCI_SetReference',
                               self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND, byref(table))
            _library_check_run(_library, 'VCI_SetReference',
                               self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND_STATUS,
                               byref(c_int(1)))       # TODO 不使用结构体行不行



