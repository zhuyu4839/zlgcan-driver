__all__ = [
    "ZCAN_LIN_MSG", "ZCAN_LIN_INIT_CONFIG", "ZCANLINDataPid", "ZCANLINDataFlag", "ZCANLINData",
]

from ctypes import Structure, c_ubyte, c_byte, c_ushort, c_uint, c_ulong


class ZCAN_LIN_MSG(Structure):                               # ZCAN_LIN_MSG
    _fields_ = [("ID", c_ubyte),
                ("DataLen", c_byte),
                ("Flag", c_ushort),
                ("TimeStamp", c_uint),
                ("Data", c_ubyte * 8)]


class ZCAN_LIN_INIT_CONFIG(Structure):                   # ZCAN_LIN_INIT_CONFIG
    _fields_ = [("linMode", c_ubyte),
                ("linFlag", c_byte),
                ("reserved", c_ushort),
                ("linBaud", c_uint)]


class ZCANLINDataPid(Structure):
    # _fields_ = [("unionVal", _ZlgLinDataPidVal), ("rawVal", c_ubyte)]
    _pack_ = 1
    _fields_ = [('ID', c_ubyte, 6),
                ('Parity', c_ubyte, 2)]


class ZCANLINDataFlag(Structure):
    _pack_ = 1
    # _fields_ = [("unionVal", _ZlgLinDataFlagVal), ("rawVal", c_ushort)]
    _fields_ = [('tx', c_ushort, 1),                # 控制器发送在总线上的消息, 接收有效
                ('rx', c_ushort, 1),                # 控制器接收总线上的消息, 接收有效
                ('noData', c_ushort, 1),            # 无数据区
                ('chkSumErr', c_ushort, 1),         # 校验和错误
                ('parityErr', c_ushort, 1),         # 奇偶校验错误, 此时消息中的 chksum 无效
                ('syncErr', c_ushort, 1),           # 同步段错误
                ('bitErr', c_ushort, 1),            # 发送时位错误
                ('wakeUp', c_ushort, 1),            # 收到唤醒帧, 此时消息ID|数据长度|数据域|校验值无效
                ('reserved', c_ushort, 8)]          # 保留


class ZCANLINData(Structure):                        # ZCANLINData
    _pack_ = 1
    _fields_ = [("timeStamp", c_ulong),
                ("PID", ZCANLINDataPid),
                ("dataLen", c_ubyte),               # 数据长度
                ("flag", ZCANLINDataFlag),
                ("chkSum", c_ubyte),
                ("reserved", c_ubyte * 3),
                ("data", c_ubyte * 8)]