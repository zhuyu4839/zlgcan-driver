import os

from ctypes import *

from ..codes import *
from ..structs import *
from ..structs.linux.can import *
from ..types import *
from ..exceptions import ZCANException
from ..utils import _library_path, _library_run, _system_bit
from .zlgcan import _ZLGCAN

_LINUX_CAN = (ZCANDeviceType.ZCAN_USBCAN1, ZCANDeviceType.ZCAN_USBCAN2, )
_LINUX_CAN_4E_U = (ZCANDeviceType.ZCAN_USBCAN_4E_U, )
_LINUX_CAN_8E_U = (ZCANDeviceType.ZCAN_USBCAN_8E_U, )
_LINUX_CANFD = (ZCANDeviceType.ZCAN_USBCANFD_200U, ZCANDeviceType.ZCAN_USBCANFD_100U, ZCANDeviceType.ZCAN_USBCANFD_MINI)
_LINUX_CANFD_800U = (ZCANDeviceType.ZCAN_USBCANFD_800U, )
_LINUX_PCI_E = ()           # socketcan TODO


ON = c_int(1)
OFF = c_int(0)
CMD_CAN_FILTER = 0x14
CMD_CAN_SKD_SEND = 0x16
CMD_CAN_SKD_SEND_STATUS = 0x17
CMD_CAN_RES = 0x18
CMD_CAN_TIMEOUT = 0x44


class _ZCANLinux(_ZLGCAN):

    def __init__(self, dev_index: int, dev_type: int, resend: bool, derive: bool = False, **kwargs):
        super().__init__(dev_index, dev_type, resend, derive, **kwargs)
        if _system_bit != "64bit":
            raise ZCANException(
                        "The ZLG-CAN driver could not be loaded. "
                        "Check that you are using 64bit Python on Linux."
                    )

        if self._dev_type in _LINUX_CAN:
            self._library = cdll.LoadLibrary(os.path.join(_library_path, 'linux/x86_64/libusbcan.so'))
        elif self._dev_type in _LINUX_CAN_4E_U:
            self._library = cdll.LoadLibrary(os.path.join(_library_path, 'linux/x86_64/libusbcan-4e.so'))
        elif self._dev_type in _LINUX_CAN_8E_U:
            self._library = cdll.LoadLibrary(os.path.join(_library_path, 'linux/x86_64/libusbcan-8e.so'))
        elif self._dev_type in _LINUX_CANFD:
            self._library = cdll.LoadLibrary(os.path.join(_library_path, 'linux/x86_64/libusbcanfd.so'))
        elif self._dev_type in _LINUX_CANFD_800U:
            self._library = cdll.LoadLibrary(os.path.join(_library_path, 'linux/x86_64/libusbcanfd800u.so'))
        else:
            raise ZCANException(f"device type: {self._dev_type} is not supported by this system!")

    def _get_can_init_config(self, mode, filter, **kwargs):
        config = ZCAN_CHANNEL_INIT_CONFIG_Union()
        if self._dev_is_canfd:
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
                   or arb_tseg1 is not None \
                   or arb_tseg2 is not None \
                   or arb_sjw is not None \
                   or arb_smp is not None \
                   or arb_brp is not None
            config.canfd.mode = mode
            config.canfd.clock = clock
            config.canfd.aset.tseg1 = arb_tseg1
            config.canfd.aset.tseg2 = arb_tseg2
            config.canfd.aset.sjw = arb_sjw
            config.canfd.aset.smp = arb_smp
            config.canfd.aset.brp = arb_brp
            config.canfd.dset.tseg1 = data_tseg1
            config.canfd.dset.tseg2 = data_tseg2
            config.canfd.dset.sjw = data_sjw
            config.canfd.dset.smp = data_smp
            config.canfd.dset.brp = data_brp
            return config
        else:
            timing0 = kwargs.get("timing0", None)
            timing1 = kwargs.get("timing1", None)
            assert timing0 is not None \
                   or timing1 is not None
            config.can.acc_code = kwargs.get("acc_code", 0)
            config.can.acc_mask = kwargs.get('acc_mask', 0xFFFFFFFF)
            config.can.reserved = 0
            config.can.filter = kwargs.get("filter", 0)
            config.can.timing0 = timing0
            config.can.timing1 = timing1
            config.can.mode = mode
            return config

    def ResistanceStatus(self, channel, status=None):
        if self._dev_type in ZCAN_RESISTANCE_NOT_SUPPORT:
            return

        channel = self._get_channel_handler('CAN', channel)
        if status is not None:
            self._SetReference(channel, CMD_CAN_RES, byref(c_int(status)))
        return self._GetReference(channel, CMD_CAN_RES)

    # EXTERN_C U32 ZCAN_API VCI_SetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def _SetReference(self, channel, ref_code, data):
        _library_run(self._library, 'VCI_SetReference',
                     self._dev_type, self._dev_index, channel, ref_code, data)

    # EXTERN_C U32 ZCAN_API VCI_GetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def _GetReference(self, channel, ref_code):
        if self._dev_type in [ZCANDeviceType.ZCAN_CANETUDP, ZCANDeviceType.ZCAN_CANETE, ZCANDeviceType.ZCAN_CANETTCP,
                              ZCANDeviceType.ZCAN_CANDTU_NET, ZCANDeviceType.ZCAN_CANDTU_NET_400]:
            result = c_int()
            _library_run(self._library, 'VCI_GetReference',
                         self._dev_type, self._dev_index, channel, ref_code, cast(byref(result), c_void_p))
            return result

    def Debug(self, level):
        _library_run(self._library, 'VCI_Debug', level)

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
        _library_run(self._library, 'VCI_SetReference', self._dev_index, channel, CMD_CAN_FILTER, byref(_filter))

    # EXTERN_C U32 ZCAN_API VCI_OpenDevice(U32 Type, U32 Card, U32 Reserved);
    def OpenDevice(self, reserved=0):
        self._dev_handler = _library_run(self._library, 'VCI_OpenDevice', self._dev_type, self._dev_index, reserved)
        if not self._dev_derive:
            try:
                self._dev_info = self.GetDeviceInf()
                self._channels = tuple(i for i in range(self._dev_info.can_num))
                self._dev_is_canfd = 'CANFD' in self._dev_info.hw_type
            except ZCANException:
                raise ZCANException("can't get device info, consider set derive as True")
        else:
            self._channels = tuple(i for i in range(self.kwargs.get("channels", 1)))
            self._dev_is_canfd = self.kwargs.get("canfd", False)

    # EXTERN_C U32 ZCAN_API VCI_CloseDevice(U32 Type, U32 Card);
    def CloseDevice(self):
        can_channels = self._channel_handlers['CAN']
        lin_channels = self._channel_handlers['LIN']
        if not self._dev_derive:
            for channel, _ in can_channels.items():
                try:
                    self.ResetCAN(channel)
                except ZCANException as e:
                    self._logger.warning(e)
                    # raise ZCANException("can't reset can channel, consider set derive as True")
        # for channel in lin_channels:      # TODO for LIN
        #     self.ResetLIN(channel)
        _library_run(self._library, 'VCI_CloseDevice', self._dev_type, self._dev_index)
        can_channels.clear()
        lin_channels.clear()

    # EXTERN_C U32 ZCAN_API VCI_ReadBoardInfo(U32 Type, U32 Card, ZCAN_DEV_INF *pInfo);
    def GetDeviceInf(self) -> ZCAN_DEVICE_INFO:
        dev_info = ZCAN_DEVICE_INFO()
        _library_run(self._library, 'VCI_ReadBoardInfo',
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
        if "bitrate" not in kwargs:
            raise ZCANException("'bitrate' is required in config")

        _arb_cfg = self._baudrate_config[self._dev_type]['bitrate'].get(kwargs.get('bitrate'))
        if not _arb_cfg:
            raise ZCANException(f"buadrate: {kwargs.get('bitrate')} not configured in file(baudrate.conf.yaml)")

        _data_cfg = {}
        if self._dev_is_canfd:
            _data_cfg = (self._baudrate_config[self._dev_type].get("data_bitrate") or {}).get(kwargs.get('data_bitrate'), {})

        config = self._get_can_init_config(mode, filter, **_arb_cfg, **_data_cfg)
        _library_run(self._library, 'VCI_InitCAN', self._dev_type, self._dev_index, channel, byref(config))

        self._channel_handlers['CAN'][channel] = channel
        self.ResistanceStatus(channel, kwargs.get('initenal_resistance', 1))

    # EXTERN_C U32 ZCAN_API VCI_StartCAN(U32 Type, U32 Card, U32 Port);
    def StartCAN(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'VCI_StartCAN', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ResetCAN(U32 Type, U32 Card, U32 Port);
    def ResetCAN(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'VCI_ResetCAN', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ClearBuffer(U32 Type, U32 Card, U32 Port);
    def ClearBuffer(self, channel):
        channel = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'VCI_ClearBuffer', self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_ReadErrInfo(U32 Type, U32 Card, U32 Port, ZCAN_ERR_MSG *pErr);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        channel = self._get_channel_handler(chl_type, channel)
        error_frame = ZCAN_CHANNEL_ERR_INFO()
        ret = self._library.VCI_ReadErrInfo(self._dev_type, self._dev_index, channel, byref(error_frame))
        if ret:
            return error_frame

    # EXTERN_C U32 ZCAN_API VCI_ReadCANStatus(U32 Type, U32 Card, U32 Port, ZCAN_STAT *pStat);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        channel = self._get_channel_handler(chl_type, channel)
        status_info = ZCAN_CHANNEL_STATUS()
        _library_run(self._library, 'VCI_ReadCANStatus',
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
        return self._library.VCI_GetReceiveNum(self._dev_type, self._dev_index, channel)

    # EXTERN_C U32 ZCAN_API VCI_TransmitFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count);
    def TransmitFD(self, channel, msgs, size=None):
        channel = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = self._library.VCI_TransmitFD(self._dev_type, self._dev_index, channel, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCAN_CANFD_FRAME expect: {_size}, actual: {ret}')
        return ret

    # EXTERN_C U32 ZCAN_API VCI_ReceiveFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count, U32 Time);
    def ReceiveFD(self, channel, size=1, timeout=-1):
        channel = self._get_channel_handler('CAN', channel)
        if timeout is not None:
            timeout = int(timeout)
        can_msgs = (ZCAN_CANFD_FRAME * size)()
        ret = self._library.VCI_ReceiveFD(self._dev_type, self._dev_index, channel, byref(can_msgs), size, timeout)
        self._logger.debug(f'ZLG: Receive ZCAN_CANFD_FRAME expect: {size}, actual: {ret}')
        for i in range(ret):
            can_msg = can_msgs[i]
            can_msg.is_rx = True
            yield can_msg

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
        ret = self._library.VCI_Transmit(self._dev_type, self._dev_index, channel, byref(msgs), _size)
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
        if self._dev_type in ZUSBCAN_I_II_TYPE:
            can_msgs = (ZCAN_CAN_FRAME_I_II * size)()
        else:
            can_msgs = (ZCAN_CAN_FRAME * size)()
        ret = self._library.VCI_Receive(self._dev_type, self._dev_index, channel, byref(can_msgs), size, timeout)
        for i in range(ret):
            can_msg = can_msgs[i]
            can_msg.is_rx = True
            if self._dev_type in ZUSBCAN_I_II_TYPE:
                can_msg.channel = channel

            yield can_msg

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
        _library_run(self._library, 'VCI_SetReference',
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
            _library_run(self._library, 'VCI_SetReference',
                         self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND, byref(table))
            _library_run(self._library, 'VCI_SetReference',
                         self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND_STATUS,
                         byref(c_int(1)))       # TODO 不使用结构体行不行



