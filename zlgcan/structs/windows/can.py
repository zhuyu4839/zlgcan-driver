__all__ = [
    "ZCAN_CAN_FRAME", "ZCAN_CANFD_FRAME", "ZCAN_CHANNEL_ERR_INFO", "ZCAN_CHANNEL_STATUS",
    "ZCAN_CHANNEL_INIT_CONFIG_Union", "ZCAN_CHANNEL_INIT_CONFIG", "ZCAN_Transmit_Data",
    "ZCAN_Receive_Data", "ZCAN_TransmitFD_Data", "ZCAN_ReceiveFD_Data", "ZCAN_AUTO_TRANSMIT_OBJ",
    "ZCANFD_AUTO_TRANSMIT_OBJ", "ZCAN_AUTO_TRANSMIT_OBJ_PARAM", "USBCANFDTxTimeStamp", "TxTimeStamp", "BusUsage",
    "ZCANErrorData", "ZCANCANFDDataFlag", "ZCANCANFDData", "ZCANDataObjData", "ZCANDataObjFlag", "ZCANDataObj",
    "IProperty",
]

from ctypes import Structure, c_ubyte, sizeof, Union, c_uint, c_ulong, c_ushort, c_ulonglong, POINTER, c_int, c_long, \
    c_void_p

from .gps import *
from .lin import *


class ZCAN_CAN_FRAME(Structure):               # ZCAN_CAN_FRAME
    _fields_ = [("id", c_uint, 29),
                ("is_error", c_uint, 1),        # 错误帧标识CANID bit29
                ("is_remote", c_uint, 1),       # 远程帧标识CANID bit30
                ("is_extend", c_uint, 1),       # 扩展帧标识CANID bit31
                ("dlc", c_ubyte),               # 数据长度
                ("__pad", c_ubyte),             # 队列模式下bit7为延迟发送标志位
                ("__res0", c_ubyte),            # 队列模式下帧间隔低8位, 单位 ms
                ("__res1", c_ubyte),            # 队列模式下帧间隔高8位, 单位 ms
                ("data", c_ubyte * 8)]


class ZCAN_CANFD_FRAME(Structure):             # ZCAN_CANFD_FRAME
    _fields_ = [("id", c_uint, 29),
                ("is_error", c_uint, 1),    # 错误帧标识CANID bit29
                ("is_remote", c_uint, 1),   # 远程帧标识CANID bit30
                ("is_extend", c_uint, 1),   # 扩展帧标识CANID bit31
                ("len", c_ubyte),           # 数据长度
                ("brs", c_ubyte, 1),        # Bit Rate Switch, flags bit0
                ("esi", c_ubyte, 1),        # Error State Indicator, flags bit1
                ("__res", c_ubyte, 6),      # 保留, flags bit2-7
                ("__res0", c_ubyte),        # 队列模式下帧间隔低8位, 单位 ms
                ("__res1", c_ubyte),        # 队列模式下帧间隔高8位, 单位 ms
                ("data", c_ubyte * 64)]


class ZCAN_CHANNEL_ERR_INFO(Structure):           # ZCAN_CHANNEL_ERR_INFO
    ERROR_CODE = {
        0x0001: 'CAN FIFO Overflow',
        0x0002: 'CAN Error Warning',
        0x0004: 'CAN Passive Error',
        0x0008: 'CAN Arbitration Lost',
        0x0010: 'CAN Bus Error',
        0x0020: 'CAN Bus closed',
        0x0040: 'CAN Cache Overflow'
    }
    _fields_ = [("error_code", c_uint),
                ("passive_ErrData", c_ubyte * 3),
                ("arLost_ErrData", c_ubyte)]

    def __str__(self):
        return f'error info           : {self.ERROR_CODE[self.error_code]} \n' \
               f'passive error info   : {bytes(self.passive_ErrData).hex()} \n' \
               f'arbitration lost info: {self.arLost_ErrData}'


class ZCAN_CHANNEL_STATUS(Structure):         # ZCAN_CHANNEL_STATUS
    _fields_ = [("errInterrupt", c_ubyte),
                ("regMode", c_ubyte),
                ("regStatus", c_ubyte),
                ("regALCapture", c_ubyte),
                ("regECCapture", c_ubyte),
                ("regEWLimit", c_ubyte),
                ("regRECounter", c_ubyte),
                ("regTECounter", c_ubyte),
                ("Reserved", c_ubyte)]


class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):     # _ZCAN_CHANNEL_CAN_INIT_CONFIG
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter", c_ubyte),
                ("timing0", c_ubyte),
                ("timing1", c_ubyte),
                ("mode", c_ubyte)]


class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):    # _ZCAN_CHANNEL_CANFD_INIT_CONFIG
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("abit_timing", c_uint),
                ("dbit_timing", c_uint),
                ("brp", c_uint),
                ("filter", c_ubyte),
                ("mode", c_ubyte),
                ("pad", c_ushort),
                ("reserved", c_uint)]


class ZCAN_CHANNEL_INIT_CONFIG_Union(Union):         # union in ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]


class ZCAN_CHANNEL_INIT_CONFIG(Structure):       # ZCAN_CHANNEL_INIT_CONFIG
    _fields_ = [("type", c_uint),
                ("config", ZCAN_CHANNEL_INIT_CONFIG_Union)]


class ZCAN_Transmit_Data(Structure):            # ZCAN_Transmit_Data
    _pack_ = 1
    _fields_ = [("frame", ZCAN_CAN_FRAME),
                ("transmit_type", c_uint)]      # 0=正常发送, 1=单次发送, 2=自发自收, 3=单次自发自收


class ZCAN_Receive_Data(Structure):             # ZCAN_Receive_Data
    _fields_ = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.is_rx = False

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp:>15.6f} " \
               f"ID: {self.frame.id:08x} " \
               f"{'X' if self.frame.is_extend else 'S'} " \
               f"{'Rx' if self.is_rx else 'Tx'} " \
               f"{'E' if self.frame.is_error else ' '} " \
               f"{'R' if self.frame.is_remote else ' '} " \
               f"  " \
               f"  " \
               f"  " \
               f"DL: {self.frame.dlc:2d} " \
               f"{' '.join('%02x' % self.data[i] for i in range(min(self.frame.dlc, len(self.data))))} " \
               f"Channel: {self.channel}"


class ZCAN_TransmitFD_Data(Structure):          # ZCAN_TransmitFD_Data
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]


class ZCAN_ReceiveFD_Data(Structure):           # ZCAN_ReceiveFD_Data
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.is_rx = False

    def __str__(self) -> str:
        return f"Timestamp: {self.timestamp:>15.6f} " \
               f"ID: {self.frame.id:08x} " \
               f"{'X' if self.frame.is_extend else 'S'} " \
               f"{'Rx' if self.is_rx else 'Tx'} " \
               f"{'E' if self.frame.is_error else ' '} " \
               f"{'R' if self.frame.is_remote else ' '} " \
               f"F " \
               f"{'BS' if self.frame.brs else ' '} " \
               f"{'EI' if self.frame.esi else ' '} " \
               f"DL: {self.frame.len:2d} " \
               f"{' '.join('%02x' % self.data[i] for i in range(min(self.frame.len, len(self.data))))} " \
               f"Channel: {self.channel}"


class ZCAN_AUTO_TRANSMIT_OBJ(Structure):         # ZCAN_AUTO_TRANSMIT_OBJ
    _fields_ = [("enable", c_ushort),
                ("index", c_ushort),
                ("interval", c_uint),  # ms
                ("obj", ZCAN_Transmit_Data)]


class ZCANFD_AUTO_TRANSMIT_OBJ(Structure):       # ZCANFD_AUTO_TRANSMIT_OBJ
    _fields_ = [("enable", c_ushort),
                ("index", c_ushort),
                ("interval", c_uint),
                ("obj", ZCAN_TransmitFD_Data)]


# 用于设置定时发送额外的参数, 目前只支持USBCANFD-X00U系列设备
class ZCAN_AUTO_TRANSMIT_OBJ_PARAM(Structure):      # ZCANFD_AUTO_TRANSMIT_OBJ_PARAM
    _fields_ = [("index", c_ushort),                # 定时发送帧的索引
                ("type", c_ushort),                 # 参数类型，目前类型只有1：表示启动延时
                ("value", c_uint)]                  # 参数数值


class USBCANFDTxTimeStamp(Structure):                    # USBCANFDTxTimeStamp
    _fields_ = [("pTxTimeStampBuffer", POINTER(c_uint)),    # allocated by user, size:nBufferTimeStampCount * 4,unit:100us
                ("nBufferTimeStampCount", c_uint)]          # buffer size


class TxTimeStamp(Structure):                            # TxTimeStamp
    _fields_ = [("pTxTimeStampBuffer", POINTER(c_ulong)),  # allocated by user, size:nBufferTimeStampCount * 8,unit:1us
                ("nBufferTimeStampCount", c_uint),          # buffer timestamp count
                ("nWaitTime", c_int)]                       # Wait Time ms, -1表示等到有数据才返回


class BusUsage(Structure):                               # BusUsage
    _fields_ = [('nTimeStampBegin', c_long),               # 测量起始时间戳，单位us
                ('nTimeStampEnd', c_long),                 # 测量结束时间戳，单位us
                ('nChnl', c_ubyte),                         # 通道
                ('nReserved', c_ubyte),                     # 保留
                ('nBusUsage', c_ushort),                    # 总线利用率(%),总线利用率*100展示。取值0~10000，如8050表示80.50%
                ('nFrameCount', c_uint)]                    # 帧数量


class ZCANErrorData(Structure):                              # ZCANErrorData
    _pack_ = 1
    _fields_ = [("timeStamp", c_ulong),
                ("errType", c_ubyte),
                ("errSubType", c_ubyte),
                ("nodeState", c_ubyte),
                ("rxErrCount", c_ubyte),
                ("txErrCount", c_ubyte),
                ("errData", c_ubyte),
                ("reserved", c_ubyte * 2)]


class ZCANCANFDDataFlag(Structure):              # ZCANdataFlag
    # _fields_ = [("unionVal", _ZlgCanFdDataFlagVal), ("rawVal", c_uint)]
    _pack_ = 1
    _fields_ = [("frameType", c_uint, 2),       # 0-can,1-canfd
                ("txDelay", c_uint, 2),         # 队列发送延时，延时时间存放在 timeStamp 字段
                                                # 0：不启用延时,
                                                # 1：启用延时，延时时间单位为 1 毫秒(1ms),
                                                # 2：启用延时，延时时间单位为 100 微秒(0.1ms)
                ("transmitType", c_uint, 4),    # 发送方式，0-正常发送, 1：单次发送, 2：自发自收, 3：单次自发自收
                ("txEchoRequest", c_uint, 1),   # 发送回显请求，0-不回显，1-回显
                ("txEchoed", c_uint, 1),        # 报文是否是发送回显报文, 0：正常总线接收到的报文, 1：本设备发送回显报文
                ("reserved", c_uint, 22)]       # 保留


class ZCANCANFDData(Structure):                  # ZCANCANFDData
    _pack_ = 1
    _fields_ = [("timeStamp", c_ulong),
                ("flag", ZCANCANFDDataFlag),
                ("extraData", c_ubyte * 4),  # 保留
                ("frame", ZCAN_CANFD_FRAME)]


class ZCANDataObjData(Union):
    _pack_ = 1
    _fields_ = [("zcanCANFDData", ZCANCANFDData), ("zcanErrData", ZCANErrorData),
                ("zcanGPSData", ZCANGPSData), ("zcanLINData", ZCANLINData), ("raw", c_ubyte * 92)]


class ZCANDataObjFlag(Union):
    # _fields_ = [("unionVal", _ZlgDataObjFlagVal), ("rawVal", c_ushort)]
    _pack_ = 1
    _fields_ = [("reserved", c_ushort, 16)]


# 合并接收数据数据结构, 支持CAN/CANFD/LIN/GPS/错误等不同类型数据
class ZCANDataObj(Structure):                    # ZCANDataObj
    _pack_ = 1
    _fields_ = [("dataType", c_ubyte),          # 数据类型, 参考eZCANDataDEF中 数据类型 部分定义
                                                # 1 - CAN/CANFD 数据，data.zcanCANFDData 有效
                                                # 2 - 错误数据，data.zcanErrData 有效
                                                # 3 - GPS 数据，data.zcanGPSData 有效
                                                # 4 - LIN 数据，data.zcanLINData 有效
                ("chnl", c_ubyte),  # 数据通道
                ("flag", ZCANDataObjFlag),      # 标志信息, 暂未使用
                ("extraData", c_ubyte * 4),     # 额外数据, 暂未使用
                ("data", ZCANDataObjData)]      # 实际数据, 联合体，有效成员根据 dataType 字段而定


assert sizeof(ZCANDataObj) == 100
# class ZlgCanDataObj(Structure):                     # from zlgcan echo demo
#     _pack_ = 1
#     _fields_ = [("dataType", c_ubyte),              # can/canfd frame
#                 ("chnl", c_ubyte),                  # can_channel
#                 ("flag", c_ushort),                 # 标志信息, 暂未使用
#                 ("extraData", c_ubyte * 4),         # 标志信息, 暂未使用
#                 ("zcanfddata", ZlgCanFdData),       # 88个字节
#                 ("reserved", c_ubyte * 4)]


class IProperty(Structure):  # IProperty
    _fields_ = [("SetValue", c_void_p),
                ("GetValue", c_void_p),
                ("GetPropertys", c_void_p)]
