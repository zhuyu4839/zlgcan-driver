"""
by zhuyu4839@gmail.com

tools download: https://zlg.cn/can/down/down/id/22.html
description|driver|developer docs: https://manual.zlg.cn/web/#/42/1710
driver download: https://manual.zlg.cn/web/#/146
develop demo: https://manual.zlg.cn/web/#/152/5332
canfd develop reference(linux): https://manual.zlg.cn/web/#/188/6982

derive device: usb vendor id is 0471
"""
from zlgcan.codes import *
from zlgcan.exceptions import *
from zlgcan.types import *

from zlgcan.utils import _system_name

if _system_name == "windows":
    from zlgcan.structs.windows.cloud.gps import *
    from zlgcan.structs.windows.can import *
    from zlgcan.structs import *
    from zlgcan.structs import *
    from .drivers.windows import _ZCANWindows as ZCAN
elif _system_name == "linux":
    from zlgcan.structs import *
    from .drivers.linux import _ZCANLinux as ZCAN
else:
    raise ZCANException(f"ZLG: unsupported system: {_system_name}")
