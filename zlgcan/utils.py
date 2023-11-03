import os.path
import platform

from .codes import Status
from .exceptions import ZCANException


_system_name = platform.system().lower()
_system_bit, _ = platform.architecture()
_current_path = os.path.dirname(__file__)
_library_path = os.path.join(_current_path, "library")


def _library_run(lib, func_name, *args, **kwargs):
    try:
        _ret = getattr(lib, func_name)(*args, **kwargs)
        if _ret == Status.ZCAN_STATUS_OK:
            return

        if _ret == Status.ZCAN_STATUS_ERR:
            raise ZCANException(f"ZLG: {func_name} execute error!")
        elif _ret == Status.ZCAN_STATUS_ONLINE:
            raise ZCANException(f"ZLG: {func_name} device is online!")
        elif _ret == Status.ZCAN_STATUS_OFFLINE:
            raise ZCANException(f"ZLG: {func_name} device is offline!")
        elif _ret == Status.ZCAN_STATUS_UNSUPPORTED:
            raise ZCANException(f"ZLG: {func_name} device is unsupported!")
        else:
            raise ZCANException(f"ZLG: {func_name} unknown error: {_ret}!")
    except AttributeError:
        raise ZCANException(f"ZLG: {func_name} has not supported by the library!")
