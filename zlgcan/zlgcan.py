"""
by zhuyu4839@gmail.com
"""
import logging
import os
import platform
import warnings
from ctypes import *

_curr_path = os.path.split(os.path.realpath(__file__))[0]
_arch, _os = platform.architecture()
_is_windows, _is_linux = False, False
if 'windows' in _os.lower():
    _is_windows = True
    if _arch == '32bit':
        _lib_path = os.path.join(_curr_path, 'windows/x86/zlgcan/zlgcan.dll')
    else:
        _lib_path = os.path.join(_curr_path, 'windows/x86_64/zlgcan/zlgcan.dll')
    _library = windll.LoadLibrary(_lib_path)
elif 'linux' in _os.lower():
    _is_linux = True
    if _arch == '64bit':
        _lib_path = os.path.join(_curr_path, 'linux/x86_64/zlgcan/libusbcanfd.so')
    else:
        _lib_path = None
    if not _lib_path:
        _library = cdll.LoadLibrary(_lib_path)
else:
    _library = None


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


_path = lambda ch, path: f'{ch}/{path}' if ch else f'{path}'
_version = lambda version: ("V%02x.%02x" if version // 0xFF >= 9 else "V%d.%02x") % (version // 0xFF, version & 0xFF)

if _is_linux:
    ON = c_int32(1)
    OFF = c_int32(0)
    CMD_CAN_FILTER = 0x14
    CMD_CAN_SKD_SEND = 0x16
    CMD_CAN_SKD_SEND_STATUS = 0x17
    CMD_CAN_RES = 0x18
    CMD_CAN_TIMEOUT = 0x44

    class _ZCANInitASet(Structure):
        _fields_ = [('tseg1', c_uint8),
                    ('tseg2', c_uint8),
                    ('sjw', c_uint8),
                    ('smp', c_uint8),
                    ('brp', c_uint16)]

    class _ZCANInitDSet(Structure):
        _fields_ = [('tseg1', c_uint8),
                    ('tseg2', c_uint8),
                    ('sjw', c_uint8),
                    ('smp', c_uint8),
                    ('brp', c_uint16)]

    class ZCAN_MSG_INFO(Structure):
        _pack_ = 1
        _fields_ = [('txm', c_uint32, 4),       # 发送方式，0为正常模式，2为自发自收（仅用于自测）
                    ('fmt', c_uint32, 4),       # 0-CAN帧，1-CANFD帧
                    ('sdf', c_uint32, 1),       # 0-数据帧，1-远程帧
                    ('sef', c_uint32, 1),       # 0-标准帧，1-扩展帧
                    ('err', c_uint32, 1),       # 0-正常帧，1-错误帧
                    ('brs', c_uint32, 1),       # 0-CANFD不加速，1-CANFD加速
                    ('est', c_uint32, 1),       # 错误状态，0-积极错误，1-消极错误
                    ('pad', c_uint32, 19)]

    class ZCAN_MSG_HEADER(Structure):
        _fields_ = [('ts', c_uint32),           # timestamp
                    ('id', c_uint32),           # can id
                    ('inf', ZCAN_MSG_INFO),     # msg info
                    ('pad', c_uint16),          # revers
                    ('chn', c_uint8),           # channel
                    ('len', c_uint8)]           # dlc

    class ZCAN_FILTER(Structure):
        _fields_ = [('type', c_uint8),          # /**< 0-std_frame, 1-ext_frame */
                    ('pad', c_uint8 * 3),
                    ('sid', c_uint32),          # /**< start-id */
                    ('eid', c_uint32)]          # /**< end-id */

    class ZCAN_FILTER_TABLE(Structure):
        _fields_ = [('size', c_uint32),
                    ('table', ZCAN_FILTER * 64)]

class ZCAN_DEVICE_INFO(Structure):  # ZCAN_DEVICE_INFO
    """
    Device information
    """
    if _is_windows:
        _fields_ = [("hw_Version", c_ushort),               # /**< hardware version */
                    ("fw_Version", c_ushort),               # /**< firmware version */
                    ("dr_Version", c_ushort),               # /**< driver version */
                    ("in_Version", c_ushort),               # /**< API version */
                    ("irq_Num", c_ushort),                  # /**< IRQ */
                    ("can_Num", c_ubyte),                   # /**< channels */
                    ("str_Serial_Num", c_ubyte * 20),       # /**< serial number */
                    ("str_hw_Type", c_ubyte * 40),          # /**< card id */
                    ("reserved", c_ushort * 4)]
    elif _is_linux:
        _fields_ = [('hwv', c_uint16),                      # /**< hardware version */
                    ('fwv', c_uint16),                      # /**< firmware version */
                    ('drv', c_uint16),                      # /**< driver version */
                    ('api', c_uint16),                      # /**< API version */
                    ('irq', c_uint16),                      # /**< IRQ */
                    ('chn', c_uint8),                       # /**< channels */
                    ('sn', c_uint8 * 20),                   # /**< serial number */
                    ('id', c_uint8 * 40),                   # /**< card id */
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

    @property
    def hw_version(self):
        if _is_windows:
            return _version(self.hw_Version)
        elif _is_linux:
            return _version(self.hwv)

    @property
    def fw_version(self):
        if _is_windows:
            return _version(self.fw_Version)
        elif _is_linux:
            return _version(self.fwv)

    @property
    def dr_version(self):
        if _is_windows:
            return _version(self.dr_Version)
        elif _is_linux:
            return _version(self.drv)

    @property
    def in_version(self):
        if _is_windows:
            return _version(self.in_Version)
        elif _is_linux:
            return _version(self.api)

    @property
    def irq_num(self):
        if _is_windows:
            return self.irq_Num
        elif _is_linux:
            return _version(self.irq)

    @property
    def can_num(self):
        if _is_windows:
            return self.can_Num
        elif _is_linux:
            return self.chn

    @property
    def serial(self):
        if _is_windows:
            return bytes(self.str_Serial_Num).decode('utf-8')
        elif _is_linux:
            return bytes(self.sn).decode('utf-8')

    @property
    def hw_type(self):
        if _is_windows:
            return bytes(self.str_hw_Type).decode('utf-8')
        elif _is_linux:
            return bytes(self.id).decode('utf-8')

class ZCAN_CAN_FRAME(Structure):               # ZCAN_CAN_FRAME
    if _is_windows:
        _fields_ = [("can_id", c_uint, 29),
                    ("err", c_uint, 1),         # 错误帧标识CANID bit29
                    ("rtr", c_uint, 1),         # 远程帧标识CANID bit30
                    ("eff", c_uint, 1),         # 扩展帧标识CANID bit31
                    ("can_dlc", c_ubyte),       # 数据长度
                    ("__pad", c_ubyte),         # 队列模式下bit7为延迟发送标志位
                    ("__res0", c_ubyte),        # 队列模式下帧间隔低8位, 单位 ms
                    ("__res1", c_ubyte),        # 队列模式下帧间隔高8位, 单位 ms
                    ("data", c_ubyte * 8)]
    elif _is_linux:
        _fields_ = [('hdr', ZCAN_MSG_HEADER),
                    ('dat', c_uint8 * 8)]

class ZCAN_CANFD_FRAME(Structure):             # ZCAN_CANFD_FRAME
    if _is_windows:
        _fields_ = [("can_id", c_uint, 29),
                    ("err", c_uint, 1),         # 错误帧标识CANID bit29
                    ("rtr", c_uint, 1),         # 远程帧标识CANID bit30
                    ("eff", c_uint, 1),         # 扩展帧标识CANID bit31
                    ("len", c_ubyte),           # 数据长度
                    ("brs", c_ubyte, 1),        # Bit Rate Switch, flags bit0
                    ("esi", c_ubyte, 1),        # Error State Indicator, flags bit1
                    ("__res", c_ubyte, 6),      # 保留, flags bit2-7
                    ("__res0", c_ubyte),        # 队列模式下帧间隔低8位, 单位 ms
                    ("__res1", c_ubyte),        # 队列模式下帧间隔高8位, 单位 ms
                    ("data", c_ubyte * 64)]
    elif _is_linux:
        _fields_ = [('hdr', ZCAN_MSG_HEADER),
                    ('dat', c_uint8 * 64)]

class ZCAN_CHANNEL_ERR_INFO(Structure):           # ZCAN_CHANNEL_ERR_INFO
    if _is_windows:
        ERROR_CODE = {
            0x0001: 'CAN FIFO Overflow',
            0x0002: 'CAN Error Warning',
            0x0004: 'CAN Passive Error',
            0x0008: 'CAN Arbitration Lost',
            0x0010: 'CAN Bus Error',
            0x0020: 'CAN Bus closed',
            0x0040: 'CAN Cache Overflow'
        }
        _fields_ = [("error_code", c_uint),
                    ("passive_ErrData", c_ubyte * 3),
                    ("arLost_ErrData", c_ubyte)]

        def __str__(self):
            return f'error info           : {self.ERROR_CODE[self.error_code]} \n' \
                   f'passive error info   : {bytes(self.passive_ErrData).hex()} \n' \
                   f'arbitration lost info: {self.arLost_ErrData}'
    elif _is_linux:
        _fields_ = [('hdr', ZCAN_MSG_HEADER),
                    ('dat', c_uint8 * 8)]

class ZCAN_CHANNEL_STATUS(Structure):         # ZCAN_CHANNEL_STATUS
    if _is_windows:
        _fields_ = [("errInterrupt", c_ubyte),
                    ("regMode", c_ubyte),
                    ("regStatus", c_ubyte),
                    ("regALCapture", c_ubyte),
                    ("regECCapture", c_ubyte),
                    ("regEWLimit", c_ubyte),
                    ("regRECounter", c_ubyte),
                    ("regTECounter", c_ubyte),
                    ("Reserved", c_ubyte)]
    elif _is_linux:
        _fields_ = [('IR', c_uint8),                    # /**< not used(for backward compatibility) */
                    ('MOD', c_uint8),                   # /**< not used */
                    ('SR', c_uint8),                    # /**< not used */
                    ('ALC', c_uint8),                   # /**< not used */
                    ('ECC', c_uint8),                   # /**< not used */
                    ('EWL', c_uint8),                   # /**< not used */
                    ('RXE', c_uint8),                   # /**< RX errors */
                    ('TXE', c_uint8),                   # /**< TX errors */
                    ('PAD', c_uint32)]

if _is_linux:
    class ZCAN_TTX(Structure):
        _fields_ = [('interval', c_uint32),             # 定时发送周期，单位百微秒
                    ('repeat', c_uint16),               # 发送次数，0等于无线循环发
                    ('index', c_uint8),                 # 定时发送列表的帧索引号，也就是第几条定时发送报文
                    ('flags', c_uint8),                 # 0-此帧禁用定时发送，1-此帧使能定时发送
                    ('msg', ZCAN_CANFD_FRAME)]

    class ZCAN_TTX_TABLE(Structure):
        _fields_ = [('size', c_uint32),
                    ('table', ZCAN_TTX * 8)]

if _is_windows:
    class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):     # _ZCAN_CHANNEL_CAN_INIT_CONFIG
        _fields_ = [("acc_code", c_uint),
                    ("acc_mask", c_uint),
                    ("reserved", c_uint),
                    ("filter", c_ubyte),
                    ("timing0", c_ubyte),
                    ("timing1", c_ubyte),
                    ("mode", c_ubyte)]

    class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):    # _ZCAN_CHANNEL_CANFD_INIT_CONFIG
        _fields_ = [("acc_code", c_uint),
                    ("acc_mask", c_uint),
                    ("abit_timing", c_uint),
                    ("dbit_timing", c_uint),
                    ("brp", c_uint),
                    ("filter", c_ubyte),
                    ("mode", c_ubyte),
                    ("pad", c_ushort),
                    ("reserved", c_uint)]

    class _ZCAN_CHANNEL_INIT_CONFIG(Union):         # union in ZCAN_CHANNEL_INIT_CONFIG
        _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

    class ZCAN_CHANNEL_INIT_CONFIG(Structure):       # ZCAN_CHANNEL_INIT_CONFIG
        if _is_windows:
            _fields_ = [("can_type", c_uint),
                        ("config", _ZCAN_CHANNEL_INIT_CONFIG)]
        elif _is_linux:
            _fields_ = [('clk', c_uint32),
                        ('mode', c_uint32),
                        ('aset', _ZCANInitASet),
                        ('dset', _ZCANInitDSet)]

    class ZCAN_Transmit_Data(Structure):            # ZCAN_Transmit_Data
        _pack_ = 1
        _fields_ = [("frame", ZCAN_CAN_FRAME),
                    ("transmit_type", c_uint)]      # 0=正常发送, 1=单次发送, 2=自发自收, 3=单次自发自收

    class ZCAN_Receive_Data(Structure):             # ZCAN_Receive_Data
        _fields_ = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

    class ZCAN_TransmitFD_Data(Structure):          # ZCAN_TransmitFD_Data
        _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

    class ZCAN_ReceiveFD_Data(Structure):           # ZCAN_ReceiveFD_Data
        _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]

    class ZCAN_AUTO_TRANSMIT_OBJ(Structure):         # ZCAN_AUTO_TRANSMIT_OBJ
        _fields_ = [("enable", c_ushort),
                    ("index", c_ushort),
                    ("interval", c_uint),  # ms
                    ("obj", ZCAN_Transmit_Data)]

    class ZCANFD_AUTO_TRANSMIT_OBJ(Structure):       # ZCANFD_AUTO_TRANSMIT_OBJ
        _fields_ = [("enable", c_ushort),
                    ("index", c_ushort),
                    ("interval", c_uint),
                    ("obj", ZCAN_TransmitFD_Data)]

    # 用于设置定时发送额外的参数, 目前只支持USBCANFD-X00U系列设备
    class ZCAN_AUTO_TRANSMIT_OBJ_PARAM(Structure):      # ZCANFD_AUTO_TRANSMIT_OBJ_PARAM
        _fields_ = [("index", c_ushort),                # 定时发送帧的索引
                    ("type", c_ushort),                 # 参数类型，目前类型只有1：表示启动延时
                    ("value", c_uint)]                  # 参数数值

    class ZCLOUD_CHNINFO(Structure):                       # ZCLOUD_CHNINFO
        _fields_ = [("enable", c_ubyte),                    # // 0:CAN, 1:ISO CANFD, 2:Non-ISO CANFD
                    ("type", c_ubyte),
                    ("isUpload", c_ubyte),
                    ("isDownload", c_ubyte)]

        def __str__(self):
            return f'enable    : {self.enable}\n' \
                   f'type      : {self.type}\n' \
                   f'isUpload  : {self.isUpload}\n' \
                   f'isDownload: {self.isDownload}\n'

    class ZCLOUD_DEVINFO(Structure):                        # ZCLOUD_DEVINFO
        _fields_ = [("devIndex", c_int),
                    ("type", c_char * 64),
                    ("id", c_char * 64),
                    ("name", c_char * 64),
                    ("owner", c_char * 64),
                    ("model", c_char * 64),
                    ("fwVer", c_char * 16),
                    ("hwVer", c_char * 16),
                    ("serial", c_char * 64),
                    ("status", c_int),  # 0:online, 1:offline
                    ("bGpsUpload", c_ubyte),
                    ("channelCnt", c_ubyte),
                    ("channels", ZCLOUD_CHNINFO * ZCLOUD_MAX_CHANNEL)]

    class ZCLOUD_USER_DATA(Structure):                          # ZCLOUD_USER_DATA
        _fields_ = [("username", c_char * 64),
                    ("mobile", c_char * 64),
                    ("dllVer", c_char * 16),
                    ("devCnt", c_size_t),
                    ("channels", ZCLOUD_DEVINFO * ZCLOUD_MAX_DEVICES)]

    class _ZCLOUD_GPS_FRAMETime(Structure):
        _fields_ = [("year", c_ushort),
                    ("mon", c_ushort),
                    ("day", c_ushort),
                    ("hour", c_ushort),
                    ("min", c_ushort),
                    ("sec", c_ushort)]

    class ZCLOUD_GPS_FRAME(Structure):                          # ZCLOUD_GPS_FRAME
        _fields_ = [("latitude", c_float),  # + north latitude, - south latitude
                    ("longitude", c_float),  # + east longitude, - west longitude
                    ("speed", c_float),  # km/h
                    ("tm", _ZCLOUD_GPS_FRAMETime)]

    class USBCANFDTxTimeStamp(Structure):                    # USBCANFDTxTimeStamp
        _fields_ = [("pTxTimeStampBuffer", POINTER(c_uint)),    # allocated by user, size:nBufferTimeStampCount * 4,unit:100us
                    ("nBufferTimeStampCount", c_uint)]          # buffer size

    class TxTimeStamp(Structure):                            # TxTimeStamp
        _fields_ = [("pTxTimeStampBuffer", POINTER(c_uint64)),  # allocated by user, size:nBufferTimeStampCount * 8,unit:1us
                    ("nBufferTimeStampCount", c_uint),          # buffer timestamp count
                    ("nWaitTime", c_int)]                       # Wait Time ms, -1表示等到有数据才返回

    class BusUsage(Structure):                               # BusUsage
        _fields_ = [('nTimeStampBegin', c_int64),               # 测量起始时间戳，单位us
                    ('nTimeStampEnd', c_int64),                 # 测量结束时间戳，单位us
                    ('nChnl', c_ubyte),                         # 通道
                    ('nReserved', c_ubyte),                     # 保留
                    ('nBusUsage', c_ushort),                    # 总线利用率(%),总线利用率*100展示。取值0~10000，如8050表示80.50%
                    ('nFrameCount', c_uint)]                    # 帧数量

    class ZCAN_LIN_MSG(Structure):                               # ZCAN_LIN_MSG
        _fields_ = [("ID", c_ubyte),
                    ("DataLen", c_byte),
                    ("Flag", c_ushort),
                    ("TimeStamp", c_uint),
                    ("Data", c_ubyte * 8)]

    class ZCAN_LIN_INIT_CONFIG(Structure):                   # ZCAN_LIN_INIT_CONFIG
        _fields_ = [("linMode", c_ubyte),
                    ("linFlag", c_byte),
                    ("reserved", c_ushort),
                    ("linBaud", c_uint)]

    class _ZCANCANFDDataFlag(Structure):              # ZCANdataFlag
        # _fields_ = [("unionVal", _ZlgCanFdDataFlagVal), ("rawVal", c_uint)]
        _pack_ = 1
        _fields_ = [("frameType", c_uint, 2),       # 0-can,1-canfd
                    ("txDelay", c_uint, 2),         # 队列发送延时，延时时间存放在 timeStamp 字段
                                                    # 0：不启用延时,
                                                    # 1：启用延时，延时时间单位为 1 毫秒(1ms),
                                                    # 2：启用延时，延时时间单位为 100 微秒(0.1ms)
                    ("transmitType", c_uint, 4),    # 发送方式，0-正常发送, 1：单次发送, 2：自发自收, 3：单次自发自收
                    ("txEchoRequest", c_uint, 1),   # 发送回显请求，0-不回显，1-回显
                    ("txEchoed", c_uint, 1),        # 报文是否是发送回显报文, 0：正常总线接收到的报文, 1：本设备发送回显报文
                    ("reserved", c_uint, 22)]       # 保留

    class ZCANCANFDData(Structure):                  # ZCANCANFDData
        _pack_ = 1
        _fields_ = [("timeStamp", c_uint64),
                    ("flag", _ZCANCANFDDataFlag),
                    ("extraData", c_ubyte * 4),  # 保留
                    ("frame", ZCAN_CANFD_FRAME)]

    class ZCANErrorData(Structure):                              # ZCANErrorData
        _pack_ = 1
        _fields_ = [("timeStamp", c_uint64),
                    ("errType", c_ubyte),
                    ("errSubType", c_ubyte),
                    ("nodeState", c_ubyte),
                    ("rxErrCount", c_ubyte),
                    ("txErrCount", c_ubyte),
                    ("errData", c_ubyte),
                    ("reserved", c_ubyte * 2)]

    class _ZCANGPSDataTime(Structure):
        _pack_ = 1
        _fields_ = [("year", c_ushort),
                    ("mon", c_ushort),
                    ("day", c_ushort),
                    ("hour", c_ushort),
                    ("min", c_ushort),
                    ("sec", c_ushort),
                    ("milsec", c_ushort)]

    class _ZCANGPSDataFlag(Structure):
        # _fields_ = [("unionVal", _ZlgGpsDataFlagVal), ("rawVal", c_ushort)]
        _pack_ = 1
        _fields_ = [("timeValid", c_ushort, 1),         # 时间数据是否有效
                    ("latlongValid", c_ushort, 1),      # 经纬度数据是否有效
                    ("altitudeValid", c_ushort, 1),     # 海拔数据是否有效
                    ("speedValid", c_ushort, 1),        # 速度数据是否有效
                    ("courseAngleValid", c_ushort, 1),  # 航向角数据是否有效
                    ("reserved", c_ushort, 13)]         # 保留

    class ZCANGPSData(Structure):                        # ZCANGPSData
        _pack_ = 1
        _fields_ = [("time", _ZCANGPSDataTime),
                    ("flag", _ZCANGPSDataFlag),
                    ("latitude", c_float),              # 纬度 正数表示北纬, 负数表示南纬
                    ("longitude", c_float),             # 经度 正数表示东经, 负数表示西经
                    ("altitude", c_float),              # 海拔 单位: 米
                    ("speed", c_float),                 # 速度 单位: km/h
                    ("courseAngle", c_float)]           # 航向角

    class _ZCANLINDataPid(Structure):
        # _fields_ = [("unionVal", _ZlgLinDataPidVal), ("rawVal", c_ubyte)]
        _pack_ = 1
        _fields_ = [('ID', c_ubyte, 6),
                    ('Parity', c_ubyte, 2)]

    class _ZCANLINDataFlag(Structure):
        _pack_ = 1
        # _fields_ = [("unionVal", _ZlgLinDataFlagVal), ("rawVal", c_ushort)]
        _fields_ = [('tx', c_ushort, 1),                # 控制器发送在总线上的消息, 接收有效
                    ('rx', c_ushort, 1),                # 控制器接收总线上的消息, 接收有效
                    ('noData', c_ushort, 1),            # 无数据区
                    ('chkSumErr', c_ushort, 1),         # 校验和错误
                    ('parityErr', c_ushort, 1),         # 奇偶校验错误, 此时消息中的 chksum 无效
                    ('syncErr', c_ushort, 1),           # 同步段错误
                    ('bitErr', c_ushort, 1),            # 发送时位错误
                    ('wakeUp', c_ushort, 1),            # 收到唤醒帧, 此时消息ID|数据长度|数据域|校验值无效
                    ('reserved', c_ushort, 8)]          # 保留

    class ZCANLINData(Structure):                        # ZCANLINData
        _pack_ = 1
        _fields_ = [("timeStamp", c_uint64),
                    ("PID", _ZCANLINDataPid),
                    ("dataLen", c_ubyte),               # 数据长度
                    ("flag", _ZCANLINDataFlag),
                    ("chkSum", c_ubyte),
                    ("reserved", c_ubyte * 3),
                    ("data", c_ubyte * 8)]

    class _ZCANDataObjFlag(Union):
        # _fields_ = [("unionVal", _ZlgDataObjFlagVal), ("rawVal", c_ushort)]
        _pack_ = 1
        _fields_ = [("reserved", c_ushort, 16)]

    class _ZCANDataObjData(Union):
        _pack_ = 1
        _fields_ = [("zcanCANFDData", ZCANCANFDData), ("zcanErrData", ZCANErrorData),
                    ("zcanGPSData", ZCANGPSData), ("zcanLINData", ZCANLINData), ("raw", c_ubyte * 92)]

    # 合并接收数据数据结构, 支持CAN/CANFD/LIN/GPS/错误等不同类型数据
    class ZCANDataObj(Structure):                    # ZCANDataObj
        _pack_ = 1
        _fields_ = [("dataType", c_ubyte),          # 数据类型, 参考eZCANDataDEF中 数据类型 部分定义
                                                    # 1 - CAN/CANFD 数据，data.zcanCANFDData 有效
                                                    # 2 - 错误数据，data.zcanErrData 有效
                                                    # 3 - GPS 数据，data.zcanGPSData 有效
                                                    # 4 - LIN 数据，data.zcanLINData 有效
                    ("chnl", c_ubyte),  # 数据通道
                    ("flag", _ZCANDataObjFlag),     # 标志信息, 暂未使用
                    ("extraData", c_ubyte * 4),     # 额外数据, 暂未使用
                    ("data", _ZCANDataObjData)]     # 实际数据, 联合体，有效成员根据 dataType 字段而定

    assert sizeof(ZCANDataObj) == 100
    # class ZlgCanDataObj(Structure):                     # from zlgcan echo demo
    #     _pack_ = 1
    #     _fields_ = [("dataType", c_ubyte),              # can/canfd frame
    #                 ("chnl", c_ubyte),                  # can_channel
    #                 ("flag", c_ushort),                 # 标志信息, 暂未使用
    #                 ("extraData", c_ubyte * 4),         # 标志信息, 暂未使用
    #                 ("zcanfddata", ZlgCanFdData),       # 88个字节
    #                 ("reserved", c_ubyte * 4)]

    class IProperty(Structure):  # IProperty
        _fields_ = [("SetValue", c_void_p),
                    ("GetValue", c_void_p),
                    ("GetPropertys", c_void_p)]

def _library_check_run(func_name, *args, **kwargs):
    ret = getattr(_library, func_name)(*args, **kwargs)
    if ret != ZCAN_STATUS_OK:
        raise ZCANException(f'ZLG: {func_name} failed!')
    return ret

class ZCAN(object):

    def __init__(self):
        if _library is None:
            raise ZCANException(
                "The ZLG-CAN driver could not be loaded. "
                "Check that you are using 32-bit/64bit Python on Windows or 64bit Python on Linux."
            )
        self._logger = logging.getLogger(self.__class__.__name__)
        self._dev_index = None
        self._dev_type = None
        # self._dev_type_name = None
        self._dev_info = None
        self._dev_is_canfd = None
        self._channels = ()
        # {'CAN': {chl_obj: is_canfd}, 'LIN': {chl_obj: is_master}}
        self._channel_handlers = {'CAN': [], 'LIN': []}
        if _is_windows:
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

    def _get_can_init_config(self, mode, filter, **kwargs):
        config = ZCAN_CHANNEL_INIT_CONFIG()
        if _is_windows:
            assert self._dev_is_canfd is not None, f'The device{self._dev_index} is not opened!'
            # clock = kwargs.get('clock', None)
            # if clock:
            #     self.SetValue()
            config.can_type = ZCANCanType.CANFD if self._dev_is_canfd else ZCANCanType.CAN
            acc_code = kwargs.get('acc_code', 0)
            acc_mask = kwargs.get('acc_mask', 0xFFFFFFFF)
            if self._dev_is_canfd:
                # USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI acc_code, acc_mask ignored
                if self._dev_type not in ZUSBCANFD_TYPE:
                    config.config.canfd.acc_code = acc_code
                    config.config.canfd.acc_mask = acc_mask
                config.config.canfd.abit_timing = kwargs.get('abit_timing', 104286)     # ignored
                config.config.canfd.dbit_timing = kwargs.get('dbit_timing', 8487694)    # ignored
                config.config.canfd.brp = kwargs.get('brp', 0)
                config.config.canfd.filter = filter
                config.config.canfd.mode = mode
                config.config.canfd.brp = kwargs.get('pad', 0)
            else:
                if self._dev_type in (ZCANDeviceType.ZCAN_PCI5010U, ZCANDeviceType.ZCAN_PCI5020U,
                                      ZCANDeviceType.ZCAN_USBCAN_E_U, ZCANDeviceType.ZCAN_USBCAN_2E_U,
                                      ZCANDeviceType.ZCAN_USBCAN_4E_U, ZCANDeviceType.ZCAN_CANDTU_200UR,
                                      ZCANDeviceType.ZCAN_CANDTU_MINI, ZCANDeviceType.ZCAN_CANDTU_NET,
                                      ZCANDeviceType.ZCAN_CANDTU_100UR, ZCANDeviceType.ZCAN_CANDTU_NET_400):
                    config.config.can.acc_code = acc_code
                    config.config.can.acc_mask = acc_mask
                config.config.can.filter = filter
                if self._dev_type in ZUSBCAN_I_II_TYPE:
                    config.config.can.timing0 = kwargs.get('timing0', 0)                   # ignored
                    config.config.can.timing1 = kwargs.get('timing0', 28)                  # ignored
                config.config.can.mode = mode
        elif _is_linux:
            clock = kwargs.get('clock', None)
            arb_seg1 = kwargs.get('arb_seg1', None)
            arb_seg2 = kwargs.get('arb_seg2', None)
            arb_sjw = kwargs.get('arb_sjw', None)
            arb_smp = kwargs.get('arb_smp', 0)
            arb_brp = kwargs.get('arb_brp', None)
            data_seg1 = kwargs.get('data_seg1', arb_seg1)
            data_seg2 = kwargs.get('data_seg2', arb_seg2)
            data_sjw = kwargs.get('data_sjw', arb_sjw)
            data_smp = kwargs.get('data_smp', arb_smp)
            data_brp = kwargs.get('data_brp', arb_brp)
            assert clock is not None \
                and arb_seg1 is not None and arb_seg2 is not None and arb_sjw is not None and arb_smp is not None \
                and arb_brp is not None
            config.mode = mode
            config.clk = clock
            config.aset.tseg1 = arb_seg1
            config.aset.tseg2 = arb_seg2
            config.aset.sjw = arb_sjw
            config.aset.smp = arb_smp
            config.aset.brp = arb_brp
            config.dset.tseg1 = data_seg1
            config.dset.tseg2 = data_seg2
            config.dset.sjw = data_sjw
            config.dset.smp = data_smp
            config.dset.brp = data_brp
        return config

    def _get_channel_handler(self, chl_type, channel):
        channels = self._channel_handlers[chl_type]
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

    def ResistanceStatus(self, channel, status=None):
        if _is_windows:
            if status is not None:
                self.SetValue(channel, initenal_resistance=status)
            return self.GetValue(channel, 'initenal_resistance')
        elif _is_linux:
            warnings.warn('ZLG: Cant get the resistance status in Linux.')
            if status is not None:
                _library_check_run('VCI_SetReference', 
                                   self._dev_type, self._dev_index, channel,
                                   CMD_CAN_RES, byref(c_int32(status)))      # TODO 不使用结构体行不行

    def SetFilters(self, channel, filters=None):
        if _is_windows:
            if filters is None:
                return self.SetValue(channel, filter_clear=0)
            if len(filters) > 64:
                filters = filters[:64]
            for _filter in filters:
                mode = _filter[0]
                start = _filter[1]
                end = _filter[2]
                self.SetValue(channel, filter_mode=mode, filter_start=start, filter_end=end)
        elif _is_linux:
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
            _library_check_run('VCI_SetReference',
                               self._dev_index, channel, CMD_CAN_FILTER, byref(_filter))

    # DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
    def OpenDevice(self, dev_type: ZCANDeviceType, dev_index=0, reserved=0):
        if _is_windows:
            ret = _library.ZCAN_OpenDevice(dev_type, dev_index, reserved)
            if ret == INVALID_DEVICE_HANDLE:
                raise ZCANException('ZLG: ZCAN_OpenDevice failed!')
            self._dev_handler = ret
        elif _is_linux:
            self._dev_handler = _library_check_run('VCI_OpenDevice',
                                                   dev_type, dev_index, reserved)
        self._dev_index = dev_index
        self._dev_type = dev_type
        # matched = re.findall(r'[.](\w*?),', inspect.getframeinfo(inspect.currentframe().f_back)[3][0])
        # assert len(matched) > 0
        # self._dev_type_name = matched[0]
        self._dev_info = self.GetDeviceInf()
        channels = self._dev_info.can_num
        self._channels = tuple(i for i in range(channels))
        self._dev_is_canfd = 'CANFD' in self._dev_info.hw_type

    # UINT FUNC_CALL ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
    def CloseDevice(self):
        can_channels = self._channel_handlers['CAN']
        lin_channels = self._channel_handlers['LIN']
        for index, _ in enumerate(can_channels):
            self.ResetCAN(index)
        for index, _ in enumerate(lin_channels):
            self.ResetLIN(index)
        if _is_windows:
            _library_check_run('ZCAN_CloseDevice', self._dev_handler)
            self._dev_handler = None
        elif _is_linux:
            for channel in self._channels:
                self.ResetCAN(channel)
            _library_check_run('VCI_CloseDevice', self._dev_type, self._dev_index)
        can_channels.clear()
        lin_channels.clear()

    # UINT FUNC_CALL ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);
    def GetDeviceInf(self) -> ZCAN_DEVICE_INFO:
        dev_info = ZCAN_DEVICE_INFO()
        if _is_windows:
            _library_check_run('ZCAN_GetDeviceInf', self._dev_handler, byref(dev_info))
            return dev_info
        elif _is_linux:
            _library_check_run('VCI_ReadBoardInfo',
                               self._dev_type, self._dev_type, byref(dev_info))
            return dev_info

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
        config = self._get_can_init_config(mode, filter, **kwargs)
        if _is_windows:
            clock = kwargs.get('clock', None)
            if clock:
                self.SetValue(channel, clock=clock)
            ret = _library.ZCAN_InitCAN(self._dev_handler, channel, byref(config))
            if ret == INVALID_CHANNEL_HANDLE:
                raise ZCANException('ZLG: ZCAN_InitCAN failed!')
            self._channel_handlers['CAN'].append(ret)
        elif _is_linux:
            _library_check_run('VCI_InitCAN', self._dev_type, self._dev_index, channel, byref(config))
            self._channel_handlers['CAN'].append(channel)

    # UINT FUNC_CALL ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
    def StartCAN(self, channel):
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            _library_check_run('ZCAN_StartCAN', handler)
        elif _is_linux:
            _library_check_run('VCI_StartCAN', self._dev_type, self._dev_index, channel)

    # UINT FUNC_CALL ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
    def ResetCAN(self, channel):
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            _library_check_run('ZCAN_ResetCAN', handler)
        elif _is_linux:
            _library_check_run('VCI_ResetCAN', self._dev_type, self._dev_type, channel)

    # UINT FUNC_CALL ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
    def ClearBuffer(self, channel):
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            _library_check_run('ZCAN_ClearBuffer', handler)
        elif _is_linux:
            _library_check_run('VCI_ClearBuffer', self._dev_type, self._dev_index)

    # UINT FUNC_CALL ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        error_info = ZCAN_CHANNEL_ERR_INFO()
        if _is_windows:
            handler = self._get_channel_handler(chl_type, channel)
            # TODO 统一
            _library_check_run('ZCAN_ReadChannelErrInfo', handler, byref(error_info))
            return error_info
        elif _is_linux:
            # TODO 统一
            _library_check_run('VCI_ReadErrInfo',
                               self._dev_type, self._dev_info, byref(error_info))
            return error_info

    # UINT FUNC_CALL ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        warnings.warn('ZLG: no device supported.', DeprecationWarning, 2)
        status_info = ZCAN_CHANNEL_STATUS()
        if _is_windows:
            handler = self._get_channel_handler(chl_type, channel)
            # TODO 统一
            _library_check_run('ZCAN_ReadChannelStatus', handler, byref(status_info))
            return status_info
        elif _is_linux:
            _library_check_run('VCI_ReadCANStatus',
                               self._dev_type, self._dev_index, byref(status_info))
            return status_info

    # UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
    # UINT FUNC_CALL ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
    def GetReceiveNum(self, channel, msg_type: ZCANMessageType = ZCANMessageType.CAN):
        """
        获取指定通道已经接收到消息数量
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msg_type: 消息类型: 0 - CAN; 1 - CANFD; '-1' - LIN
        :return: 消息数量
        """
        if _is_windows:
            if msg_type == ZCANMessageType.LIN:
                return _library.ZCAN_GetLINReceiveNum(self._get_channel_handler('LIN', channel))
            return _library.ZCAN_GetReceiveNum(self._get_channel_handler('CAN', channel), msg_type)
        elif _is_linux:
            port = 0x00000000
            if msg_type == ZCANMessageType.CANFD:
                port |= 0x80000000
            return _library.VCI_GetReceiveNum(self._dev_type, self._dev_index, (port | channel))

    # UINT FUNC_CALL ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
    def TransmitFD(self, channel, msgs, size=None):
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            _size = size or len(msgs)
            ret = _library.ZCAN_TransmitFD(handler, byref(msgs), _size)
            self._logger.debug(f'ZLG: Transmit ZCAN_TransmitFD_Data expect: {_size}, actual: {ret}')
            return ret
        elif _is_linux:
            _size = size or len(msgs)
            ret = _library.VCI_TransmitFD(self._dev_type, self._dev_index, channel, byref(msgs), _size)
            self._logger.debug(f'ZLG: Transmit ZCAN_CANFD_FRAME expect: {_size}, actual: {ret}')
            return ret

    # UINT FUNC_CALL ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int timeout DEF(-1));
    def ReceiveFD(self, channel, size=1, timeout=-1):
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            can_msgs = (ZCAN_ReceiveFD_Data * size)()
            ret = _library.ZCAN_ReceiveFD(handler, byref(can_msgs), size, timeout)
            self._logger.debug(f'ZLG: Receive ZCAN_ReceiveFD_Data expect: {size}, actual: {ret}')
            for i in range(ret):
                yield can_msgs[i]
        elif _is_linux:
            can_msgs = (ZCAN_CANFD_FRAME * size)()
            ret = _library.VCI_ReceiveFD(self._dev_type, self._dev_index, channel, byref(can_msgs), size)
            self._logger.debug(f'ZLG: Receive ZCAN_CANFD_FRAME expect: {size}, actual: {ret}')
            for i in range(ret):
                yield can_msgs[i]

    # # UINT FUNC_CALL ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
    def Transmit(self, channel, msgs, size=None):
        """
        发送CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msgs: 消息报文
        :param size: 报文大小
        :return: 实际发送报文长度
        """
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            _size = size or len(msgs)
            ret = _library.ZCAN_Transmit(handler, byref(msgs), _size)
            self._logger.debug(f'ZLG: Transmit ZCAN_Transmit_Data expect: {_size}, actual: {ret}')
            return ret
        elif _is_linux:
            _size = size or len(msgs)
            ret = _library.VCI_Transmit(self._dev_type, self._dev_index, channel, byref(msgs), _size)
            self._logger.debug(f'ZLG: Transmit ZCAN_CAN_FRAME expect: {_size}, actual: {ret}')
            return ret

    # UINT FUNC_CALL ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
    def Receive(self, channel, size=1, timeout=-1):
        """
        接收CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param size: 期待接收报文个数
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        if _is_windows:
            handler = self._get_channel_handler('CAN', channel)
            can_msgs = (ZCAN_Receive_Data * size)()
            ret = _library.ZCAN_Receive(handler, byref(can_msgs), size, timeout)
            for i in range(ret):
                yield can_msgs[i]
        elif _is_linux:
            can_msgs = (ZCAN_CAN_FRAME * size)()
            ret = _library.VCI_Receive(self._dev_type, self._dev_index, channel, byref(can_msgs), size)
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
        if _is_windows:
            prop = self.GetIProperty()
            func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
            func1 = CFUNCTYPE(c_uint, c_char_p, c_void_p)(prop.contents.SetValue)
            try:
                ret = func(c_char_p(f'{channel}/clear_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
                if ret != ZCAN_STATUS_OK:
                    raise ZCANException(f'ZLG: Set {channel}/clear_auto_send failed!')
                if interval_msgs:
                    if len(interval_msgs) > 8:
                        interval_msgs = interval_msgs[:8]
                    for index, msg_dict in enumerate(interval_msgs):
                        is_fd = False
                        msg = msg_dict.get('msg')
                        if isinstance(msg, ZCAN_Transmit_Data):
                            data = ZCAN_AUTO_TRANSMIT_OBJ()
                        elif isinstance(msg, ZCAN_TransmitFD_Data):
                            data = ZCANFD_AUTO_TRANSMIT_OBJ()
                            is_fd = True
                        else:
                            raise ZCANException(f'ZLG: Unsupported message type {type(msg)}')
                        data.enable = msg_dict.get('enable', 0)
                        data.index = msg_dict.get('index', index)
                        data.interval = msg_dict.get('interval', 0)
                        data.obj.transmit_type = msg_dict.get('trans_type', 0)
                        data.obj.frame = msg
                        ret = func1(c_char_p(f'{channel}/auto_send{"fd" if is_fd else ""}'.encode("utf-8")),
                                    cast(byref(data), c_void_p))
                        if ret != ZCAN_STATUS_OK:
                            raise ZCANException(f'ZLG: Set {channel} auto transmit object failed!')
                        delay = msg_dict.get('delay', None)
                        if delay:
                            delay_param = ZCAN_AUTO_TRANSMIT_OBJ_PARAM()
                            delay_param.index = msg_dict.get('index', index)
                            delay_param.type = 1
                            delay_param.value = delay
                            ret = func1(c_char_p(f'{channel}/auto_send_param'.encode("utf-8")),
                                        cast(byref(delay_param), c_void_p))
                            if ret != ZCAN_STATUS_OK:
                                raise ZCANException(f'ZLG: Set {channel} auto transmit object param failed!')

                        ret = func(c_char_p(f'{channel}/apply_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
                        if ret != ZCAN_STATUS_OK:
                            raise ZCANException(f'ZLG: Set {channel}/apply_auto_send failed!')
            finally:
                self.ReleaseIProperty(prop)
        elif _is_linux:
            # TODO 清空自动发送列表(怎么做)
            _library_check_run('VCI_SetReference',
                               self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND_STATUS,
                               byref(c_int32(0)))           # TODO 不使用结构体行不行
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
                _library_check_run('VCI_SetReference',
                                   self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND, byref(table))
                _library_check_run('VCI_SetReference',
                                   self._dev_type, self._dev_index, channel, CMD_CAN_SKD_SEND_STATUS,
                                   byref(c_int32(1)))       # TODO 不使用结构体行不行

    if _is_linux:
        def Debug(self, level):
            _library_check_run('VCI_Debug', level)

    if _is_windows:
        # UINT FUNC_CALL ZCAN_SetValue(DEVICE_HANDLE device_handle, const char* path, const void* value);
        def SetValue(self, channel, **kwargs):
            """
            设置通道波特率/时钟频率/终端电阻使能等属性信息
            :param channel: 通道号, 范围 0 ~ 通道数-1
            :param kwargs: 其他关键字参数/字典:
| 名称                              | 参数功能                             | 值说明                                                                              | 默认值                   | 时机                     | 备注                                                                  |
|---------------------------------|----------------------------------|----------------------------------------------------------------------------------|-----------------------|------------------------|---------------------------------------------------------------------|
| canfd_standard                  | 设置协议类型                           | 0 – CANFD ISO <br/> 1 – CANFD Non-ISO                                            | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用USBCANFD-100U 、USBCANFD-200U 、USBCANFD-MINI 设备                    |
| protocol                        | 设置协议类型                           | 0 – CAN <br/> 1 – CANFD ISO <br/> 2 – CANFD Non-ISO                              | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用 USBCANFD-800U 设备                                                 |
| clock                           | 设置时钟频率, 直接影响波特率                  | 不同设备支持的时钟频率不同                                                                    | 上一次设置值                | 在设置波特率之前               |                                                                     |
| canfd_abit_baud_rate            | 设置仲裁域波特率                         | 1000000,800000,500000, <br/> 250000,125000,100000,50000                          | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| canfd_dbit_baud_rate            | 设置数据域波特率                         | 5000000,4000000,2000000, <br/> 1000000,800000,500000, <br/> 250000,125000,100000 | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| baud_rate_custom                | 设置自定义波特率                         | 需计算                                                                              | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| initenal_resistance             | 设置终端电阻                           | 0 - 禁能 <br/> 1 - 使能                                                              | 上一次设置值                | 需在 init_channel 之后设置   |                                                                     |
| tx_timeout                      | 设置发送超时时间                         | 0 ~ 4000 ms                                                                      |                       |                        | 只适用 100U/200U/MINI/设备、不适用 USBCANFD-800U                             |
| auto_send                       | 设置定时发送CAN 帧                      |                                                                                  |                       | 需在 start_channel 之后设置  |                                                                     |
| auto_send_canfd                 | 设置定时发送 CANFD 帧                   |                                                                                  |                       | 需在 start_channel 之后设置  | USBCANFD 支持每通道最大 100 条定时发送列表（USBCANFD-800U 支持每通道最大 32条定时发送列表）       |
| auto_send_param                 | 定时发送附加参数（用于设定特定索引定时发送帧的延时启动）     |                                                                                  | 需在 start_channel 之后设置 | 需在 start_channel 之后设置  | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| clear_auto_send                 | 清空定时发送                           | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| apply_auto_send                 | 应用定时发送（使能定时发送属性设置）               | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| set_send_mode                   | 设置设备发送模式                         | 0 – 正常模式 <br/> 1 – 队列模式                                                          | 0 正常模式                |                        | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| get_device_available_tx_count/1 | 获取发送队列可用缓存数量（仅队列模式）              | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| clear_delay_send_queue          | 清空发送缓存（仅队列模式，缓存中未发送的帧将被清空，停止时使用） | 0 - 固定值                                                                          |                       |                        |                                                                     |
| set_device_recv_merge           | 设置合并接收功能开启/关闭                    | 0 – 关闭合并接收功能 <br/> 1 – 开启合并接收功能                                                  | 0 – 关闭合并接收功能          |                        |                                                                     |
| get_device_recv_merge/1         | 获取设备当前是否开启了合并接收                  | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| set_cn                          | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备                    |
| set_name                        | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-800U 设备                                                 |
| get_cn/1                        | 获取自定义序列号                         | 无                                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备, 后面的 1 必须，也可以是任意数字 |
| get_name/1                      | 获取自定义序列号                         |                                                                                  |                       |                        | 适用 USBCANFD-800U 设备, 后面的 1 必须，也可以是任意数字                              |
| filter_mode                     | 设置滤波模式                           | 0 – 标准帧 <br/> 1 – 扩展帧                                                            |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_start                    | 设置滤波起始帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_end                      | 设置滤波结束帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_ack                      | 滤波生效（全部滤波 ID 同时生效）               | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_clear                    | 清除滤波                             | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| set_bus_usage_enable            | 设置总线利用率信息上报开关                    | 0 - 禁能 <br/> 1 - 使能                                                              |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| set_bus_usage_period            | 设置总线利用率信息上报周期                    | 20 ~ 2000 ms                                                                     |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| get_bus_usage/1                 | 获取总线利用率信息                        | 无                                                                                |                       | 	需在 start_channel 之后获取 | 只适用 USBCANFD-800U 设备, 最后的数字“1”只是内部标志，可以是任意数字                        |
| set_tx_retry_policy             | 设置发送失败时重试策略                      | 0 – 发送失败不重传 <br/> 1 -发送失败重传，直到总线关闭                                               |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备，其他 USBCANFD 设备通过设置工作模式来写入属性                    |

            :return: None
            """
            prop = self.GetIProperty()
            try:
                for path, value in kwargs.items():
                    func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
                    # _path = f'{channel}/{path}' if channel else f'{path}'
                    ret = func(c_char_p(_path(channel, path).encode("utf-8")), c_char_p(f'{value}'.encode("utf-8")))
                    if ret != ZCAN_STATUS_OK:
                        raise ZCANException(f'ZLG: Set channel{channel} property: {path} = {value} failed, code {ret}!')
                    self._logger.debug(f'ZLG: Set channel{channel} property: {path} = {value} success.')
                    assert str(value) == self.GetValue(channel, path, prop)
            finally:
                self.ReleaseIProperty(prop)

        # const void* FUNC_CALL ZCAN_GetValue(DEVICE_HANDLE device_handle, const char* path);
        def GetValue(self, channel, path, prop=None) -> str:
            """
            获取属性值
            :param channel: 通道号, 范围 0 ~ 通道数-1
            :param path: 参考zlg_set_properties说明中的字典参数
            :param prop: 属性对象, None即可(内部调用使用)
            :return: 属性值
            """
            _prop = prop or self.GetIProperty()
            try:
                func = CFUNCTYPE(c_char_p, c_char_p)(_prop.contents.GetValue)
                # _path = f'{channel}/{path}' if channel else f'{path}'
                ret = func(c_char_p(_path(channel, path).encode("utf-8")))
                if ret:
                    return ret.decode('utf-8')
            finally:
                if not prop:
                    self.ReleaseIProperty(_prop)

        def MergeEnabled(self):
            """
            设备是否开启合并收发模式
            :return: True if enabled else False
            """
            return self.GetValue(None, 'get_device_recv_merge/1') is not None

        # UINT FUNC_CALL ZCAN_TransmitData(DEVICE_HANDLE device_handle, ZCANDataObj* pTransmit, UINT len);
        def TransmitData(self, msgs, size=None):
            """
            合并发送数据[只有在设备支持合并发送功能并开启合并发送功能后才可以正常的发送到各种数据]
            :param msgs: 消息内容
            :param size: 消息长度
            :return: 实际发送的消息长度
            """
            self._merge_support()
            _size = size or len(msgs)
            ret = _library.ZCAN_TransmitData(self._dev_handler, byref(msgs), _size)
            self._logger.debug(f'ZLG: Transmit ZCANDataObj expect: {_size}, actual: {ret}')
            return ret

        # UINT FUNC_CALL ZCAN_ReceiveData(DEVICE_HANDLE device_handle, ZCANDataObj* pReceive, UINT len, int wait_time DEF(-1));
        def ReceiveData(self, size=1, timeout=-1):
            """
            合并接收数据[只有在设备支持合并接收功能并开启合并接收功能后才可以正常的接收到各种数据]
            :param size: 期待接收的数据大小
            :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
            :return: 消息内容及消息实际长度
            """
            # warnings.warn('ZLG: Library not support.', DeprecationWarning, 2)
            # self.zlg_get_property()
            self._merge_support()
            if not self.MergeEnabled():
                raise ZCANException('ZLG: device merge receive is not enable!')
            msgs = (ZCANDataObj * size)()
            ret = _library.ZCAN_ReceiveData(self._dev_handler, byref(msgs), size, c_int(timeout))
            self._logger.debug(f'ZLG: Received {ret} ZCANDataObj messages.')
            return msgs, ret

        # IProperty* FUNC_CALL GetIProperty(DEVICE_HANDLE device_handle);
        def GetIProperty(self):
            _library.GetIProperty.restype = POINTER(IProperty)
            return _library.GetIProperty(self._dev_handler)

        # UINT FUNC_CALL ReleaseIProperty(IProperty * pIProperty);
        def ReleaseIProperty(self, prop: IProperty):
            return _library.ReleaseIProperty(prop)

        # UINT FUNC_CALL ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);
        def DeviceOnLine(self):
            ret = _library.ZCAN_IsDeviceOnLine(self._dev_handler)
            self._logger.debug(f'ZLG: get device is online return code: {ret}.')
            return ret == ZCAN_STATUS_ONLINE

        # void FUNC_CALL ZCLOUD_SetServerInfo(const char* httpSvr, unsigned short httpPort, const char* authSvr, unsigned short authPort);
        def SetServerInfo(self, auth_host: str, auth_port, data_host=None, data_post=None):
            _library_check_run('ZCLOUD_SetServerInfo',
                               c_char_p(auth_host.encode('utf-8')), c_ushort(auth_port),
                               c_char_p((data_host or auth_host).encode('utf-8')),
                               c_ushort(data_post or auth_port))

        # // return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt connection error, 5:no device
        # UINT FUNC_CALL ZCLOUD_ConnectServer(const char* username, const char* password);
        def ConnectServer(self, username, password):
            ret = _library.ZCLOUD_ConnectServer(c_char_p(username.encode('utf-8')), c_char_p(password.encode('utf-8')))
            if ret == 0:
                return
            elif ret == 1:
                raise ZCANException('ZLG: connect server failure')
            elif ret == 2:
                raise ZCANException('ZLG: connect server https error')
            elif ret == 3:
                raise ZCANException('ZLG: connect server user login info error')
            elif ret == 4:
                raise ZCANException('ZLG: connect server mqtt connection error')
            elif ret == 5:
                raise ZCANException('ZLG: connect server no device')
            else:
                raise ZCANException(f'ZLG: connect server undefined error: {ret}')

        # bool FUNC_CALL ZCLOUD_IsConnected();
        def CloudConnected(self):
            return _library.ZCLOUD_IsConnected()

        # // return 0:success, 1:failure
        # UINT FUNC_CALL ZCLOUD_DisconnectServer();
        def DisconnectServer(self):
            ret = _library.ZCLOUD_IsConnected()
            return ret == 0

        # const ZCLOUD_USER_DATA* FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
        def GetUserData(self, userid) -> ZCLOUD_USER_DATA:
            return _library.ZCLOUD_GetUserData(userid)

        # UINT FUNC_CALL ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));
        def ReceiveGPS(self, size=1, timeout=-1):
            msgs = (ZCLOUD_GPS_FRAME * size)()
            ret = _library.ZCLOUD_ReceiveGPS(self._dev_handler, byref(msgs), size, timeout)
            self._logger.debug(f'ZLG: Master Transmit ZCLOUD_GPS_FRAME expect: {size}, actual: {ret}')
            return msgs, ret

        # CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT can_index, PZCAN_LIN_INIT_CONFIG pLINInitConfig);
        def InitLIN(self, channel, config: ZCAN_LIN_INIT_CONFIG):
            ret = _library.ZCAN_InitLIN(self._dev_handler, channel, byref(config))
            if ret == INVALID_CHANNEL_HANDLE:
                raise ZCANException('ZLG: ZCAN_InitLIN failed!')
            self._channel_handlers['LIN'][ret] = True

        # UINT FUNC_CALL ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
        def StartLIN(self, channel):
            handler = self._get_channel_handler('LIN', channel)
            _library_check_run('ZCAN_StartLIN', handler)

        # UINT FUNC_CALL ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
        def ResetLIN(self, channel):
            handler = self._get_channel_handler('LIN', channel)
            _library_check_run('ZCAN_ResetLIN', handler)

        # UINT FUNC_CALL ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
        def TransmitLIN(self, channel, msgs, size=None):
            handler = self._get_channel_handler('LIN', channel)
            _size = size or len(msgs)
            ret = _library.ZCAN_TransmitLIN(handler, byref(msgs), _size)
            self._logger.debug(f'ZLG: Master Transmit ZCAN_LIN_MSG expect: {_size}, actual: {ret}')
            return ret

        # UINT FUNC_CALL ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len,int WaitTime);
        def ReceiveLIN(self, channel, size=1, timeout=-1):
            msgs = (ZCAN_LIN_MSG * size)()
            handler = self._get_channel_handler('LIN', channel)
            ret = _library.ZCAN_ReceiveLIN(handler, byref(msgs), size, c_int(timeout))
            self._logger.debug(f'ZLG: Master Received {ret} ZCAN_LIN_MSG messages')
            return msgs, ret

        # UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
        def SetLINSlaveMsg(self, channel, msgs):
            handler = self._get_channel_handler('LIN', channel)
            ret = _library.ZCAN_SetLINSlaveMsg(handler, byref(msgs), len(msgs))
            self._logger.debug(f'ZLG: Slave Transmit {ret} ZCAN_LIN_MSG messages')
            return ret

        # UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE* pLINID, UINT nIDCount);
        def ClearLINSlaveMsg(self, channel, lin_ids):
            handler = self._get_channel_handler('LIN', channel)
            _library_check_run('ZCAN_ClearLINSlaveMsg', handler, byref(lin_ids), len(lin_ids))










