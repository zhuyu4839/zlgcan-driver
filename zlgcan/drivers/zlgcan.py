import logging
import os.path

from ..types import *
from ..utils import ZCANException, _current_path


class _ZLGCAN(object):

    def __init__(self, dev_index: int, dev_type: int, resend: bool, derive: bool, **kwargs):
        """
        Create ZLG-CAN object
        :param resend: true if retry to send a frame until success else false
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._resend = resend
        self._dev_index = dev_index
        self._dev_type = dev_type
        self._dev_derive = derive
        self._dev_info = None
        self._dev_is_canfd = None
        self._channels = ()
        # {'CAN': {chl_obj: is_canfd}, 'LIN': {chl_obj: is_master}}
        self._channel_handlers = {'CAN': {}, 'LIN': {}}     # "CAN": {channel: channel_handler}
        self._dev_handler = None
        self._library = None
        self.kwargs = kwargs

        try:
            import yaml  # load baud-rate configuration file
            try:
                with open(os.path.join(_current_path, 'baudrate.conf.yaml'), 'r', encoding='utf-8') as stream:
                    self._baudrate_config = yaml.full_load(stream)
            except (FileNotFoundError, PermissionError, ValueError, yaml.YAMLError) as e:
                raise ZCANException(e)
        except ImportError:
            raise ZCANException("package 'pyyaml' required!")

    @property
    def device_index(self):
        return self._dev_index

    @property
    def device_type(self):
        return self._dev_type

    @property
    def device_is_canfd(self):
        return self._dev_is_canfd

    @property
    def channels(self) -> tuple:
        return self._channels

    @property
    def resend(self):
        return self._resend

    @property
    def device_info(self):
        return self._dev_info

    def _get_channel_handler(self, chl_type, channel):
        channels = self._channel_handlers[chl_type]
        if channel not in channels:
            raise ZCANException(f'Channel {channel} not exits or not initialized')
        return channels[channel]

    def _merge_support(self):
        if self._dev_type not in ZCAN_MERGE_SUPPORT_TYPE:
            raise ZCANException(f'ZLG: merge receive is not supported by {self._dev_type}!')

    def _get_can_init_config(self, mode, filter, **kwargs):
        pass

    def ResistanceStatus(self, channel, status=None):
        pass

    def SetFilters(self, channel, filters=None):
        pass

    # DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
    def OpenDevice(self, reserved=0):
        pass

    # UINT FUNC_CALL ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
    def CloseDevice(self):
        pass

    # UINT FUNC_CALL ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);
    def GetDeviceInf(self):
        pass

    # CHANNEL_HANDLE FUNC_CALL ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
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
        pass

    # UINT FUNC_CALL ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
    def StartCAN(self, channel):
        pass

    # UINT FUNC_CALL ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
    def ResetCAN(self, channel):
        pass

    # UINT FUNC_CALL ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
    def ClearBuffer(self, channel):
        pass

    # UINT FUNC_CALL ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        pass

    # UINT FUNC_CALL ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        pass

    # UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
    # UINT FUNC_CALL ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
    def GetReceiveNum(self, channel, msg_type: ZCANMessageType = ZCANMessageType.CAN):
        """
        获取指定通道已经接收到消息数量
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msg_type: 消息类型: 0 - CAN; 1 - CANFD; '-1' - LIN
        :return: 消息数量
        """
        pass

    # UINT FUNC_CALL ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
    def TransmitFD(self, channel, msgs, size=None):
        pass

    # UINT FUNC_CALL ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int timeout DEF(-1));
    def ReceiveFD(self, channel, size=1, timeout=-1):
        pass

    # # UINT FUNC_CALL ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
    def Transmit(self, channel, msgs, size=None):
        """
        发送CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msgs: 消息报文
        :param size: 报文大小
        :return: 实际发送报文长度
        """
        pass

    # UINT FUNC_CALL ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
    def Receive(self, channel, size=1, timeout=-1):
        """
        接收CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param size: 期待接收报文个数
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        pass

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
        pass



