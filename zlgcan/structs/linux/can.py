__all__ = [
    "ZCAN_CAN_FRAME", "ZCAN_CHANNEL_ERR_INFO", "ZCAN_CANFD_FRAME", "ZCAN_CAN_FRAME_I_II",
    "ZCAN_FILTER", "ZCAN_FILTER_TABLE",
    "ZCAN_CHANNEL_STATUS",
    "ZCAN_TTX", "ZCAN_TTX_TABLE",
    "ZCAN_CHANNEL_INIT_CONFIG_Union",
]

from ctypes import Structure, c_uint, c_ushort, c_ubyte, c_int, Union, c_uint32, c_uint8, c_byte


class _ZCANInitSet(Structure):
    _fields_ = [('tseg1', c_ubyte),
                ('tseg2', c_ubyte),
                ('sjw', c_ubyte),
                ('smp', c_ubyte),
                ('brp', c_ushort)]


class _ZCAN_MSG_INFO(Structure):
    _pack_ = 1
    _fields_ = [('mode', c_uint, 4),            # 发送方式，0为正常模式，2为自发自收（仅用于自测）
                ('is_fd', c_uint, 4),           # 0-CAN帧，1-CANFD帧
                ('is_remote', c_uint, 1),       # 0-数据帧，1-远程帧
                ('is_extend', c_uint, 1),       # 0-标准帧，1-扩展帧
                ('is_error', c_uint, 1),        # 0-正常帧，1-错误帧
                ('bsr', c_uint, 1),             # 0-CANFD不加速，1-CANFD加速(Bit Rate Switch)
                ('esi', c_uint, 1),             # 错误状态，0-积极错误，1-消极错误(Error State Indicator)
                ('pad', c_uint, 19)]


class _ZCAN_MSG_HEADER(Structure):
    _fields_ = [('timestamp', c_uint),  # timestamp
                ('id', c_uint),  # can id
                ('info', _ZCAN_MSG_INFO),  # msg info
                ('pad', c_ushort),  # reversed
                ('channel', c_ubyte),  # channel
                ('dlc', c_ubyte)]  # dlc


class ZCAN_FILTER(Structure):
    _fields_ = [('type', c_ubyte),  # /**< 0-std_frame, 1-ext_frame */
                ('pad', c_ubyte * 3),
                ('sid', c_uint),  # /**< start-id */
                ('eid', c_uint)]  # /**< end-id */


class ZCAN_FILTER_TABLE(Structure):
    _fields_ = [('size', c_uint),
                ('table', ZCAN_FILTER * 64)]


class ZCAN_CAN_FRAME(Structure):               # ZCAN_CAN_FRAME
    _fields_ = [('header', _ZCAN_MSG_HEADER),
                ('data', c_ubyte * 8)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_rx = False

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp:>15.6f} " \
               f"ID: {self.header.info.id:08x} " \
               f"{'X' if self.header.info.is_extend else 'S'} " \
               f"{'Rx' if self.is_rx else 'Tx'} " \
               f"{'E' if self.header.info.is_error else ' '} " \
               f"{'R' if self.is_remote else ' '} " \
               f"{'F' if self.header.info.is_fd else ' '} " \
               f"{'BS' if self.header.info.brs else ' '} " \
               f"{'EI' if self.header.info.esi else ' '} " \
               f"DL: {self.header.dlc:2d} " \
               f"{' '.join('%02x' % self.data[i] for i in range(min(self.header.dlc, len(self.data))))} " \
               f"Channel: {self.header.channel}"


class ZCAN_CAN_FRAME_I_II(Structure):
    _fields_ = [("id", c_uint32),
                ("timestamp", c_uint32),
                ("time_flag", c_uint8),
                ("mode", c_byte),
                ("is_remote", c_byte),            # remote frame
                ("is_extend", c_byte),            # extend frame
                ("dlc", c_byte),
                ("data", c_ubyte * 8),
                ("reserved", c_ubyte * 3)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.is_rx = False

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp:>15.6f} " \
               f"ID: {self.id:08x} " \
               f"{'X' if self.is_extend else 'S'} " \
               f"{'Rx' if self.is_rx else 'Tx'} " \
               f"  " \
               f"{'R' if self.is_remote else ' '} " \
               f"  " \
               f"  " \
               f"  " \
               f"DL: {self.dlc:2d} " \
               f"{' '.join('%02x' % self.data[i] for i in range(min(self.dlc, len(self.data))))} " \
               f"Channel: {self.channel}"


class ZCAN_CHANNEL_ERR_INFO(Structure):           # ZCAN_CHANNEL_ERR_INFO
    _fields_ = [('header', _ZCAN_MSG_HEADER),
                ('data', c_ubyte * 8)]


class ZCAN_CANFD_FRAME(Structure):             # ZCAN_CANFD_FRAME
    _fields_ = [('header', _ZCAN_MSG_HEADER),
                ('data', c_ubyte * 64)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_rx = False

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp:>15.6f} " \
               f"ID: {self.header.info.id:08x} " \
               f"{'X' if self.header.info.is_extend else 'S'} " \
               f"{'Rx' if self.is_rx else 'Tx'} " \
               f"{'E' if self.header.info.is_error else ' '} " \
               f"{'R' if self.is_remote else ' '} " \
               f"{'F' if self.header.info.is_fd else ' '} " \
               f"{'BS' if self.header.info.brs else ' '} " \
               f"{'EI' if self.header.info.esi else ' '} " \
               f"DL: {self.header.dlc:2d} " \
               f"{' '.join('%02x' % self.data[i] for i in range(min(self.header.dlc, len(self.data))))} " \
               f"Channel: {self.header.channel}"


class ZCAN_CHANNEL_STATUS(Structure):         # ZCAN_CHANNEL_STATUS
    _fields_ = [('IR', c_ubyte),                    # /**< not used(for backward compatibility) */
                ('MOD', c_ubyte),                   # /**< not used */
                ('SR', c_ubyte),                    # /**< not used */
                ('ALC', c_ubyte),                   # /**< not used */
                ('ECC', c_ubyte),                   # /**< not used */
                ('EWL', c_ubyte),                   # /**< not used */
                ('RXE', c_ubyte),                   # /**< RX errors */
                ('TXE', c_ubyte),                   # /**< TX errors */
                ('PAD', c_uint)]


class ZCAN_TTX(Structure):
    _fields_ = [('interval', c_uint),               # 定时发送周期，单位百微秒
                ('repeat', c_ushort),               # 发送次数，0等于无线循环发
                ('index', c_ubyte),                 # 定时发送列表的帧索引号，也就是第几条定时发送报文
                ('flags', c_ubyte),                 # 0-此帧禁用定时发送，1-此帧使能定时发送
                ('msg', ZCAN_CANFD_FRAME)]


class ZCAN_TTX_TABLE(Structure):                    # 定时发送报文列表
    _fields_ = [('size', c_uint),
                ('table', ZCAN_TTX * 8)]


class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):     # ZCAN_CHANNEL_CAN_INIT_CONFIG
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter", c_ubyte),
                ("timing0", c_ubyte),
                ("timing1", c_ubyte),
                ("mode", c_ubyte)]


class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):    # ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [('clock', c_uint),
                ('mode', c_uint),
                ('aset', _ZCANInitSet),
                ('dset', _ZCANInitSet)]


class ZCAN_CHANNEL_INIT_CONFIG_Union(Union):         # union in ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]
