__all__ = [
    "ZCLOUD_GPS_FRAMETime", "ZCLOUD_GPS_FRAME", "ZCLOUD_CHNINFO", "ZCLOUD_DEVINFO", "ZCLOUD_USER_DATA",
]

from ctypes import Structure, c_ushort, c_float, c_ubyte, c_int, c_char, c_size_t

from ....codes import Cloud


class ZCLOUD_GPS_FRAMETime(Structure):
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
                ("tm", ZCLOUD_GPS_FRAMETime)]


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
                ("channels", ZCLOUD_CHNINFO * Cloud.ZCLOUD_MAX_CHANNEL)]


class ZCLOUD_USER_DATA(Structure):                          # ZCLOUD_USER_DATA
    _fields_ = [("username", c_char * 64),
                ("mobile", c_char * 64),
                ("dllVer", c_char * 16),
                ("devCnt", c_size_t),
                ("channels", ZCLOUD_DEVINFO * Cloud.ZCLOUD_MAX_DEVICES)]
