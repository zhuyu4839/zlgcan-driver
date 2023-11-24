"""
by zhuyu4839@gmail.com
"""
from ._common import _os_name, _system_bit
from ._common import *

if 'windows' in _os_name.lower():
    from .windows import _ZCANWindows as ZCAN
    from .windows import ZCAN_Transmit_Data
    from .windows import ZCAN_TransmitFD_Data
    from .windows import ZCAN_Receive_Data
    from .windows import ZCAN_ReceiveFD_Data
    from .windows import ZCANDataObj
    from . windows import ZCAN_CHANNEL_ERR_INFO, ZCAN_CHANNEL_STATUS, ZCAN_CHANNEL_INIT_CONFIG
elif 'linux' in _os_name.lower():
    if _system_bit == "64bit":
        from .linux import _ZCANLinux as ZCAN
        from .linux import ZCAN_CHANNEL_ERR_INFO, ZCAN_CHANNEL_STATUS, ZCAN_CHANNEL_CAN_INIT_CONFIG, ZCAN_CHANNEL_CANFD_INIT_CONFIG
    else:
        raise ZCANException(
            "The ZLG-CAN driver only support 64bit Python on Linux."
        )
else:
    raise ZCANException(f'ZLG: Unsupported platform: {_os_name}')










