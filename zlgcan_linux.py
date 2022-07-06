import logging
import platform
from enum import Enum
from ctypes import *


class ZlgException(Exception):
    pass


class ZlgCanTxMode(Enum):
    ZCAN_TX_NORM = 0,                           # /**< normal transmission */
    ZCAN_TX_ONCE = 1,                           # /**< single-shot transmission */
    ZCAN_SR_NORM = 2,                           # /**< self reception */
    ZCAN_SR_ONCE = 3,                           # /**< single-shot transmission & self reception */


# /** CAN filter configuration */
class ZlgCanFilter(Structure):
    _fields_ = [('type', c_uint8),              # /**< 0-std_frame, 1-ext_frame */
                ('pad', c_uint8 * 3),
                ('sid', c_uint32),              # /**< start-id */
                ('eid', c_uint32)]              # /**< end-id */


class _ZlgCanInitASet(Structure):
    _fields_ = [('tseg1', c_uint8),
                ('tseg2', c_uint8),
                ('sjw', c_uint8),
                ('smp', c_uint8),
                ('brp', c_uint16)]


class _ZlgCanInitDSet(Structure):
    _fields_ = [('tseg1', c_uint8),
                ('tseg2', c_uint8),
                ('sjw', c_uint8),
                ('smp', c_uint8),
                ('brp', c_uint16)]


# /** controller initialization */
class ZlgCanInit(Structure):
    _fields_ = [('clk', c_uint32),
                ('mode', c_uint32),
                ('aset', _ZlgCanInitASet),
                ('dset', _ZlgCanInitDSet)]


# /** CAN message info */
class ZlgCanMessageInfo(Structure):
    _fields_ = [('txm', c_uint32, 4),           # /**< TX-mode, @see ZCAN_TX_MODE */
                ('fmt', c_uint32, 4),           # /**< 0-CAN2.0, 1-CANFD */
                ('sdf', c_uint32, 1),           # /**< 0-data_frame, 1-remote_frame */
                ('sef', c_uint32, 1),           # /**< 0-std_frame, 1-ext_frame */
                ('err', c_uint32, 1),           # /**< error flag */
                ('brs', c_uint32, 1),           # /**< bit-rate switch */
                ('est', c_uint32, 1),           # /**< error state */
                ('pad', c_uint32, 19)]


# /** CAN message header */
class ZlgCanMessageHeader(Structure):
    _fields_ = [('ts', c_uint32),
                ('id', c_uint32),
                ('inf', ZlgCanMessageInfo),
                ('pad', c_uint16),
                ('chn', c_uint8),
                ('len', c_uint8)]


# /** CAN2.0-frame */
class ZlgCan20Frame(Structure):
    _fields_ = [('hdr', ZlgCanMessageHeader),
                ('dat', c_uint8 * 8)]


# /** CANFD-frame */
class ZlgCanFdFrame(Structure):
    _fields_ = [('hdr', ZlgCanMessageHeader),
                ('dat', c_uint8 * 64)]


# /** CANERR-frame */
class ZlgCanErrorFrame(Structure):
    _fields_ = [('hdr', ZlgCanMessageHeader),
                ('dat', c_uint8 * 64)]


# /** device info */
class ZlgDeviceInfo(Structure):
    _fields_ = [('hwv', c_uint16),          # /**< hardware version */
                ('fwv', c_uint16),          # /**< firmware version */
                ('drv', c_uint16),          # /**< driver version */
                ('api', c_uint16),          # /**< API version */
                ('irp', c_uint16),          # /**< IRQ */
                ('chn', c_uint8),           # /**< channels */
                ('sn', c_uint8 * 20),       # /**< serial number */
                ('id', c_uint8 * 40),       # /**< card id */
                ('pad', c_uint8 * 4)]


# /** controller status */
class ZlgDeviceStatus(Structure):
    _fields_ = [('IR', c_uint8),            # /**< not used(for backward compatibility) */
                ('MOD', c_uint8),           # /**< not used */
                ('SR', c_uint8),            # /**< not used */
                ('ALC', c_uint8),           # /**< not used */
                ('ECC', c_uint8),           # /**< not used */
                ('EWL', c_uint8),           # /**< not used */
                ('RXE', c_uint8),           # /**< RX errors */
                ('TXE', c_uint8),           # /**< TX errors */
                ('PAD', c_uint32)]


class ZlgDeviceLinux(object):

    def __init__(self, lib_path):
        self._logger = logging.getLogger(self.__class__.__name__)
        if platform.system() == "Linux":
            self.__dll = windll.LoadLibrary(lib_path)
        else:
            raise ZlgException("ZLG: No support now!")
        if self.__dll is None:
            raise ZlgException("ZLG: DLL couldn't be loaded!")
        self._dev_handler = None
        self._dev_index = 0
        self._dev_type = None
        self._channels = 0

    # EXTERN_C U32 ZCAN_API VCI_OpenDevice(U32 Type, U32 Card, U32 Reserved);
    def zlg_open_device(self, dev_type, dev_index=0, reserved=0):
        ret = self.__dll.VCI_OpenDevice(dev_type, dev_index, reserved)
        # if ret == INVALID_DEVICE_HANDLE:

    # EXTERN_C U32 ZCAN_API VCI_CloseDevice(U32 Type, U32 Card);
    def CloseDevice(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_InitCAN(U32 Type, U32 Card, U32 Port, ZCAN_INIT *pInit);
    def InitCAN(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_StartCAN(U32 Type, U32 Card, U32 Port);
    def StartCAN(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ReadBoardInfo(U32 Type, U32 Card, ZCAN_DEV_INF *pInfo);
    def GetDeviceInf(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ReadErrInfo(U32 Type, U32 Card, U32 Port, ZCAN_ERR_MSG *pErr);
    def ReadChannelErrInfo(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ReadCANStatus(U32 Type, U32 Card, U32 Port, ZCAN_STAT *pStat);
    def ReadChannelStatus(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_GetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def zlg_get_property(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_SetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    def zlg_set_property(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_GetReceiveNum(U32 Type, U32 Card, U32 Port);
    def GetReceiveNum(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ClearBuffer(U32 Type, U32 Card, U32 Port);
    def ClearBuffer(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ResetCAN(U32 Type, U32 Card, U32 Port);
    def ResetCAN(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_Transmit(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count);
    def Transmit(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_TransmitFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count);
    def TransmitFD(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_Receive(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count, U32 Time);
    def Receive(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_ReceiveFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count, U32 Time);
    def ReceiveFD(self):
        pass

    # EXTERN_C U32 ZCAN_API VCI_Debug(U32 Debug);
    def zlg_debug(self):
        pass




















