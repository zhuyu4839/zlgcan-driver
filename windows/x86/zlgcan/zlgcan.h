#ifndef ZLGCAN_H_
#define ZLGCAN_H_

#include <time.h>

#include "canframe.h"
#include "config.h"

#define ZCAN_PCI5121                        1
#define ZCAN_PCI9810                        2
#define ZCAN_USBCAN1                        3
#define ZCAN_USBCAN2                        4
#define ZCAN_PCI9820                        5
#define ZCAN_CAN232                         6
#define ZCAN_PCI5110                        7
#define ZCAN_CANLITE                        8
#define ZCAN_ISA9620                        9
#define ZCAN_ISA5420                        10
#define ZCAN_PC104CAN                       11
#define ZCAN_CANETUDP                       12
#define ZCAN_CANETE                         12
#define ZCAN_DNP9810                        13
#define ZCAN_PCI9840                        14
#define ZCAN_PC104CAN2                      15
#define ZCAN_PCI9820I                       16
#define ZCAN_CANETTCP                       17
#define ZCAN_PCIE_9220                      18
#define ZCAN_PCI5010U                       19
#define ZCAN_USBCAN_E_U                     20
#define ZCAN_USBCAN_2E_U                    21
#define ZCAN_PCI5020U                       22
#define ZCAN_EG20T_CAN                      23
#define ZCAN_PCIE9221                       24
#define ZCAN_WIFICAN_TCP                    25
#define ZCAN_WIFICAN_UDP                    26
#define ZCAN_PCIe9120                       27
#define ZCAN_PCIe9110                       28
#define ZCAN_PCIe9140                       29
#define ZCAN_USBCAN_4E_U                    31
#define ZCAN_CANDTU_200UR                   32
#define ZCAN_CANDTU_MINI                    33
#define ZCAN_USBCAN_8E_U                    34
#define ZCAN_CANREPLAY                      35
#define ZCAN_CANDTU_NET                     36
#define ZCAN_CANDTU_100UR                   37
#define ZCAN_PCIE_CANFD_100U                38
#define ZCAN_PCIE_CANFD_200U                39
#define ZCAN_PCIE_CANFD_400U                40
#define ZCAN_USBCANFD_200U                  41
#define ZCAN_USBCANFD_100U                  42
#define ZCAN_USBCANFD_MINI                  43
#define ZCAN_CANFDCOM_100IE                 44
#define ZCAN_CANSCOPE                       45
#define ZCAN_CLOUD                          46
#define ZCAN_CANDTU_NET_400                 47
#define ZCAN_CANFDNET_TCP                   48
#define ZCAN_CANFDNET_200U_TCP              48
#define ZCAN_CANFDNET_UDP                   49
#define ZCAN_CANFDNET_200U_UDP              49
#define ZCAN_CANFDWIFI_TCP                  50
#define ZCAN_CANFDWIFI_100U_TCP             50
#define ZCAN_CANFDWIFI_UDP                  51
#define ZCAN_CANFDWIFI_100U_UDP             51
#define ZCAN_CANFDNET_400U_TCP              52
#define ZCAN_CANFDNET_400U_UDP              53
#define ZCAN_CANFDBLUE_200U                 54
#define ZCAN_CANFDNET_100U_TCP              55
#define ZCAN_CANFDNET_100U_UDP              56
#define ZCAN_CANFDNET_800U_TCP              57
#define ZCAN_CANFDNET_800U_UDP              58
#define ZCAN_USBCANFD_800U                  59
#define ZCAN_PCIE_CANFD_100U_EX             60
#define ZCAN_PCIE_CANFD_400U_EX             61
#define ZCAN_PCIE_CANFD_200U_MINI           62
#define ZCAN_PCIE_CANFD_200U_M2             63
#define ZCAN_CANFDDTU_400_TCP               64
#define ZCAN_CANFDDTU_400_UDP               65
#define ZCAN_CANFDWIFI_200U_TCP             66
#define ZCAN_CANFDWIFI_200U_UDP             67

#define ZCAN_OFFLINE_DEVICE                 98
#define ZCAN_VIRTUAL_DEVICE                 99

#define ZCAN_ERROR_CAN_OVERFLOW             0x0001
#define ZCAN_ERROR_CAN_ERRALARM             0x0002
#define ZCAN_ERROR_CAN_PASSIVE              0x0004
#define ZCAN_ERROR_CAN_LOSE                 0x0008
#define ZCAN_ERROR_CAN_BUSERR               0x0010
#define ZCAN_ERROR_CAN_BUSOFF               0x0020
#define ZCAN_ERROR_CAN_BUFFER_OVERFLOW      0x0040

#define ZCAN_ERROR_DEVICEOPENED             0x0100
#define ZCAN_ERROR_DEVICEOPEN               0x0200
#define ZCAN_ERROR_DEVICENOTOPEN            0x0400
#define ZCAN_ERROR_BUFFEROVERFLOW           0x0800
#define ZCAN_ERROR_DEVICENOTEXIST           0x1000
#define ZCAN_ERROR_LOADKERNELDLL            0x2000
#define ZCAN_ERROR_CMDFAILED                0x4000
#define ZCAN_ERROR_BUFFERCREATE             0x8000

#define ZCAN_ERROR_CANETE_PORTOPENED        0x00010000
#define ZCAN_ERROR_CANETE_INDEXUSED         0x00020000
#define ZCAN_ERROR_REF_TYPE_ID              0x00030001
#define ZCAN_ERROR_CREATE_SOCKET            0x00030002
#define ZCAN_ERROR_OPEN_CONNECT             0x00030003
#define ZCAN_ERROR_NO_STARTUP               0x00030004
#define ZCAN_ERROR_NO_CONNECTED             0x00030005
#define ZCAN_ERROR_SEND_PARTIAL             0x00030006
#define ZCAN_ERROR_SEND_TOO_FAST            0x00030007

#define STATUS_ERR                          0
#define STATUS_OK                           1
#define STATUS_ONLINE                       2
#define STATUS_OFFLINE                      3
#define STATUS_UNSUPPORTED                  4

#define CMD_DESIP                           0
#define CMD_DESPORT                         1
#define CMD_CHGDESIPANDPORT                 2
#define CMD_SRCPORT                         2
#define CMD_TCP_TYPE                        4
#define TCP_CLIENT                          0
#define TCP_SERVER                          1

#define CMD_CLIENT_COUNT                    5
#define CMD_CLIENT                          6
#define CMD_DISCONN_CLINET                  7
#define CMD_SET_RECONNECT_TIME              8

#define TYPE_CAN                            0
#define TYPE_CANFD                          1
#define TYPE_ALL_DATA                       2

typedef void * DEVICE_HANDLE;
typedef void * CHANNEL_HANDLE;

#pragma pack(push, 1)

typedef struct tagZCAN_DEVICE_INFO {
    USHORT hw_Version;
    USHORT fw_Version;
    USHORT dr_Version;
    USHORT in_Version;
    USHORT irq_Num;
    BYTE   can_Num;
    UCHAR  str_Serial_Num[20];
    UCHAR  str_hw_Type[40];
    USHORT reserved[4];
}ZCAN_DEVICE_INFO;

typedef struct tagZCAN_CHANNEL_INIT_CONFIG {
    UINT can_type;                          //type:TYPE_CAN TYPE_CANFD
    union
    {
        struct
        {
            UINT  acc_code;
            UINT  acc_mask;
            UINT  reserved;
            BYTE  filter;
            BYTE  timing0;
            BYTE  timing1;
            BYTE  mode;
        }can;
        struct
        {
            UINT   acc_code;
            UINT   acc_mask;
            UINT   abit_timing;
            UINT   dbit_timing;
            UINT   brp;
            BYTE   filter;
            BYTE   mode;
            USHORT pad;
            UINT   reserved;
        }canfd;
    };
}ZCAN_CHANNEL_INIT_CONFIG;

typedef struct tagZCAN_CHANNEL_ERR_INFO {
    UINT error_code;
    BYTE passive_ErrData[3];
    BYTE arLost_ErrData;
} ZCAN_CHANNEL_ERR_INFO;

typedef struct tagZCAN_CHANNEL_STATUS {
    BYTE errInterrupt;
    BYTE regMode;
    BYTE regStatus;
    BYTE regALCapture;
    BYTE regECCapture;
    BYTE regEWLimit;
    BYTE regRECounter;
    BYTE regTECounter;
    UINT Reserved;
}ZCAN_CHANNEL_STATUS;

typedef struct tagZCAN_Transmit_Data
{
    can_frame   frame;
    UINT        transmit_type;
}ZCAN_Transmit_Data;

typedef struct tagZCAN_Receive_Data
{
    can_frame   frame;
    UINT64      timestamp;                  //us
}ZCAN_Receive_Data;

typedef struct tagZCAN_TransmitFD_Data
{
    canfd_frame frame;
    UINT        transmit_type;
}ZCAN_TransmitFD_Data;

typedef struct tagZCAN_ReceiveFD_Data
{
    canfd_frame frame;
    UINT64      timestamp;                  //us
}ZCAN_ReceiveFD_Data;

typedef struct tagZCAN_AUTO_TRANSMIT_OBJ{
    USHORT enable;
    USHORT index;                           //0...n
    UINT   interval;                        //ms
    ZCAN_Transmit_Data obj;
}ZCAN_AUTO_TRANSMIT_OBJ, *PZCAN_AUTO_TRANSMIT_OBJ;

typedef struct tagZCANFD_AUTO_TRANSMIT_OBJ{
    USHORT enable;
    USHORT index;                           //0...n
    UINT interval;                          //ms
    ZCAN_TransmitFD_Data obj;
}ZCANFD_AUTO_TRANSMIT_OBJ, *PZCANFD_AUTO_TRANSMIT_OBJ;

//用于设置定时发送额外的参数, 目前只支持USBCANFD-X00U系列设备
typedef struct tagZCAN_AUTO_TRANSMIT_OBJ_PARAM
{
    USHORT index;                           // 定时发送帧的索引
    USHORT type;                            // 参数类型，目前类型只有1：表示启动延时
    UINT   value;                           // 参数数值
}ZCAN_AUTO_TRANSMIT_OBJ_PARAM, *PZCAN_AUTO_TRANSMIT_OBJ_PARAM;

//for zlg cloud
#define ZCLOUD_MAX_DEVICES                  100
#define ZCLOUD_MAX_CHANNEL                  16

typedef struct tagZCLOUD_CHNINFO
{
    BYTE enable;                            // 0:disable, 1:enable
    BYTE type;                              // 0:CAN, 1:ISO CANFD, 2:Non-ISO CANFD
    BYTE isUpload;
    BYTE isDownload;
} ZCLOUD_CHNINFO;

typedef struct tagZCLOUD_DEVINFO
{
    int devIndex;           
    char type[64];
    char id[64];
    char name[64];
    char owner[64];
    char model[64];
    char fwVer[16];
    char hwVer[16];
    char serial[64];
    int status;                             // 0:online, 1:offline
    BYTE bGpsUpload;
    BYTE channelCnt;
    ZCLOUD_CHNINFO channels[ZCLOUD_MAX_CHANNEL];
}ZCLOUD_DEVINFO;

typedef struct tagZCLOUD_USER_DATA
{
    char username[64];
    char mobile[64];
    char dllVer[16];                        // cloud dll version
    size_t devCnt;
    ZCLOUD_DEVINFO devices[ZCLOUD_MAX_DEVICES];
}ZCLOUD_USER_DATA;

// GPS
typedef struct tagZCLOUD_GPS_FRAME
{
    float latitude;                         // + north latitude, - south latitude
    float longitude;                        // + east longitude, - west longitude           
    float speed;                            // km/h    
    struct __gps_time {
        USHORT    year;
        USHORT    mon;
        USHORT    day;
        USHORT    hour;
        USHORT    min;
        USHORT    sec;
    }tm;
} ZCLOUD_GPS_FRAME;
//for zlg cloud

//TX timestamp
typedef struct tagUSBCANFDTxTimeStamp
{
    UINT* pTxTimeStampBuffer;               //allocated by user, size:nBufferTimeStampCount * 4,unit:100us
    UINT  nBufferTimeStampCount;            //buffer size
}USBCANFDTxTimeStamp;

typedef struct tagTxTimeStamp
{
    UINT64* pTxTimeStampBuffer;             //allocated by user, size:nBufferTimeStampCount * 8,unit:1us
    UINT    nBufferTimeStampCount;          //buffer timestamp count
    int     nWaitTime;                      //Wait Time ms, -1表示等到有数据才返回
}TxTimeStamp;

// Bus usage
typedef struct tagBusUsage
{
    UINT64  nTimeStampBegin;                //测量起始时间戳，单位us
    UINT64  nTimeStampEnd;                  //测量结束时间戳，单位us
    BYTE    nChnl;                          //通道
    BYTE    nReserved;                      //保留
    USHORT  nBusUsage;                      //总线利用率(%),总线利用率*100展示。取值0~10000，如8050表示80.50%
    UINT    nFrameCount;                    //帧数量
}BusUsage;

//LIN
typedef struct _VCI_LIN_MSG{
    BYTE    ID;
    BYTE    DataLen;
    USHORT  Flag;
    UINT    TimeStamp;
    BYTE    Data[8];
}ZCAN_LIN_MSG, *PZCAN_LIN_MSG;

#define LIN_MODE_MASTER                     0
#define LIN_MODE_SLAVE                      1
#define LIN_FLAG_CHK_ENHANCE                0x01
#define LIN_FLAG_VAR_DLC                    0x02

typedef struct _VCI_LIN_INIT_CONFIG
{
    BYTE    linMode;
    BYTE    linFlag;
    USHORT  reserved;
    UINT    linBaud;
}ZCAN_LIN_INIT_CONFIG, *PZCAN_LIN_INIT_CONFIG;
//end LIN

enum eZCANErrorDEF
{
    //总线错误类型
    ZCAN_ERR_TYPE_NO_ERR                = 0,        //无错误
    ZCAN_ERR_TYPE_BUS_ERR               = 1,        //总线错误
    ZCAN_ERR_TYPE_CONTROLLER_ERR        = 2,        //控制器错误
    ZCAN_ERR_TYPE_DEVICE_ERR            = 3,        //终端设备错误

    //节点状态
    ZCAN_NODE_STATE_ACTIVE              = 1,        //总线积极
    ZCAN_NODE_STATE_WARNNING            = 2,        //总线告警
    ZCAN_NODE_STATE_PASSIVE             = 3,        //总线消极
    ZCAN_NODE_STATE_BUSOFF              = 4,        //总线关闭

    //总线错误子类型, errType = ZCAN_ERR_TYPE_BUS_ERR
    ZCAN_BUS_ERR_NO_ERR                 = 0,        //无错误
    ZCAN_BUS_ERR_BIT_ERR                = 1,        //位错误
    ZCAN_BUS_ERR_ACK_ERR                = 2,        //应答错误
    ZCAN_BUS_ERR_CRC_ERR                = 3,        //CRC错误
    ZCAN_BUS_ERR_FORM_ERR               = 4,        //格式错误
    ZCAN_BUS_ERR_STUFF_ERR              = 5,        //填充错误
    ZCAN_BUS_ERR_OVERLOAD_ERR           = 6,        //超载错误
    ZCAN_BUS_ERR_ARBITRATION_LOST       = 7,        //仲裁丢失

    //控制器错误, errType = ZCAN_ERR_TYPE_CONTROLLER_ERR
    ZCAN_CONTROLLER_RX_FIFO_OVERFLOW    = 1,        //控制器接收FIFO溢出
    ZCAN_CONTROLLER_DRIVER_RX_BUFFER_OVERFLOW  = 2, //驱动接收缓存溢出
    ZCAN_CONTROLLER_DRIVER_TX_BUFFER_OVERFLOW  = 3, //驱动发送缓存溢出
    ZCAN_CONTROLLER_INTERNAL_ERROR      = 4,        //控制器内部错误

    //终端设备错误, errType = ZCAN_ERR_TYPE_DEVICE_ERR
    ZCAN_DEVICE_APP_RX_BUFFER_OVERFLOW = 1,         //终端应用接收缓存溢出
    ZCAN_DEVICE_APP_TX_BUFFER_OVERFLOW = 2,         //终端应用发送缓存溢出
    ZCAN_DEVICE_APP_AUTO_SEND_FAILED   = 3,         //定时发送失败
    ZCAN_CONTROLLER_TX_FRAME_INVALID   = 4,         //发送报文无效
};

enum eZCANDataDEF
{
    //数据类型
    ZCAN_DT_ZCAN_CAN_CANFD_DATA     = 1,            // CAN/CANFD数据
    ZCAN_DT_ZCAN_ERROR_DATA         = 2,            // 错误数据
    ZCAN_DT_ZCAN_GPS_DATA           = 3,            // GPS数据
    ZCAN_DT_ZCAN_LIN_DATA           = 4,            // LIN数据

    //发送延时单位
    ZCAN_TX_DELAY_NO_DELAY          = 0,            // 无发送延时
    ZCAN_TX_DELAY_UNIT_MS           = 1,            // 发送延时单位毫秒
    ZCAN_TX_DELAY_UNIT_100US        = 2,            // 发送延时单位100微秒(0.1毫秒)

};

// CAN/CANFD数据
typedef struct tagZCANCANFDData
{
    UINT64          timeStamp;                      // 时间戳,数据接收时单位微秒(us),队列延时发送时,数据单位取决于flag.unionVal.txDelay
    union
    {
        struct{
            UINT    frameType : 2;                  // 帧类型, 0:CAN帧, 1:CANFD帧
            UINT    txDelay : 2;                    // 队列发送延时, 发送有效. 0:无发送延时, 1:发送延时单位ms, 2:发送延时单位100us. 启用队列发送延时，延时时间存放在timeStamp字段
            UINT    transmitType : 4;               // 发送类型, 发送有效. 0:正常发送, 1:单次发送, 2:自发自收, 3:单次自发自收. 所有设备支持正常发送，其他类型请参考具体使用手册
            UINT    txEchoRequest : 1;              // 发送回显请求, 发送有效. 支持发送回显的设备,发送数据时将此位置1,设备可以通过接收接口将发送出去的数据帧返回,接收到的发送数据使用txEchoed位标记
            UINT    txEchoed : 1;                   // 报文是否是回显报文, 接收有效. 0:正常总线接收报文, 1:本设备发送回显报文.
            UINT    reserved : 22;                  // 保留
        }unionVal;
        UINT    rawVal;                             // 帧标志位raw数据
    }flag;                                          // CAN/CANFD帧标志位
    BYTE        extraData[4];                       // 额外数据,暂未使用
    canfd_frame frame;                              // can/canfd帧ID+数据
}ZCANCANFDData;

// 错误数据
typedef struct tagZCANErrorData
{
    UINT64  timeStamp;                              // 时间戳, 单位微秒(us)
    BYTE    errType;                                // 错误类型, 参考eZCANErrorDEF中 总线错误类型 部分值定义
    BYTE    errSubType;                             // 错误子类型, 参考eZCANErrorDEF中 总线错误子类型 部分值定义
    BYTE    nodeState;                              // 节点状态, 参考eZCANErrorDEF中 节点状态 部分值定义
    BYTE    rxErrCount;                             // 接收错误计数
    BYTE    txErrCount;                             // 发送错误计数
    BYTE    errData;                                // 错误数据, 和当前错误类型以及错误子类型定义的具体错误相关, 具体请参考使用手册
    BYTE    reserved[2];                            // 保留
}ZCANErrorData;

// GPS数据
typedef struct tagZCANGPSData
{
    struct {
        USHORT  year;                               // 年
        USHORT  mon;                                // 月
        USHORT  day;                                // 日
        USHORT  hour;                               // 时
        USHORT  min;                                // 分
        USHORT  sec;                                // 秒
        USHORT  milsec;                             // 毫秒
    }           time;                               // UTC时间
    union{
        struct{
            USHORT timeValid : 1;                   // 时间数据是否有效
            USHORT latlongValid : 1;                // 经纬度数据是否有效
            USHORT altitudeValid : 1;               // 海拔数据是否有效
            USHORT speedValid : 1;                  // 速度数据是否有效
            USHORT courseAngleValid : 1;            // 航向角数据是否有效
            USHORT reserved:13;                     // 保留
        }unionVal;
        USHORT rawVal;
    }flag;                                          // 标志信息
    double latitude;                                // 纬度 正数表示北纬, 负数表示南纬
    double longitude;                               // 经度 正数表示东经, 负数表示西经
    double altitude;                                // 海拔 单位: 米
    double speed;                                   // 速度 单位: km/h
    double courseAngle;                             // 航向角
} ZCANGPSData;

// LIN数据
typedef struct tagZCANLINData
{
    UINT64          timeStamp;                      // 时间戳，单位微秒(us)
    union {
        struct {
            BYTE    ID:6;                           // 帧ID
            BYTE    Parity:2;                       // 帧ID校验
        }unionVal;
        BYTE    rawVal;                             // 受保护的ID原始值
    }       PID;                                    // 受保护的ID
    BYTE    dataLen;                                // 数据长度
    union{
        struct{
            USHORT tx : 1;                          // 控制器发送在总线上的消息, 接收有效
            USHORT rx : 1;                          // 控制器接收总线上的消息, 接收有效
            USHORT noData : 1;                      // 无数据区
            USHORT chkSumErr : 1;                   // 校验和错误
            USHORT parityErr : 1;                   // 奇偶校验错误， 此时消息中的 chksum 无效
            USHORT syncErr : 1;                     // 同步段错误 
            USHORT bitErr : 1;                      // 发送时位错误 
            USHORT wakeUp : 1;                      // 收到唤醒帧， 此时消息 ID、数据长度、数据域、校验值无效
            USHORT reserved : 8;                    // 保留
        }unionVal;                                  // LIN数据标志位(按位表示)
        USHORT rawVal;                              // LIN数据标志位
    }flag;                                          // 标志信息
    BYTE    chkSum;                                 // 数据校验, 部分设备不支持校验数据的获取
    BYTE    reserved[3];                            // 保留
    BYTE    data[8];                                // 数据
}ZCANLINData;

// 合并接收数据数据结构，支持CAN/CANFD/LIN/GPS/错误等不同类型数据
typedef struct tagZCANDataObj
{
    BYTE        dataType;                           // 数据类型, 参考eZCANDataDEF中 数据类型 部分定义
    BYTE        chnl;                               // 数据通道
    union{
        struct{
            USHORT reserved : 16;                   // 保留
        }unionVal;
        USHORT rawVal;
    }flag;                                          // 标志信息, 暂未使用
    BYTE        extraData[4];                       // 额外数据, 暂未使用
    union
    {
        ZCANCANFDData           zcanCANFDData;      // CAN/CANFD数据
        ZCANErrorData           zcanErrData;        // 错误数据
        ZCANGPSData             zcanGPSData;        // GPS数据
        ZCANLINData             zcanLINData;        // LIN数据
        BYTE                    raw[92];            // RAW数据
    } data;                                         // 实际数据, 联合体，有效成员根据 dataType 字段而定
}ZCANDataObj;

#pragma pack(pop)

#ifdef __cplusplus 
#define DEF(a) = a
#else 
#define DEF(a)
#endif 

#define FUNC_CALL __stdcall
#ifdef __cplusplus
extern "C"
{
#endif

#define INVALID_DEVICE_HANDLE 0
DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
UINT FUNC_CALL ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
UINT FUNC_CALL ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);

UINT FUNC_CALL ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);

#define INVALID_CHANNEL_HANDLE 0
CHANNEL_HANDLE FUNC_CALL ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
UINT FUNC_CALL ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
UINT FUNC_CALL ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
UINT FUNC_CALL ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
UINT FUNC_CALL ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
UINT FUNC_CALL ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
UINT FUNC_CALL ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
UINT FUNC_CALL ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int wait_time DEF(-1));

UINT FUNC_CALL ZCAN_TransmitData(DEVICE_HANDLE device_handle, ZCANDataObj* pTransmit, UINT len);
UINT FUNC_CALL ZCAN_ReceiveData(DEVICE_HANDLE device_handle, ZCANDataObj* pReceive, UINT len, int wait_time DEF(-1));
UINT FUNC_CALL ZCAN_SetValue(DEVICE_HANDLE device_handle, const char* path, const void* value);
const void* FUNC_CALL ZCAN_GetValue(DEVICE_HANDLE device_handle, const char* path);

IProperty* FUNC_CALL GetIProperty(DEVICE_HANDLE device_handle);
UINT FUNC_CALL ReleaseIProperty(IProperty * pIProperty);

void FUNC_CALL ZCLOUD_SetServerInfo(const char* httpSvr, unsigned short httpPort, const char* authSvr, unsigned short authPort);
// return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt connection error, 5:no device
UINT FUNC_CALL ZCLOUD_ConnectServer(const char* username, const char* password);
bool FUNC_CALL ZCLOUD_IsConnected();
// return 0:success, 1:failure
UINT FUNC_CALL ZCLOUD_DisconnectServer();
const ZCLOUD_USER_DATA* FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
UINT FUNC_CALL ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));

CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT can_index, PZCAN_LIN_INIT_CONFIG pLINInitConfig);
UINT FUNC_CALL ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len,int WaitTime);
UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE* pLINID, UINT nIDCount);

#ifdef __cplusplus
}
#endif

#endif //ZLGCAN_H_
