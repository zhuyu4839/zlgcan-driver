"""
by zhuyu4839@gmail.com
"""
from ._common import _os_name, _system_bit
from ._common import *

if 'windows' in _os_name.lower():
    from .windows import _ZCANWindows as ZCAN
elif 'linux' in _os_name.lower():
    if _system_bit == "64bit":
        from .linux import _ZCANLinux as ZCAN
    else:
        raise ZCANException(
            "The ZLG-CAN driver only support 64bit Python on Linux."
        )
else:
    raise ZCANException(f'ZLG: Unsupported platform: {_os_name}')










