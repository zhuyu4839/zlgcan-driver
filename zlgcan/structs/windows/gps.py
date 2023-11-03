__all__ = [
    "ZCANGPSDataTime", "ZCANGPSDataFlag", "ZCANGPSData",
]

from ctypes import Structure, c_ushort, c_float


class ZCANGPSDataTime(Structure):
    _pack_ = 1
    _fields_ = [("year", c_ushort),
                ("mon", c_ushort),
                ("day", c_ushort),
                ("hour", c_ushort),
                ("min", c_ushort),
                ("sec", c_ushort),
                ("milsec", c_ushort)]


class ZCANGPSDataFlag(Structure):
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
    _fields_ = [("time", ZCANGPSDataTime),
                ("flag", ZCANGPSDataFlag),
                ("latitude", c_float),              # 纬度 正数表示北纬, 负数表示南纬
                ("longitude", c_float),             # 经度 正数表示东经, 负数表示西经
                ("altitude", c_float),              # 海拔 单位: 米
                ("speed", c_float),                 # 速度 单位: km/h
                ("courseAngle", c_float)]           # 航向角
