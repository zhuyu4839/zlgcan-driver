"""
the type of ZLG-CAN that defined
"""
__all__ = [
    "ZCAN_DEVICE_TYPE", "ZCAN_DEVICE_INDEX", "ZCANDeviceType", "ZCANCanType", "ZCANCanTransType", "ZCANCanFilter",
    "ZCANMessageType", "ZCANCanFdStd", "ZCANProtocol", "ZCANCanMode",
    "ZCAN_RESISTANCE_NOT_SUPPORT", "ZUSBCANFD_TYPE", "ZUSBCAN_XE_U_TYPE", "ZUSBCAN_I_II_TYPE", "ZCAN_MERGE_SUPPORT_TYPE"
]

from ctypes import c_uint

ZCAN_DEVICE_TYPE = c_uint
ZCAN_DEVICE_INDEX = c_uint


class ZCANDeviceType:
    ZCAN_PCI5121                       = 1
    ZCAN_PCI9810                       = 2
    ZCAN_USBCAN1                       = 3
    ZCAN_USBCAN2                       = 4
    ZCAN_PCI9820                       = 5
    ZCAN_CAN232                        = 6
    ZCAN_PCI5110                       = 7
    ZCAN_CANLITE                       = 8
    ZCAN_ISA9620                       = 9
    ZCAN_ISA5420                       = 10
    ZCAN_PC104CAN                      = 11
    ZCAN_CANETUDP                      = 12
    ZCAN_CANETE                        = 12
    ZCAN_DNP9810                       = 13
    ZCAN_PCI9840                       = 14
    ZCAN_PC104CAN2                     = 15
    ZCAN_PCI9820I                      = 16
    ZCAN_CANETTCP                      = 17
    ZCAN_PCIE_9220                     = 18
    ZCAN_PCI5010U                      = 19
    ZCAN_USBCAN_E_U                    = 20
    ZCAN_USBCAN_2E_U                   = 21
    ZCAN_PCI5020U                      = 22
    ZCAN_EG20T_CAN                     = 23
    ZCAN_PCIE9221                      = 24
    ZCAN_WIFICAN_TCP                   = 25
    ZCAN_WIFICAN_UDP                   = 26
    ZCAN_PCIe9120                      = 27
    ZCAN_PCIe9110                      = 28
    ZCAN_PCIe9140                      = 29
    ZCAN_USBCAN_4E_U                   = 31
    ZCAN_CANDTU_200UR                  = 32
    ZCAN_CANDTU_MINI                   = 33
    ZCAN_USBCAN_8E_U                   = 34
    ZCAN_CANREPLAY                     = 35
    ZCAN_CANDTU_NET                    = 36
    ZCAN_CANDTU_100UR                  = 37
    ZCAN_PCIE_CANFD_100U               = 38
    ZCAN_PCIE_CANFD_200U               = 39
    ZCAN_PCIE_CANFD_400U               = 40
    ZCAN_USBCANFD_200U                 = 41
    ZCAN_USBCANFD_100U                 = 42
    ZCAN_USBCANFD_MINI                 = 43
    ZCAN_CANFDCOM_100IE                = 44
    ZCAN_CANSCOPE                      = 45
    ZCAN_CLOUD                         = 46
    ZCAN_CANDTU_NET_400                = 47
    ZCAN_CANFDNET_TCP                  = 48
    ZCAN_CANFDNET_200U_TCP             = 48
    ZCAN_CANFDNET_UDP                  = 49
    ZCAN_CANFDNET_200U_UDP             = 49
    ZCAN_CANFDWIFI_TCP                 = 50
    ZCAN_CANFDWIFI_100U_TCP            = 50
    ZCAN_CANFDWIFI_UDP                 = 51
    ZCAN_CANFDWIFI_100U_UDP            = 51
    ZCAN_CANFDNET_400U_TCP             = 52
    ZCAN_CANFDNET_400U_UDP             = 53
    ZCAN_CANFDBLUE_200U                = 54
    ZCAN_CANFDNET_100U_TCP             = 55
    ZCAN_CANFDNET_100U_UDP             = 56
    ZCAN_CANFDNET_800U_TCP             = 57
    ZCAN_CANFDNET_800U_UDP             = 58
    ZCAN_USBCANFD_800U                 = 59
    ZCAN_PCIE_CANFD_100U_EX            = 60
    ZCAN_PCIE_CANFD_400U_EX            = 61
    ZCAN_PCIE_CANFD_200U_MINI          = 62
    ZCAN_PCIE_CANFD_200U_M2            = 63
    ZCAN_CANFDDTU_400_TCP              = 64
    ZCAN_CANFDDTU_400_UDP              = 65
    ZCAN_CANFDWIFI_200U_TCP            = 66
    ZCAN_CANFDWIFI_200U_UDP            = 67
    ZCAN_CANFDDTU_800ER_TCP            = 68
    ZCAN_CANFDDTU_800ER_UDP            = 69
    ZCAN_CANFDDTU_800EWGR_TCP          = 70
    ZCAN_CANFDDTU_800EWGR_UDP          = 71
    ZCAN_CANFDDTU_600EWGR_TCP          = 72
    ZCAN_CANFDDTU_600EWGR_UDP          = 73

    ZCAN_OFFLINE_DEVICE                = 98
    ZCAN_VIRTUAL_DEVICE                = 99


ZUSBCANFD_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U, ZCANDeviceType.ZCAN_USBCANFD_100U,
                  ZCANDeviceType.ZCAN_USBCANFD_MINI, )
ZUSBCAN_XE_U_TYPE = (ZCANDeviceType.ZCAN_USBCAN_E_U, ZCANDeviceType.ZCAN_USBCAN_2E_U,
                     ZCANDeviceType.ZCAN_USBCAN_4E_U, )
ZUSBCAN_I_II_TYPE = (ZCANDeviceType.ZCAN_USBCAN1, ZCANDeviceType.ZCAN_USBCAN2, )
ZCAN_MERGE_SUPPORT_TYPE = (ZCANDeviceType.ZCAN_USBCANFD_200U, ZCANDeviceType.ZCAN_USBCANFD_100U,
                           ZCANDeviceType.ZCAN_USBCANFD_MINI, ZCANDeviceType.ZCAN_CANFDNET_TCP,
                           ZCANDeviceType.ZCAN_CANFDNET_UDP, ZCANDeviceType.ZCAN_CANFDNET_400U_TCP,
                           ZCANDeviceType.ZCAN_CANFDNET_400U_UDP, ZCANDeviceType.ZCAN_CANFDNET_100U_TCP,
                           ZCANDeviceType.ZCAN_CANFDNET_100U_UDP, ZCANDeviceType.ZCAN_CANFDNET_800U_TCP,
                           ZCANDeviceType.ZCAN_CANFDNET_800U_UDP, ZCANDeviceType.ZCAN_CANFDWIFI_TCP,
                           ZCANDeviceType.ZCAN_CANFDWIFI_UDP, ZCANDeviceType.ZCAN_CANFDDTU_400_TCP,
                           ZCANDeviceType.ZCAN_CANFDDTU_400_UDP,
                           ZCANDeviceType.ZCAN_PCIE_CANFD_100U_EX, ZCANDeviceType.ZCAN_PCIE_CANFD_400U_EX,
                           ZCANDeviceType.ZCAN_PCIE_CANFD_200U_MINI, ZCANDeviceType.ZCAN_PCIE_CANFD_200U_M2, )
ZCAN_SELF_TR_SUPPORT = (ZCANDeviceType.ZCAN_PCIE_CANFD_100U_EX, ZCANDeviceType.ZCAN_PCIE_CANFD_400U_EX,
                        ZCANDeviceType.ZCAN_PCIE_CANFD_200U_MINI, ZCANDeviceType.ZCAN_PCIE_CANFD_200U_M2, )
ZCAN_RESISTANCE_NOT_SUPPORT = (ZCANDeviceType.ZCAN_USBCAN1, ZCANDeviceType.ZCAN_USBCAN2, )  # 不支持终端电阻设置


class ZCANCanType:
    CAN = c_uint(0)
    CANFD = c_uint(1)


class ZCANCanTransType:
    NORMAL = 0              # 正常发送
    SINGLE = 1              # 单次发送
    SELF_SR = 2             # 自发自收
    SINGLE_SELF_SR = 3      # 单次自发自收


class ZCANCanFilter:
    SINGLE = 1
    DOUBLE = 0


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
