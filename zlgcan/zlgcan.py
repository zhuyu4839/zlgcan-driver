"""
by zhuyu4839@gmail.com
"""
import platform
from ._common import *

_os = platform.system()
if 'windows' in _os.lower():
    from .windows import _ZCANWindows as ZCAN
    from .windows import ZCAN_Transmit_Data
    from .windows import ZCAN_TransmitFD_Data
    from .windows import ZCAN_Receive_Data
    from .windows import ZCAN_ReceiveFD_Data
    from .windows import ZCANDataObj
    from . windows import ZCAN_CHANNEL_ERR_INFO, ZCAN_CHANNEL_STATUS, ZCAN_CHANNEL_INIT_CONFIG
elif 'linux' in _os.lower():
    from .linux import _ZCANLinux as ZCAN
    from .linux import ZCAN_CHANNEL_ERR_INFO, ZCAN_CHANNEL_STATUS, ZCAN_CHANNEL_INIT_CONFIG
else:
    raise ZCANException(f'ZLG: Unsupported platform: {_os}')










