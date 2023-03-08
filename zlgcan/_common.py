"""
by zhuyu4839@gmail.com
"""
import logging
import os.path
import platform as _platform
from ctypes import *

_curr_path = os.path.dirname(__file__)
_arch, _ = _platform.architecture()


class ZCANException(Exception):
    pass


class ZCANMessageType:
    LIN = c_uint(-1)
    CAN = c_uint(0)
    CANFD = c_uint(1)


class ZCANCanFdStd:
    ISO = 0
    NON_ISO = 0


class ZCANProtocol:
    CAN = 0
    CANFD_ISO = 1
    CANFD_NON_ISO = 2


class ZCANCanMode:
    NORMAL = 0
    READ_ONLY = 1
    # PCIECANFD-100U、PCIECANFD-400U、MiniPCIeCANFD、M.2CANFD支持
    SELF_SR = 2             # 自发自收
    SINGLE_SEND = 3         # 单次发送模式, 送失败时不会进行重发, 此时发送超时无效


class ZCANCanTransType:
    NORMAL = 0              # 正常发送
    SINGLE = 1              # 单次发送
    SELF_SR = 2             # 自发自收
    SINGLE_SELF_SR = 3      # 单次自发自收


class ZCANCanFilter:
    SINGLE = 1
    DOUBLE = 0


class ZCANCanType:
    CAN = c_uint(0)
    CANFD = c_uint(1)


ZCAN_DEVICE_TYPE = c_uint


class ZCANDeviceType:
    ZCAN_PCI5121                       = ZCAN_DEVICE_TYPE(1)
    ZCAN_PCI9810                       = ZCAN_DEVICE_TYPE(2)
    ZCAN_USBCAN1                       = ZCAN_DEVICE_TYPE(3)
    ZCAN_USBCAN2                       = ZCAN_DEVICE_TYPE(4)
    ZCAN_PCI9820                       = ZCAN_DEVICE_TYPE(5)
    ZCAN_CAN232                        = ZCAN_DEVICE_TYPE(6)
    ZCAN_PCI5110                       = ZCAN_DEVICE_TYPE(7)
    ZCAN_CANLITE                       = ZCAN_DEVICE_TYPE(8)
    ZCAN_ISA9620                       = ZCAN_DEVICE_TYPE(9)
    ZCAN_ISA5420                       = ZCAN_DEVICE_TYPE(10)
    ZCAN_PC104CAN                      = ZCAN_DEVICE_TYPE(11)
    ZCAN_CANETUDP                      = ZCAN_DEVICE_TYPE(12)
    ZCAN_CANETE                        = ZCAN_DEVICE_TYPE(12)
    ZCAN_DNP9810                       = ZCAN_DEVICE_TYPE(13)
    ZCAN_PCI9840                       = ZCAN_DEVICE_TYPE(14)
    ZCAN_PC104CAN2                     = ZCAN_DEVICE_TYPE(15)
    ZCAN_PCI9820I                      = ZCAN_DEVICE_TYPE(16)
    ZCAN_CANETTCP                      = ZCAN_DEVICE_TYPE(17)
    ZCAN_PCIE_9220                     = ZCAN_DEVICE_TYPE(18)
    ZCAN_PCI5010U                      = ZCAN_DEVICE_TYPE(19)
    ZCAN_USBCAN_E_U                    = ZCAN_DEVICE_TYPE(20)
    ZCAN_USBCAN_2E_U                   = ZCAN_DEVICE_TYPE(21)
    ZCAN_PCI5020U                      = ZCAN_DEVICE_TYPE(22)
    ZCAN_EG20T_CAN                     = ZCAN_DEVICE_TYPE(23)
    ZCAN_PCIE9221                      = ZCAN_DEVICE_TYPE(24)
    ZCAN_WIFICAN_TCP                   = ZCAN_DEVICE_TYPE(25)
    ZCAN_WIFICAN_UDP                   = ZCAN_DEVICE_TYPE(26)
    ZCAN_PCIe9120                      = ZCAN_DEVICE_TYPE(27)
    ZCAN_PCIe9110                      = ZCAN_DEVICE_TYPE(28)
    ZCAN_PCIe9140                      = ZCAN_DEVICE_TYPE(29)
    ZCAN_USBCAN_4E_U                   = ZCAN_DEVICE_TYPE(31)
    ZCAN_CANDTU_200UR                  = ZCAN_DEVICE_TYPE(32)
    ZCAN_CANDTU_MINI                   = ZCAN_DEVICE_TYPE(33)
    ZCAN_USBCAN_8E_U                   = ZCAN_DEVICE_TYPE(34)
    ZCAN_CANREPLAY                     = ZCAN_DEVICE_TYPE(35)
    ZCAN_CANDTU_NET                    = ZCAN_DEVICE_TYPE(36)
    ZCAN_CANDTU_100UR                  = ZCAN_DEVICE_TYPE(37)
    ZCAN_PCIE_CANFD_100U               = ZCAN_DEVICE_TYPE(38)
    ZCAN_PCIE_CANFD_200U               = ZCAN_DEVICE_TYPE(39)
    ZCAN_PCIE_CANFD_400U               = ZCAN_DEVICE_TYPE(40)
    ZCAN_USBCANFD_200U                 = ZCAN_DEVICE_TYPE(41)
    ZCAN_USBCANFD_100U                 = ZCAN_DEVICE_TYPE(42)
    ZCAN_USBCANFD_MINI                 = ZCAN_DEVICE_TYPE(43)
    ZCAN_CANFDCOM_100IE                = ZCAN_DEVICE_TYPE(44)
    ZCAN_CANSCOPE                      = ZCAN_DEVICE_TYPE(45)
    ZCAN_CLOUD                         = ZCAN_DEVICE_TYPE(46)
    ZCAN_CANDTU_NET_400                = ZCAN_DEVICE_TYPE(47)
    ZCAN_CANFDNET_TCP                  = ZCAN_DEVICE_TYPE(48)
    ZCAN_CANFDNET_200U_TCP             = ZCAN_DEVICE_TYPE(48)
    ZCAN_CANFDNET_UDP                  = ZCAN_DEVICE_TYPE(49)
    ZCAN_CANFDNET_200U_UDP             = ZCAN_DEVICE_TYPE(49)
    ZCAN_CANFDWIFI_TCP                 = ZCAN_DEVICE_TYPE(50)
    ZCAN_CANFDWIFI_100U_TCP            = ZCAN_DEVICE_TYPE(50)
    ZCAN_CANFDWIFI_UDP                 = ZCAN_DEVICE_TYPE(51)
    ZCAN_CANFDWIFI_100U_UDP            = ZCAN_DEVICE_TYPE(51)
    ZCAN_CANFDNET_400U_TCP             = ZCAN_DEVICE_TYPE(52)
    ZCAN_CANFDNET_400U_UDP             = ZCAN_DEVICE_TYPE(53)
    ZCAN_CANFDBLUE_200U                = ZCAN_DEVICE_TYPE(54)
    ZCAN_CANFDNET_100U_TCP             = ZCAN_DEVICE_TYPE(55)
    ZCAN_CANFDNET_100U_UDP             = ZCAN_DEVICE_TYPE(56)
    ZCAN_CANFDNET_800U_TCP             = ZCAN_DEVICE_TYPE(57)
    ZCAN_CANFDNET_800U_UDP             = ZCAN_DEVICE_TYPE(58)
    ZCAN_USBCANFD_800U                 = ZCAN_DEVICE_TYPE(59)
    ZCAN_PCIE_CANFD_100U_EX            = ZCAN_DEVICE_TYPE(60)
    ZCAN_PCIE_CANFD_400U_EX            = ZCAN_DEVICE_TYPE(61)
    ZCAN_PCIE_CANFD_200U_MINI          = ZCAN_DEVICE_TYPE(62)
    ZCAN_PCIE_CANFD_200U_M2            = ZCAN_DEVICE_TYPE(63)
    ZCAN_CANFDDTU_400_TCP              = ZCAN_DEVICE_TYPE(64)
    ZCAN_CANFDDTU_400_UDP              = ZCAN_DEVICE_TYPE(65)
    ZCAN_CANFDWIFI_200U_TCP            = ZCAN_DEVICE_TYPE(66)
    ZCAN_CANFDWIFI_200U_UDP            = ZCAN_DEVICE_TYPE(67)
    ZCAN_CANFDDTU_800ER_TCP            = ZCAN_DEVICE_TYPE(68)
    ZCAN_CANFDDTU_800ER_UDP            = ZCAN_DEVICE_TYPE(69)
    ZCAN_CANFDDTU_800EWGR_TCP          = ZCAN_DEVICE_TYPE(70)
    ZCAN_CANFDDTU_800EWGR_UDP          = ZCAN_DEVICE_TYPE(71)
    ZCAN_CANFDDTU_600EWGR_TCP          = ZCAN_DEVICE_TYPE(72)
    ZCAN_CANFDDTU_600EWGR_UDP          = ZCAN_DEVICE_TYPE(73)

    ZCAN_OFFLINE_DEVICE                = ZCAN_DEVICE_TYPE(98)
    ZCAN_VIRTUAL_DEVICE                = ZCAN_DEVICE_TYPE(99)


ZUSBCANFD_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U,
                  ZCANDeviceType.ZCAN_USBCANFD_100U,
                  ZCANDeviceType.ZCAN_USBCANFD_MINI)
ZUSBCAN_XE_U_TYPE = (ZCANDeviceType.ZCAN_USBCAN_E_U,
                     ZCANDeviceType.ZCAN_USBCAN_2E_U,
                     ZCANDeviceType.ZCAN_USBCAN_4E_U)
ZUSBCAN_I_II_TYPE = (ZCANDeviceType.ZCAN_USBCAN1,
                     ZCANDeviceType.ZCAN_USBCAN2)
ZCAN_MERGE_SUPPORT_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U,
                           ZCANDeviceType.ZCAN_USBCANFD_100U,
                           ZCANDeviceType.ZCAN_USBCANFD_MINI,
                           ZCANDeviceType.ZCAN_USBCANFD_800U,
                           )

INVALID_DEVICE_HANDLE = 0
INVALID_CHANNEL_HANDLE = 0

ZCAN_ERROR_CAN_OVERFLOW            = 0x0001
ZCAN_ERROR_CAN_ERRALARM            = 0x0002
ZCAN_ERROR_CAN_PASSIVE             = 0x0004
ZCAN_ERROR_CAN_LOSE                = 0x0008
ZCAN_ERROR_CAN_BUSERR              = 0x0010
ZCAN_ERROR_CAN_BUSOFF              = 0x0020
ZCAN_ERROR_CAN_BUFFER_OVERFLOW     = 0x0040

ZCAN_ERROR_DEVICEOPENED            = 0x0100
ZCAN_ERROR_DEVICEOPEN              = 0x0200
ZCAN_ERROR_DEVICENOTOPEN           = 0x0400
ZCAN_ERROR_BUFFEROVERFLOW          = 0x0800
ZCAN_ERROR_DEVICENOTEXIST          = 0x1000
ZCAN_ERROR_LOADKERNELDLL           = 0x2000
ZCAN_ERROR_CMDFAILED               = 0x4000
ZCAN_ERROR_BUFFERCREATE            = 0x8000

ZCAN_ERROR_CANETE_PORTOPENED       = 0x00010000
ZCAN_ERROR_CANETE_INDEXUSED        = 0x00020000
ZCAN_ERROR_REF_TYPE_ID             = 0x00030001
ZCAN_ERROR_CREATE_SOCKET           = 0x00030002
ZCAN_ERROR_OPEN_CONNECT            = 0x00030003
ZCAN_ERROR_NO_STARTUP              = 0x00030004
ZCAN_ERROR_NO_CONNECTED            = 0x00030005
ZCAN_ERROR_SEND_PARTIAL            = 0x00030006
ZCAN_ERROR_SEND_TOO_FAST           = 0x00030007

ZCAN_STATUS_ERR                    = 0
ZCAN_STATUS_OK                     = 1
ZCAN_STATUS_ONLINE                 = 2
ZCAN_STATUS_OFFLINE                = 3
ZCAN_STATUS_UNSUPPORTED            = 4

ZCAN_CMD_DESIP                     = 0
ZCAN_CMD_DESPORT                   = 1
ZCAN_CMD_CHGDESIPANDPORT           = 2
ZCAN_CMD_SRCPORT                   = 2
ZCAN_CMD_TCP_TYPE                  = 4
ZCAN_TCP_CLIENT                    = 0
ZCAN_TCP_SERVER                    = 1

ZCAN_CMD_CLIENT_COUNT              = 5
ZCAN_CMD_CLIENT                    = 6
ZCAN_CMD_DISCONN_CLINET            = 7
ZCAN_CMD_SET_RECONNECT_TIME        = 8

ZCAN_TYPE_CAN                      = 0
ZCAN_TYPE_CANFD                    = 1
ZCAN_TYPE_ALL_DATA                 = 2

ZCLOUD_MAX_DEVICES                 = 100
ZCLOUD_MAX_CHANNEL                 = 16

ZCAN_LIN_MODE_MASTER               = 0
ZCAN_LIN_MODE_SLAVE                = 1
ZCAN_LIN_FLAG_CHK_ENHANCE          = 0x01
ZCAN_LIN_FLAG_VAR_DLC              = 0x02

def _library_check_run(_library, func_name, *args, **kwargs):
    ret = getattr(_library, func_name)(*args, **kwargs)
    if ret != ZCAN_STATUS_OK:
        raise ZCANException(f'ZLG: {func_name} failed!')
    return ret

class ZCAN_DEVICE_INFO(Structure):  # ZCAN_DEVICE_INFO

    _fields_ = [('hwv', c_uint16),  # /**< hardware version */
                ('fwv', c_uint16),  # /**< firmware version */
                ('drv', c_uint16),  # /**< driver version */
                ('api', c_uint16),  # /**< API version */
                ('irq', c_uint16),  # /**< IRQ */
                ('chn', c_uint8),  # /**< channels */
                ('sn', c_uint8 * 20),  # /**< serial number */
                ('id', c_uint8 * 40),  # /**< card id */
                ('pad', c_uint8 * 4)]

    def __str__(self):
        return f"Hardware Version : {self.hw_version}\n" \
               f"Firmware Version : {self.fw_version}\n" \
               f"Driver Version   : {self.dr_version}\n" \
               f"Interface Version: {self.in_version}\n" \
               f"Interrupt Number : {self.irq_num}\n" \
               f"CAN Number       : {self.can_num}\n" \
               f"Serial           : {self.serial}\n" \
               f"Hardware Type    : {self.hw_type}"

    def _version(self, version):
        return "V%02x.%02x" if version // 0xFF >= 9 else "V%d.%02x" % (version // 0xFF, version & 0xFF)

    @property
    def hw_version(self):
        return self._version(self.hwv)

    @property
    def fw_version(self):
        return self._version(self.fwv)

    @property
    def dr_version(self):
        return self._version(self.drv)

    @property
    def in_version(self):
        return self._version(self.api)

    @property
    def irq_num(self):
        return self._version(self.irq)

    @property
    def can_num(self):
        return self.chn

    @property
    def serial(self):
        return bytes(self.sn).decode('utf-8')

    @property
    def hw_type(self):
        return bytes(self.id).decode('utf-8')


class _ZLGCAN(object):

    def __init__(self, resend):
        """
        Create ZLG-CAN object
        :param resend: true if retry to send a frame until success else false 
        """
        # if _library is None:
        #     raise ZCANException(
        #         "The ZLG-CAN driver could not be loaded. "
        #         "Check that you are using 32-bit/64bit Python on Windows or 64bit Python on Linux."
        #     )
        self._logger = logging.getLogger(self.__class__.__name__)
        self._resend = resend
        self._dev_index = None
        self._dev_type = None
        # self._dev_type_name = None
        self._dev_info = None
        self._dev_is_canfd = None
        self._channels = ()
        # {'CAN': {chl_obj: is_canfd}, 'LIN': {chl_obj: is_master}}
        self._channel_handlers = {'CAN': {}, 'LIN': {}}     # "CAN": {channel: channel_handler}
        self._dev_handler = None

    @property
    def device_index(self):
        return self._dev_index

    @property
    def device_is_canfd(self):
        return self._dev_is_canfd

    @property
    def channels(self) -> tuple:
        return self._channels

    @property
    def resend(self):
        return self._resend

    def _get_channel_handler(self, chl_type, channel):
        channels = self._channel_handlers[chl_type]
        if channel not in channels:
            raise ZCANException(f'Channel {channel} not exits or not initialized')
        return channels[channel]

    def _merge_support(self):
        if self._dev_type not in (ZCANDeviceType.ZCAN_USBCANFD_200U, ZCANDeviceType.ZCAN_USBCANFD_100U,
                                  ZCANDeviceType.ZCAN_USBCANFD_MINI, ZCANDeviceType.ZCAN_CANFDNET_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_UDP, ZCANDeviceType.ZCAN_CANFDNET_400U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_400U_UDP, ZCANDeviceType.ZCAN_CANFDNET_100U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_100U_UDP, ZCANDeviceType.ZCAN_CANFDNET_800U_TCP,
                                  ZCANDeviceType.ZCAN_CANFDNET_800U_UDP, ZCANDeviceType.ZCAN_CANFDWIFI_TCP,
                                  ZCANDeviceType.ZCAN_CANFDWIFI_UDP, ZCANDeviceType.ZCAN_CANFDDTU_400_TCP,
                                  ZCANDeviceType.ZCAN_CANFDDTU_400_UDP, ZCANDeviceType.ZCAN_PCIE_CANFD_100U_EX,
                                  ZCANDeviceType.ZCAN_PCIE_CANFD_400U_EX, ZCANDeviceType.ZCAN_PCIE_CANFD_200U_MINI,
                                  ZCANDeviceType.ZCAN_PCIE_CANFD_200U_M2):
            raise ZCANException(f'ZLG: merge receive is not supported by {self._dev_type}!')

    def _get_can_init_config(self, mode, filter, **kwargs):
        pass

    def ResistanceStatus(self, channel, status=None):
        pass

    def SetFilters(self, channel, filters=None):
        pass

    # DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
    def OpenDevice(self, dev_type: ZCANDeviceType, dev_index=0, reserved=0):
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



