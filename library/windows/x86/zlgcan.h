#ifndef ZLGCAN_H_
#define ZLGCAN_H_

#include <time.h>

#include "canframe.h"
#include "config.h"

#define ZCAN_PCI5121              1
#define ZCAN_PCI9810              2
#define ZCAN_USBCAN1              3
#define ZCAN_USBCAN2              4
#define ZCAN_PCI9820              5
#define ZCAN_CAN232               6
#define ZCAN_PCI5110              7
#define ZCAN_CANLITE              8
#define ZCAN_ISA9620              9
#define ZCAN_ISA5420              10
#define ZCAN_PC104CAN             11
#define ZCAN_CANETUDP             12
#define ZCAN_CANETE               12
#define ZCAN_DNP9810              13
#define ZCAN_PCI9840              14
#define ZCAN_PC104CAN2            15
#define ZCAN_PCI9820I             16
#define ZCAN_CANETTCP             17
#define ZCAN_PCIE_9220            18
#define ZCAN_PCI5010U             19
#define ZCAN_USBCAN_E_U           20
#define ZCAN_USBCAN_2E_U          21
#define ZCAN_PCI5020U             22
#define ZCAN_EG20T_CAN            23
#define ZCAN_PCIE9221             24
#define ZCAN_WIFICAN_TCP          25
#define ZCAN_WIFICAN_UDP          26
#define ZCAN_PCIe9120             27
#define ZCAN_PCIe9110             28
#define ZCAN_PCIe9140             29
#define ZCAN_USBCAN_4E_U          31
#define ZCAN_CANDTU_200UR         32
#define ZCAN_CANDTU_MINI          33
#define ZCAN_USBCAN_8E_U          34
#define ZCAN_CANREPLAY            35
#define ZCAN_CANDTU_NET           36
#define ZCAN_CANDTU_100UR         37
#define ZCAN_PCIE_CANFD_100U      38
#define ZCAN_PCIE_CANFD_200U      39
#define ZCAN_PCIE_CANFD_400U      40
#define ZCAN_USBCANFD_200U        41
#define ZCAN_USBCANFD_100U        42
#define ZCAN_USBCANFD_MINI        43
#define ZCAN_CANFDCOM_100IE       44
#define ZCAN_CANSCOPE             45
#define ZCAN_CLOUD                46
#define ZCAN_CANDTU_NET_400       47
#define ZCAN_CANFDNET_TCP         48
#define ZCAN_CANFDNET_200U_TCP    48
#define ZCAN_CANFDNET_UDP         49
#define ZCAN_CANFDNET_200U_UDP    49
#define ZCAN_CANFDWIFI_TCP        50
#define ZCAN_CANFDWIFI_100U_TCP   50
#define ZCAN_CANFDWIFI_UDP        51
#define ZCAN_CANFDWIFI_100U_UDP   51
#define ZCAN_CANFDNET_400U_TCP    52
#define ZCAN_CANFDNET_400U_UDP    53
#define ZCAN_CANFDBLUE_200U       54
#define ZCAN_CANFDNET_100U_TCP    55
#define ZCAN_CANFDNET_100U_UDP    56
#define ZCAN_CANFDNET_800U_TCP    57
#define ZCAN_CANFDNET_800U_UDP    58
#define ZCAN_USBCANFD_800U        59
#define ZCAN_PCIE_CANFD_100U_EX   60
#define ZCAN_PCIE_CANFD_400U_EX   61
#define ZCAN_PCIE_CANFD_200U_MINI 62
#define ZCAN_PCIE_CANFD_200U_M2   63
#define ZCAN_CANFDDTU_400_TCP     64
#define ZCAN_CANFDDTU_400_UDP     65
#define ZCAN_CANFDWIFI_200U_TCP   66
#define ZCAN_CANFDWIFI_200U_UDP   67
#define ZCAN_CANFDDTU_800ER_TCP   68
#define ZCAN_CANFDDTU_800ER_UDP   69
#define ZCAN_CANFDDTU_800EWGR_TCP 70
#define ZCAN_CANFDDTU_800EWGR_UDP 71
#define ZCAN_CANFDDTU_600EWGR_TCP 72
#define ZCAN_CANFDDTU_600EWGR_UDP 73
#define ZCAN_CANFDDTU_CASCADE_TCP 74
#define ZCAN_CANFDDTU_CASCADE_UDP 75
#define ZCAN_USBCANFD_400U        76
#define ZCAN_CANFDDTU_200U        77
#define ZCAN_ZPSCANFD_TCP         78
#define ZCAN_ZPSCANFD_USB         79
#define ZCAN_CANFDBRIDGE_PLUS     80

#define ZCAN_OFFLINE_DEVICE 98
#define ZCAN_VIRTUAL_DEVICE 99

#define ZCAN_ERROR_CAN_OVERFLOW        0x0001
#define ZCAN_ERROR_CAN_ERRALARM        0x0002
#define ZCAN_ERROR_CAN_PASSIVE         0x0004
#define ZCAN_ERROR_CAN_LOSE            0x0008
#define ZCAN_ERROR_CAN_BUSERR          0x0010
#define ZCAN_ERROR_CAN_BUSOFF          0x0020
#define ZCAN_ERROR_CAN_BUFFER_OVERFLOW 0x0040

#define ZCAN_ERROR_DEVICEOPENED   0x0100
#define ZCAN_ERROR_DEVICEOPEN     0x0200
#define ZCAN_ERROR_DEVICENOTOPEN  0x0400
#define ZCAN_ERROR_BUFFEROVERFLOW 0x0800
#define ZCAN_ERROR_DEVICENOTEXIST 0x1000
#define ZCAN_ERROR_LOADKERNELDLL  0x2000
#define ZCAN_ERROR_CMDFAILED      0x4000
#define ZCAN_ERROR_BUFFERCREATE   0x8000

#define ZCAN_ERROR_CANETE_PORTOPENED 0x00010000
#define ZCAN_ERROR_CANETE_INDEXUSED  0x00020000
#define ZCAN_ERROR_REF_TYPE_ID       0x00030001
#define ZCAN_ERROR_CREATE_SOCKET     0x00030002
#define ZCAN_ERROR_OPEN_CONNECT      0x00030003
#define ZCAN_ERROR_NO_STARTUP        0x00030004
#define ZCAN_ERROR_NO_CONNECTED      0x00030005
#define ZCAN_ERROR_SEND_PARTIAL      0x00030006
#define ZCAN_ERROR_SEND_TOO_FAST     0x00030007

typedef UINT ZCAN_RET_STATUS;
#define STATUS_ERR              0
#define STATUS_OK               1
#define STATUS_ONLINE           2
#define STATUS_OFFLINE          3
#define STATUS_UNSUPPORTED      4
#define STATUS_BUFFER_TOO_SMALL 5

typedef UINT ZCAN_LAST_ERROR_STATUS;
//#define STATUS_NO_ERR                       0
//#define STATUS_NO_ERR                       1

typedef UINT ZCAN_UDS_DATA_DEF;
#define DEF_CAN_UDS_DATA  1  // CAN/CANFD UDS数据
#define DEF_LIN_UDS_DATA  2  // LIN UDS数据
#define DEF_DOIP_UDS_DATA 3  // DOIP UDS数据

#define CMD_DESIP           0
#define CMD_DESPORT         1
#define CMD_CHGDESIPANDPORT 2
#define CMD_SRCPORT         2
#define CMD_TCP_TYPE        4
#define TCP_CLIENT          0
#define TCP_SERVER          1

#define CMD_CLIENT_COUNT       5
#define CMD_CLIENT             6
#define CMD_DISCONN_CLINET     7
#define CMD_SET_RECONNECT_TIME 8

#define TYPE_CAN      0
#define TYPE_CANFD    1
#define TYPE_ALL_DATA 2

// 动态配置 持久配置 BEGIN
#define ZCAN_DYNAMIC_CONFIG_DEVNAME \
    "DYNAMIC_CONFIG_DEVNAME"  // 设备名，最长为32字节（包括’\0’），CANFDNET -
                              // 200U默认值为“CANFDNET - 200U”，CANFDNET -
                              // 100MINI默认值为“CANFDNET - 100MINI”
// CAN的通道配置信息(CAN%d需进行格式化声明通道 范围是0-7)
#define ZCAN_DYNAMIC_CONFIG_CAN_ENABLE \
    "DYNAMIC_CONFIG_CAN%d_ENABLE"  // 通道使能；1：使能，0：失能；CANFDNET系列产品通道默认使能。
#define ZCAN_DYNAMIC_CONFIG_CAN_MODE "DYNAMIC_CONFIG_CAN%d_MODE"  // 工作模式，默认正常模式；0：正常模式；1：只听模式。
#define ZCAN_DYNAMIC_CONFIG_CAN_TXATTEMPTS \
    "DYNAMIC_CONFIG_CAN%d_TXATTEMPTS"  // 发送失败是否重传：0：发送失败不重传1：发送失败重传，直到总线关闭（CANFDNET
                                       // - 100 / 200无此项配置）
#define ZCAN_DYNAMIC_CONFIG_CAN_NOMINALBAUD     "DYNAMIC_CONFIG_CAN%d_NOMINALBAUD"  // CAN波特率或CANFD仲裁域波特率；
#define ZCAN_DYNAMIC_CONFIG_CAN_DATABAUD        "DYNAMIC_CONFIG_CAN%d_DATABAUD"     // CANFD数据域波特率；
#define ZCAN_DYNAMIC_CONFIG_CAN_USERES          "DYNAMIC_CONFIG_CAN%d_USERES"       // 终端电阻开关；0：关闭；1：打开。
#define ZCAN_DYNAMIC_CONFIG_CAN_SNDCFG_INTERVAL "DYNAMIC_CONFIG_CAN%d_SNDCFG_INTERVAL"  // 报文发送间隔，0~255ms
#define ZCAN_DYNAMIC_CONFIG_CAN_BUSRATIO_ENABLE \
    "DYNAMIC_CONFIG_CAN%d_BUSRATIO_ENABLE"  // 总线利用率使能，使能后，将周期发送总线利用率到设定的TCP/UDP连接。1:使能，0：失能
#define ZCAN_DYNAMIC_CONFIG_CAN_BUSRATIO_PERIOD \
    "DYNAMIC_CONFIG_CAN%d_BUSRATIO_PERIOD"  // 总线利用率采集周期，取值200~2000ms

typedef struct tagZCAN_DYNAMIC_CONFIG_DATA {
    char key[64];
    char value[64];
} ZCAN_DYNAMIC_CONFIG_DATA;

#define CANFD_FILTER_COUNT_MAX 16
#define CANFD_DATA_LEN_MAX     64

typedef UINT DynamicConfigDataType;
#define DYNAMIC_CONFIG_CAN    0  // CAN通道设置
#define DYNAMIC_CONFIG_FILTER 1  // 滤波设置

union unionCANFDFilterRulePresent {
    struct {
        unsigned int bChnl       : 1;   // 通道条件 是否存在
        unsigned int bFD         : 1;   // CANFD标识 是否存在
        unsigned int bEXT        : 1;   // 标准帧/扩展帧标识 是否存在
        unsigned int bRTR        : 1;   // 数据帧/远程帧标识 是否存在
        unsigned int bLen        : 1;   // 长度  是否存在
        unsigned int bID         : 1;   // 起始ID/结束ID 是否存在
        unsigned int bTime       : 1;   // 起始时间/结束时间 是否存在
        unsigned int bFilterMask : 1;   // 报文数据过滤/屏蔽 是否存在
        unsigned int bErr        : 1;   // 错误报文 CAN/CANFD标志 是否存在
        unsigned int nReserved   : 23;  // 保留
    } unionValue;
    unsigned int rawValue;
};

// 单条过滤规则，
struct CANFD_FILTER_RULE {
    unionCANFDFilterRulePresent presentFlag;  // 标识对应的数据是否存在
    int                         nErr;  // 是否错误报文，此条件一定存在，表示此条过滤是正常帧还是错误帧，0:不过滤错误帧
                                       // 1:过滤错误帧
    int  nChnl;                        // 通道
    int  nFD;                          // CANFD标识，0：CAN; 1:CANFD
    int  nExt;                         // 扩展帧标识，0:标准帧 1:扩展帧
    int  nRtr;                         // 远程帧标识，0:数据帧 1:远程帧
    int  nLen;                         // 报文长度，0-64
    int  nBeginID;                     // 起始ID
    int  nEndID;                       // 结束ID，起始ID值必须<=结束ID，与起始ID成对存在
    int  nBeginTime;                   // 过滤起始时间，单位s，取值0-(24*60*60-1)
    int  nEndTime;                     // 过滤结束时间，单位s，取值0-(24*60*60-1)，与起始时间成对存在
    int  nFilterDataLen;
    int  nMaskDataLen;
    BYTE nFilterData[CANFD_DATA_LEN_MAX];  // 报文过滤数据，uint8数组，最长64
    BYTE nMaskData[CANFD_DATA_LEN_MAX];    // 报文屏蔽数据，uint8数组，最长64，与过滤数据成对存在
};

typedef UINT enumCANFDFilterBlackWhiteList;
#define CANFD_FILTER_BLACK_LIST 0  // 黑名单
#define CANFD_FILTER_WHITE_LIST 1  // 白名单

struct CANFD_FILTER_CFG {
    int                           bEnable;
    enumCANFDFilterBlackWhiteList enBlackWhiteList;
    CANFD_FILTER_RULE             vecFilters[CANFD_FILTER_COUNT_MAX];
};

// 目前只给滤波使用、后续可集成其他模块
typedef struct tagZCAN_DYNAMIC_CONFIG {
    DynamicConfigDataType dynamicConfigDataType;
    UINT                  isPersist;  // 是否是持久配置（即设备掉电保存配置）、TRUE-持久配置
                                      // FALSE-动态配置
    union {
        CANFD_FILTER_CFG
        filterCfg;                 // dynamicConfigDataType = DYNAMIC_CONFIG_FILTER时有效
        BYTE reserved[10 * 1024];  // 保留
    } data;
} ZCAN_DYNAMIC_CONFIG;
// 动态配置 持久配置 END

typedef void *DEVICE_HANDLE;
typedef void *CHANNEL_HANDLE;

typedef struct tagZCAN_DEVICE_INFO {
    USHORT hw_Version;  // 硬件版本
    USHORT fw_Version;  // 固件版本
    USHORT dr_Version;  // 驱动版本
    USHORT in_Version;  // 动态库版本
    USHORT irq_Num;
    BYTE   can_Num;
    UCHAR  str_Serial_Num[20];
    UCHAR  str_hw_Type[40];
    USHORT reserved[4];
} ZCAN_DEVICE_INFO;

typedef struct tagZCAN_CHANNEL_INIT_CONFIG {
    UINT can_type;  // type:TYPE_CAN
                    // TYPE_CANFD（can_type的设备类型只取决于产品硬件的类型，CANFD系列的产品必须设置为1，表示CANFD设备）
    union {
        struct {
            UINT acc_code;
            UINT acc_mask;
            UINT reserved;
            BYTE filter;
            BYTE timing0;
            BYTE timing1;
            BYTE mode;
        } can;
        struct {
            UINT   acc_code;
            UINT   acc_mask;
            UINT   abit_timing;
            UINT   dbit_timing;
            UINT   brp;
            BYTE   filter;
            BYTE   mode;
            USHORT pad;
            UINT   reserved;
        } canfd;
    };
} ZCAN_CHANNEL_INIT_CONFIG;

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
} ZCAN_CHANNEL_STATUS;

typedef struct tagZCAN_Transmit_Data {
    can_frame frame;
    UINT      transmit_type;
} ZCAN_Transmit_Data;

typedef struct tagZCAN_Receive_Data {
    can_frame frame;
    UINT64    timestamp;  // us
} ZCAN_Receive_Data;

typedef struct tagZCAN_TransmitFD_Data {
    canfd_frame frame;
    UINT        transmit_type;
} ZCAN_TransmitFD_Data;

typedef struct tagZCAN_ReceiveFD_Data {
    canfd_frame frame;
    UINT64      timestamp;  // us
} ZCAN_ReceiveFD_Data;

typedef struct tagZCAN_AUTO_TRANSMIT_OBJ {
    USHORT             enable;
    USHORT             index;     // 0...n
    UINT               interval;  // ms
    ZCAN_Transmit_Data obj;
} ZCAN_AUTO_TRANSMIT_OBJ, *PZCAN_AUTO_TRANSMIT_OBJ;

typedef struct tagZCANFD_AUTO_TRANSMIT_OBJ {
    USHORT               enable;
    USHORT               index;     // 0...n
    UINT                 interval;  // ms
    ZCAN_TransmitFD_Data obj;
} ZCANFD_AUTO_TRANSMIT_OBJ, *PZCANFD_AUTO_TRANSMIT_OBJ;

// 用于设置定时发送额外的参数，目前只支持USBCANFD-X00U系列设备
typedef struct tagZCAN_AUTO_TRANSMIT_OBJ_PARAM {
    USHORT index;  // 定时发送帧的索引
    USHORT type;   // 参数类型，目前类型只有1：表示启动延时
    UINT   value;  // 参数数值
} ZCAN_AUTO_TRANSMIT_OBJ_PARAM, *PZCAN_AUTO_TRANSMIT_OBJ_PARAM;

// for zlg cloud
#define ZCLOUD_MAX_DEVICES 100
#define ZCLOUD_MAX_CHANNEL 16

typedef struct tagZCLOUD_CHNINFO {
    BYTE enable;  // 0:disable，1:enable
    BYTE type;    // 0:CAN，1:ISO CANFD，2:Non-ISO CANFD
    BYTE isUpload;
    BYTE isDownload;
} ZCLOUD_CHNINFO;

typedef struct tagZCLOUD_DEVINFO {
    int            devIndex;
    char           type[64];
    char           id[64];
    char           name[64];
    char           owner[64];
    char           model[64];
    char           fwVer[16];
    char           hwVer[16];
    char           serial[64];
    int            status;  // 0:online，1:offline
    BYTE           bGpsUpload;
    BYTE           channelCnt;
    ZCLOUD_CHNINFO channels[ZCLOUD_MAX_CHANNEL];
} ZCLOUD_DEVINFO;

typedef struct tagZCLOUD_USER_DATA {
    char           username[64];
    char           mobile[64];
    char           dllVer[16];  // cloud dll version
    size_t         devCnt;
    ZCLOUD_DEVINFO devices[ZCLOUD_MAX_DEVICES];
} ZCLOUD_USER_DATA;

// GPS
typedef struct tagZCLOUD_GPS_FRAME {
    float latitude;   // + north latitude，- south latitude
    float longitude;  // + east longitude，- west longitude
    float speed;      // km/h
    struct __gps_time {
        USHORT year;
        USHORT mon;
        USHORT day;
        USHORT hour;
        USHORT min;
        USHORT sec;
    } tm;
} ZCLOUD_GPS_FRAME;
// for zlg cloud

// TX timestamp
typedef struct tagUSBCANFDTxTimeStamp {
    UINT *pTxTimeStampBuffer;    // allocated by user, size:nBufferTimeStampCount *
                                 // 4,unit:100us
    UINT nBufferTimeStampCount;  // buffer size
} USBCANFDTxTimeStamp;

typedef struct tagTxTimeStamp {
    UINT64 *pTxTimeStampBuffer;  // allocated by user, size:nBufferTimeStampCount *
                                 // 8,unit:1us
    UINT nBufferTimeStampCount;  // buffer timestamp count
    int  nWaitTime;              // Wait Time ms, -1表示等到有数据才返回
} TxTimeStamp;

// Bus usage
typedef struct tagBusUsage {
    UINT64 nTimeStampBegin;  // 测量起始时间戳，单位us
    UINT64 nTimeStampEnd;    // 测量结束时间戳，单位us
    BYTE   nChnl;            // 通道
    BYTE   nReserved;        // 保留
    USHORT
    nBusUsage;         // 总线利用率(%)，总线利用率*100展示。取值0~10000，如8050表示80.50%
    UINT nFrameCount;  // 帧数量
} BusUsage;

enum eZCANErrorDEF {
    // 总线错误类型
    ZCAN_ERR_TYPE_NO_ERR         = 0,  // 无错误
    ZCAN_ERR_TYPE_BUS_ERR        = 1,  // 总线错误
    ZCAN_ERR_TYPE_CONTROLLER_ERR = 2,  // 控制器错误
    ZCAN_ERR_TYPE_DEVICE_ERR     = 3,  // 终端设备错误

    // 节点状态
    ZCAN_NODE_STATE_ACTIVE   = 1,  // 总线积极
    ZCAN_NODE_STATE_WARNNING = 2,  // 总线告警
    ZCAN_NODE_STATE_PASSIVE  = 3,  // 总线消极
    ZCAN_NODE_STATE_BUSOFF   = 4,  // 总线关闭

    // 总线错误子类型, errType = ZCAN_ERR_TYPE_BUS_ERR
    ZCAN_BUS_ERR_NO_ERR           = 0,  // 无错误
    ZCAN_BUS_ERR_BIT_ERR          = 1,  // 位错误
    ZCAN_BUS_ERR_ACK_ERR          = 2,  // 应答错误
    ZCAN_BUS_ERR_CRC_ERR          = 3,  // CRC错误
    ZCAN_BUS_ERR_FORM_ERR         = 4,  // 格式错误
    ZCAN_BUS_ERR_STUFF_ERR        = 5,  // 填充错误
    ZCAN_BUS_ERR_OVERLOAD_ERR     = 6,  // 超载错误
    ZCAN_BUS_ERR_ARBITRATION_LOST = 7,  // 仲裁丢失
    ZCAN_BUS_ERR_NODE_STATE_CHAGE = 8,  // 总线节点变化

    // 控制器错误, errType = ZCAN_ERR_TYPE_CONTROLLER_ERR
    ZCAN_CONTROLLER_RX_FIFO_OVERFLOW          = 1,  // 控制器接收FIFO溢出
    ZCAN_CONTROLLER_DRIVER_RX_BUFFER_OVERFLOW = 2,  // 驱动接收缓存溢出
    ZCAN_CONTROLLER_DRIVER_TX_BUFFER_OVERFLOW = 3,  // 驱动发送缓存溢出
    ZCAN_CONTROLLER_INTERNAL_ERROR            = 4,  // 控制器内部错误

    // 终端设备错误, errType = ZCAN_ERR_TYPE_DEVICE_ERR
    ZCAN_DEVICE_APP_RX_BUFFER_OVERFLOW = 1,  // 终端应用接收缓存溢出
    ZCAN_DEVICE_APP_TX_BUFFER_OVERFLOW = 2,  // 终端应用发送缓存溢出
    ZCAN_DEVICE_APP_AUTO_SEND_FAILED   = 3,  // 定时发送失败
    ZCAN_CONTROLLER_TX_FRAME_INVALID   = 4,  // 发送报文无效
};

enum eZCANDataDEF {
    // 数据类型
    ZCAN_DT_ZCAN_CAN_CANFD_DATA = 1,  // CAN/CANFD数据
    ZCAN_DT_ZCAN_ERROR_DATA     = 2,  // 错误数据
    ZCAN_DT_ZCAN_GPS_DATA       = 3,  // GPS数据
    ZCAN_DT_ZCAN_LIN_DATA       = 4,  // LIN数据
    ZCAN_DT_ZCAN_BUSUSAGE_DATA  = 5,  // BusUsage数据
    ZCAN_DT_ZCAN_LIN_ERROR_DATA = 6,  // LIN错误数据
    ZCAN_DT_ZCAN_LIN_EX_DATA    = 7,  // LIN扩展数据
    ZCAN_DT_ZCAN_LIN_EVENT_DATA = 8,  // LIN事件数据

    // 发送延时单位
    ZCAN_TX_DELAY_NO_DELAY   = 0,  // 无发送延时
    ZCAN_TX_DELAY_UNIT_MS    = 1,  // 发送延时单位毫秒
    ZCAN_TX_DELAY_UNIT_100US = 2,  // 发送延时单位100微秒(0.1毫秒)
};

#pragma pack(push, 1)

// CAN/CANFD数据
typedef struct tagZCANCANFDData {
    UINT64
    timeStamp;  // 时间戳，数据接收时单位微秒(us)，队列延时发送时，数据单位取决于flag.unionVal.txDelay
    union {
        struct {
            UINT frameType : 2;     // 帧类型，0:CAN帧，1:CANFD帧
            UINT txDelay   : 2;     // 队列发送延时，发送有效.
                                    // 0:无发送延时，1:发送延时单位ms，2:发送延时单位100us.
                                    // 启用队列发送延时，延时时间存放在timeStamp字段
            UINT transmitType : 4;  // 发送类型，发送有效.
                                    // 0:正常发送，1:单次发送，2:自发自收，3:单次自发自收.
                                    // 所有设备支持正常发送，其他类型请参考具体使用手册
            UINT
                txEchoRequest : 1;  // 发送回显请求，发送有效.
                                    // 支持发送回显的设备，发送数据时将此位置1，设备可以通过接收接口将发送出去的数据帧返回，接收到的发送数据使用txEchoed位标记
            UINT txEchoed : 1;      // 报文是否是回显报文，接收有效.
                                    // 0:正常总线接收报文，1:本设备发送回显报文.
            UINT reserved : 22;     // 保留
        } unionVal;
        UINT rawVal;           // 帧标志位raw数据
    } flag;                    // CAN/CANFD帧标志位
    BYTE        extraData[4];  // 额外数据,暂未使用
    canfd_frame frame;         // CAN/CANFD帧ID+数据
} ZCANCANFDData;

// 错误数据
typedef struct tagZCANErrorData {
    UINT64 timeStamp;   // 时间戳，单位微秒(us)
    BYTE   errType;     // 错误类型，参考eZCANErrorDEF中 总线错误类型 部分值定义
    BYTE   errSubType;  // 错误子类型，参考eZCANErrorDEF中 总线错误子类型 部分值定义
    BYTE   nodeState;   // 节点状态，参考eZCANErrorDEF中 节点状态 部分值定义
    BYTE   rxErrCount;  // 接收错误计数
    BYTE   txErrCount;  // 发送错误计数
    BYTE   errData;     // 错误数据，和当前错误类型以及错误子类型定义的具体错误相关,
                        // 具体请参考使用手册
    BYTE reserved[2];   // 保留
} ZCANErrorData;

// GPS数据
typedef struct tagZCANGPSData {
    struct {
        USHORT year;    // 年
        USHORT mon;     // 月
        USHORT day;     // 日
        USHORT hour;    // 时
        USHORT min;     // 分
        USHORT sec;     // 秒
        USHORT milsec;  // 毫秒
    } time;             // UTC时间
    union {
        struct {
            USHORT timeValid        : 1;   // 时间数据是否有效
            USHORT latlongValid     : 1;   // 经纬度数据是否有效
            USHORT altitudeValid    : 1;   // 海拔数据是否有效
            USHORT speedValid       : 1;   // 速度数据是否有效
            USHORT courseAngleValid : 1;   // 航向角数据是否有效
            USHORT reserved         : 13;  // 保留
        } unionVal;
        USHORT rawVal;
    } flag;              // 标志信息
    double latitude;     // 纬度 正数表示北纬，负数表示南纬
    double longitude;    // 经度 正数表示东经，负数表示西经
    double altitude;     // 海拔 单位: 米
    double speed;        // 速度 单位: km/h
    double courseAngle;  // 航向角
} ZCANGPSData;

// LIN数据
typedef struct tagZCANLINData {
    union {
        struct {
            BYTE ID     : 6;  // 帧ID
            BYTE Parity : 2;  // 帧ID校验
        } unionVal;
        BYTE rawVal;  // 受保护的ID原始值
    } PID;            // 受保护的ID
    struct {
        UINT64 timeStamp;     // 时间戳，单位微秒(us)
        BYTE   dataLen;       // 数据长度
        BYTE   dir;           // 传输方向，0-接收 1-发送
        BYTE   chkSum;        // 数据校验，部分设备不支持校验数据的获取
        BYTE   reserved[13];  // 保留
        BYTE   data[8];       // 数据
    } RxData;                 // 仅接收数据时有效
    BYTE reserved[7];         // 保留
} ZCANLINData;

// 错误数据
typedef struct tagZCANLINErrData {
    UINT64 timeStamp;  // 时间戳，单位微秒(us)
    union {
        struct {
            BYTE ID     : 6;  // 帧ID
            BYTE Parity : 2;  // 帧ID校验
        } unionVal;
        BYTE rawVal;  // 受保护的ID原始值
    } PID;            // 受保护的ID
    BYTE dataLen;
    BYTE data[8];
    union {
        struct {
            USHORT errStage  : 4;  // 错误阶段
            USHORT errReason : 4;  // 错误原因
            USHORT reserved  : 8;  // 保留
        };
        USHORT unionErrData;
    } errData;
    BYTE dir;           // 传输方向
    BYTE chkSum;        // 数据校验，部分设备不支持校验数据的获取
    BYTE reserved[10];  // 保留
} ZCANLINErrData;

typedef BYTE ZCAN_LIN_EVENT_TYPE;
#define ZCAN_LIN_WAKE_UP            1
#define ZCAN_LIN_ENTERED_SLEEP_MODE 2
#define ZCAN_LIN_EXITED_SLEEP_MODE  3

typedef struct tagZCANLINEventData {
    UINT64              timeStamp;  // 时间戳，单位微秒(us)
    ZCAN_LIN_EVENT_TYPE type;
    BYTE                reserved[7];
} ZCANLINEventData;

// LIN扩展数据
typedef struct tagZCANLINExData {
    union {
        struct {
            BYTE ID     : 6;  // 帧ID
            BYTE Parity : 2;  // 帧ID校验
        } unionVal;
        BYTE rawVal;   // 受保护的ID原始值
    } PID;             // 受保护的ID
    BYTE reserved[7];  // 保留
    struct {
        UINT64 timeStamp;    // 时间戳，单位微秒(us)
        BYTE   dataLen;      // 数据长度
        BYTE   dir;          // 传输方向，0-接收 1-发送
        BYTE   chkSum;       // 数据校验，部分设备不支持校验数据的获取
        BYTE   reserved[5];  // 保留
        BYTE   data[64];     // 数据
    } RxData;                // 仅接收数据时有效
} ZCANLINExData;

// 合并接收数据数据结构，支持CAN/CANFD/LIN/GPS/错误等不同类型数据
typedef struct tagZCANDataObj {
    BYTE dataType;  // 数据类型，参考eZCANDataDEF中 数据类型 部分定义
    BYTE chnl;      // 数据通道
    union {
        struct {
            USHORT reserved : 16;  // 保留
        } unionVal;
        USHORT rawVal;
    } flag;             // 标志信息，暂未使用
    BYTE extraData[4];  // 额外数据，暂未使用
    union {
        ZCANCANFDData    zcanCANFDData;     // CAN/CANFD数据
        ZCANErrorData    zcanErrData;       // 错误数据
        ZCANGPSData      zcanGPSData;       // GPS数据
        ZCANLINData      zcanLINData;       // LIN数据
        ZCANLINErrData   zcanLINErrData;    // LIN错误数据
        ZCANLINExData    zcanLINExData;     // LIN扩展数据
        ZCANLINEventData zcanLINEventData;  // LIN事件数据
        BusUsage         busUsage;          // BusUsage数据
        BYTE             raw[92];           // RAW数据
    } data;                                 // 实际数据，联合体，有效成员根据 dataType 字段而定
} ZCANDataObj;

// LIN
typedef struct _VCI_LIN_MSG {
    BYTE chnl;      // 数据通道
    BYTE dataType;  // 数据类型，0-LIN数据 1-LIN错误数据 2-LIN事件数据
    union {
        ZCANLINData      zcanLINData;       // LIN数据
        ZCANLINErrData   zcanLINErrData;    // LIN错误数据
        ZCANLINEventData zcanLINEventData;  // LIN事件数据
        BYTE             raw[46];           // RAW数据
    } data;                                 // 实际数据，联合体，有效成员根据 dataType 字段而定
} ZCAN_LIN_MSG, *PZCAN_LIN_MSG;

enum eZLINChkSumMode {
    DEFAULT = 0,     // 默认，启动时配置
    CLASSIC_CHKSUM,  // 经典校验
    ENHANCE_CHKSUM,  // 增强校验
    AUTOMATIC,       // 自动，设备自动识别校验方式（仅ZCAN_SetLINSubscribe时有效）
};

typedef struct _VCI_LIN_INIT_CONFIG {
    BYTE linMode;     // 是否作为主机，0-从机，1-主机
    BYTE chkSumMode;  // 校验方式，1-经典校验 2-增强校验 3-自动(对应eZLINChkSumMode的模式)
    BYTE maxLength;  // 最大数据长度，8~64
    BYTE reserved;   // 保留
    UINT linBaud;    // 波特率，取值1000~20000
} ZCAN_LIN_INIT_CONFIG, *PZCAN_LIN_INIT_CONFIG;

typedef struct _VCI_LIN_PUBLISH_CFG {
    BYTE ID;       // 受保护的ID（ID取值范围为0-63）
    BYTE dataLen;  // dataLen范围为1-8
    BYTE data[8];
    BYTE chkSumMode;   // 校验方式，0-默认，启动时配置 1-经典校验
                       // 2-增强校验(对应eZLINChkSumMode的模式)
    BYTE reserved[5];  // 保留
} ZCAN_LIN_PUBLISH_CFG, *PZCAN_LIN_PUBLISH_CFG;

typedef struct _VCI_LIN_PUBLISH_CFG_EX {
    BYTE ID;       // 受保护的ID（ID取值范围为0-63）
    BYTE dataLen;  // dataLen范围为1-64
    BYTE data[64];
    BYTE chkSumMode;   // 校验方式，0-默认，启动时配置 1-经典校验
                       // 2-增强校验(对应eZLINChkSumMode的模式)
    BYTE reserved[5];  // 保留
} ZCAN_LIN_PUBLISH_CFG_EX, *PZCAN_LIN_PUBLISH_CFG_EX;

typedef struct _VCI_LIN_SUBSCIBE_CFG {
    BYTE ID;           // 受保护的ID（ID取值范围为0-63）
    BYTE dataLen;      // dataLen范围为1-8 当为255（0xff）则表示设备自动识别报文长度
    BYTE chkSumMode;   // 校验方式，0-默认，启动时配置 1-经典校验 2-增强校验
                       // 3-自动(对应eZLINChkSumMode的模式)
    BYTE reserved[5];  // 保留
} ZCAN_LIN_SUBSCIBE_CFG, *PZCAN_LIN_SUBSCIBE_CFG;

// end LIN

// UDS传输协议版本
typedef BYTE ZCAN_UDS_TRANS_VER;
#define ZCAN_UDS_TRANS_VER_0 0  // ISO15765-2(2004版本)
#define ZCAN_UDS_TRANS_VER_1 1  // ISO15765-2(2016版本)

// 帧类型
typedef BYTE ZCAN_UDS_FRAME_TYPE;
#define ZCAN_UDS_FRAME_CAN       0  // CAN帧
#define ZCAN_UDS_FRAME_CANFD     1  // CANFD帧
#define ZCAN_UDS_FRAME_CANFD_BRS 2  // CANFD加速帧

// CAN UDS请求数据
typedef struct _ZCAN_UDS_REQUEST {
    UINT                req_id;             // 请求事务ID，范围0~65535，本次请求的唯一标识
    BYTE                channel;            // 设备通道索引 0~255
    ZCAN_UDS_FRAME_TYPE frame_type;         // 帧类型
    BYTE                reserved0[2];       // 保留
    UINT                src_addr;           // 请求地址
    UINT                dst_addr;           // 响应地址
    BYTE                suppress_response;  // 1:抑制响应
    BYTE                sid;                // 请求服务id
    BYTE                reserved1[6];       // 保留
    struct {
        UINT timeout;           // 响应超时时间(ms)。因PC定时器误差，建议设置不小于200ms
        UINT enhanced_timeout;  // 收到消极响应错误码为0x78后的超时时间(ms)。因PC定时器误差，建议设置不小于200ms
        BYTE check_any_negative_response : 1;  // 接收到非本次请求服务的消极响应时是否需要判定为响应错误
        BYTE wait_if_suppress_response   : 1;  // 抑制响应时是否需要等待消极响应，等待时长为响应超时时间
        BYTE flag                        : 6;  // 保留
        BYTE reserved0[7];                     // 保留
    } session_param;                           // 会话层参数
    struct {
        ZCAN_UDS_TRANS_VER version;       // 传输协议版本，VERSION_0，VERSION_1
        BYTE               max_data_len;  // 单帧最大数据长度，can:8，canfd:64
        BYTE local_st_min;  // 本程序发送流控时用，连续帧之间的最小间隔，0x00-0x7F(0ms~127ms)，0xF1-0xF9(100us~900us)
        BYTE block_size;    // 流控帧的块大小
        BYTE fill_byte;     // 无效字节的填充数据
        BYTE ext_frame;     // 0:标准帧 1:扩展帧
        BYTE is_modify_ecu_st_min;  // 是否忽略ECU返回流控的STmin，强制使用本程序设置的
                                    // remote_st_min
        BYTE remote_st_min;         // 发送多帧时用，is_ignore_ecu_st_min = 1
                                    // 时有效，0x00-0x7F(0ms~127ms)，0xF1-0xF9(100us~900us)
        UINT fc_timeout;            // 接收流控超时时间(ms)，如发送首帧后需要等待回应流控帧
        BYTE reserved0[4];          // 保留
    } trans_param;                  // 传输层参数
    BYTE *data;                     // 数据数组(不包含SID)
    UINT  data_len;                 // 数据数组的长度
    UINT  reserved2;                // 保留
} ZCAN_UDS_REQUEST;

// LIN UDS请求数据
typedef struct _ZLIN_UDS_REQUEST {
    UINT req_id;             // 请求事务ID，范围0~65535，本次请求的唯一标识
    BYTE channel;            // 设备通道索引 0~255
    BYTE suppress_response;  // 1:抑制响应 0:不抑制
    BYTE sid;                // 请求服务id
    BYTE Nad;                // 节点地址
    BYTE reserved1[8];       // 保留
    struct {
        UINT p2_timeout;        // 响应超时时间(ms)。因PC定时器误差，建议设置不小于200ms
        UINT enhanced_timeout;  // 收到消极响应错误码为0x78后的超时时间(ms)。因PC定时器误差，建议设置不小于200ms
        BYTE check_any_negative_response : 1;  // 接收到非本次请求服务的消极响应时是否需要判定为响应错误
        BYTE wait_if_suppress_response   : 1;  // 抑制响应时是否需要等待消极响应，等待时长为响应超时时间
        BYTE flag                        : 6;  // 保留
        BYTE reserved0[7];                     // 保留
    } session_param;                           // 会话层参数
    struct {
        BYTE fill_byte;     // 无效字节的填充数据
        BYTE st_min;        // 从节点准备接收诊断请求的下一帧或传输诊断响应的下一帧所需的最小时间
        BYTE reserved0[6];  // 保留
    } trans_param;          // 传输层参数
    BYTE *data;             // 数据数组(不包含SID)
    UINT  data_len;         // 数据数组的长度
    UINT  reserved2;        // 保留
} ZLIN_UDS_REQUEST;

typedef BYTE ZCAN_DOIP_ROUTING_ACT_TYPE;
#define ZCAN_DOIP_ACTIVATION_DEFAULT          0x00
#define ZCAN_DOIP_ACTIVATION_WWH_OBD          0x01
#define ZCAN_DOIP_ACTIVATION_CENTRAL_SECURITY 0xE0

typedef BYTE ZCAN_DOIP_VERSION;
#define ZCAN_DOIP_ISO_13400_2_2010      0x01
#define ZCAN_DOIP_ISO_13400_2_2012      0x02
#define ZCAN_DOIP_ISO_13400_2_2019      0x03
#define ZCAN_DOIP_AUTO_DETECTED_VERSION 0xFF

// DoIP 请求数据
typedef struct _ZDOIP_REQUEST {
    UINT req_id;        // 请求事务ID，范围0~65535，本次请求的唯一标识
    BYTE reserved0[4];  // 保留

    ZCAN_DOIP_VERSION          doipVersion;        // DoIP协议版本
    ZCAN_DOIP_ROUTING_ACT_TYPE rcType;             // 路由激活类型
    BYTE                       sourceAddress[2];   // 源逻辑地址
    char                       serverAddress[32];  // DoIP实体的IP地址
    USHORT                     connectTimeoutMs;   // 连接超时
    USHORT                     routingTimeoutMs;   // 路由激活超时

    BYTE  targetAddress[2];  // 目标逻辑地址
    BYTE  sid;               // 请求的SID
    BYTE  suppressPosResp;   // 是否抑制积极响应
    BYTE  waitForNegResp;    // 是否等待消极响应，suppressPosResp为真时有效
    BYTE  reserved1[3];      // 保留
    UINT  requestTimeoutMs;  // UDS请求超时
    UINT  dataLength;        // 诊断数据长度
    BYTE *data;              // 诊断数据
} ZDOIP_REQUEST;

// UDS错误码
typedef BYTE ZCAN_UDS_ERROR;
#define ZCAN_UDS_ERROR_OK                                            0x00  // 没错误
#define ZCAN_UDS_ERROR_TIMEOUT                                       0x01  // 响应超时
#define ZCAN_UDS_ERROR_TRANSPORT                                     0x02  // 发送数据失败
#define ZCAN_UDS_ERROR_CANCEL                                        0x03  // 取消请求
#define ZCAN_UDS_ERROR_SUPPRESS_RESPONSE                             0x04  // 抑制响应
#define ZCAN_UDS_ERROR_BUSY                                          0x05  // 忙碌中
#define ZCAN_UDS_ERROR_REQ_PARAM                                     0x06  // 请求参数错误
#define ZCAN_UDS_ERROR_OTHTER                                        0x64  // 其它未知错误
#define ZCAN_UDS_ERROR_DOIP_FAILED_TO_CREATE_SOCKET                  0x20  // 创建socket失败
#define ZCAN_UDS_ERROR_DOIP_FAILED_TO_CONNECT                        0x21  // 建立连接失败
#define ZCAN_UDS_ERROR_DOIP_TIMEOUT                                  0x22  // 操作超时
#define ZCAN_UDS_ERROR_DOIP_ROUTING_NOT_ACTIVE                       0x23  // 路由未激活
#define ZCAN_UDS_ERROR_DOIP_BUFFER_TOO_SMALL                         0x24  // 缓冲区不足
#define ZCAN_UDS_ERROR_DOIP_ROUTING_ALREADY_ACTIVE                   0x25  // 路由已被激活
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_INCORRECT_PATTERN_FORMAT     0x26  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_UNKNOWN_PAYLOAD_TYPE         0x27  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_MESSAGE_TOO_LARGE            0x28  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_OUT_OF_MEMORY                0x29  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_INVALID_PAYLOAD_LENGTH       0x2A  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_HEADER_NACK_UNKNOWN                      0x2B  // 收到DoIP头部NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_INVALID_SOURCE_ADDRESS   0x2C  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_UNKNOWN_TARGET_ADDRESS   0x2D  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_MESSAGE_TOO_LARGE        0x2E  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_OUT_OF_MEMORY            0x2F  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_TARGET_UNREACHABLE       0x30  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_UNKNOWN_NETWORK          0x31  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_TRANSPORT_PROTOCOL_ERROR 0x32  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_DIAGNOSTIC_NACK_UNKNOWN                  0x33  // 收到诊断请求NACK
#define ZCAN_UDS_ERROR_DOIP_INVALID_HANDLE                           0x34  // 无效的句柄
#define ZCAN_UDS_ERROR_DOIP_UNEXPECTED_NULL_POINTER                  0x35  // 未预期的空指针
#define ZCAN_UDS_ERROR_DOIP_UNKNOWN_HANDLE                           0x36  // 未知的句柄
#define ZCAN_UDS_ERROR_DOIP_OUT_OF_MEMORY                            0x37  // 内存不足
#define ZCAN_UDS_ERROR_DOIP_UNKNOWN_ERROR                            0x38  // 未知的错误
#define ZCAN_UDS_ERROR_DOIP_ROUTING_ACTIVE_FAIL                      0x39  // 路由激活失败

typedef BYTE ZCAN_UDS_RESPONSE_TYPE;
#define ZCAN_UDS_RT_NEGATIVE 0  // 消极响应
#define ZCAN_UDS_RT_POSITIVE 1  // 积极响应
#define ZCAN_UDS_RT_NONE     2  // 无响应

// UDS响应数据
typedef struct _ZCAN_UDS_RESPONSE {
    ZCAN_UDS_ERROR         status;       // 响应状态
    BYTE                   reserved[6];  // 保留
    ZCAN_UDS_RESPONSE_TYPE type;         // 响应类型
    union {
        struct {
            BYTE sid;       // 响应服务id
            UINT data_len;  // 数据长度(不包含SID), 数据存放在接口传入的dataBuf中
        } positive;
        struct {
            BYTE neg_code;    // 固定为0x7F
            BYTE sid;         // 请求服务id
            BYTE error_code;  // 错误码
        } negative;
        BYTE raw[8];
    };
} ZCAN_UDS_RESPONSE;

// UDS控制类型
typedef UINT ZCAN_UDS_CTRL_CODE;
#define ZCAN_UDS_CTRL_STOP_REQ 0  // 停止UDS请求

// UDS控制请求
typedef struct _ZCAN_UDS_CTRL_REQ {
    UINT               reqID;        // 请求事务ID，指明要操作哪一条请求
    ZCAN_UDS_CTRL_CODE cmd;          // 控制类型
    BYTE               reserved[8];  // 保留
} ZCAN_UDS_CTRL_REQ;

// UDS控制结果
typedef UINT ZCAN_UDS_CTRL_RESULT;
#define ZCAN_UDS_CTRL_RESULT_OK  0  // 成功
#define ZCAN_UDS_CTRL_RESULT_ERR 1  // 失败

// UDS控制响应数据
typedef struct _ZCAN_UDS_CTRL_RESP {
    ZCAN_UDS_CTRL_RESULT result;        // 操作结果
    BYTE                 reserved[12];  // 保留
} ZCAN_UDS_CTRL_RESP;

// CAN/CANFD UDS数据
typedef struct tagZCANCANFDUdsData {
    const ZCAN_UDS_REQUEST *req;  // 请求信息
    BYTE                    reserved[24];
} ZCANCANFDUdsData;

// LIN UDS数据
typedef struct tagZCANLINUdsData {
    const ZLIN_UDS_REQUEST *req;  // 请求信息
    BYTE                    reserved[24];
} ZCANLINUdsData;

// DoIP UDS数据
typedef struct tagZDoIPUdsData {
    const ZDOIP_REQUEST *req;  // 请求信息
    BYTE                 reserved[24];
} ZDoIPUdsData;

// UDS数据结构，支持CAN/LIN等UDS不同类型数据
typedef struct tagZCANUdsRequestDataObj {
    ZCAN_UDS_DATA_DEF dataType;  // 数据类型
    union {
        ZCANCANFDUdsData zcanCANFDUdsData;  // CAN/CANFD UDS数据
        ZCANLINUdsData   zcanLINUdsData;    // LIN UDS数据
        ZDoIPUdsData     zcanDoIPUdsData;   // DoIP UDS数据
        BYTE             raw[63];           // RAW数据
    } data;                                 // 实际数据，联合体，有效成员根据 dataType 字段而定
    BYTE reserved[32];                      // 保留位
} ZCANUdsRequestDataObj;

#pragma pack(pop)

#ifdef __cplusplus
#define DEF(a) = a
#else
#define DEF(a)
#endif

#ifdef WIN32
#define FUNC_CALL __stdcall
#else
#define FUNC_CALL  // __attribute__((stdcall))
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define INVALID_DEVICE_HANDLE 0
DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
UINT FUNC_CALL          ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
UINT FUNC_CALL          ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO *pInfo);

UINT FUNC_CALL ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);

#define INVALID_CHANNEL_HANDLE 0
CHANNEL_HANDLE FUNC_CALL ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index,
                                      ZCAN_CHANNEL_INIT_CONFIG *pInitConfig);
UINT FUNC_CALL           ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO *pErrInfo);
UINT FUNC_CALL           ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS *pCANStatus);
UINT FUNC_CALL           ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle,
                                            BYTE           type);  // type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
UINT FUNC_CALL           ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data *pTransmit, UINT len);
UINT FUNC_CALL           ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data *pReceive, UINT len,
                                      int wait_time DEF(-1));
UINT FUNC_CALL           ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data *pTransmit, UINT len);
UINT FUNC_CALL           ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data *pReceive, UINT len,
                                        int wait_time DEF(-1));

UINT FUNC_CALL ZCAN_TransmitData(DEVICE_HANDLE device_handle, ZCANDataObj *pTransmit, UINT len);
UINT FUNC_CALL ZCAN_ReceiveData(DEVICE_HANDLE device_handle, ZCANDataObj *pReceive, UINT len, int wait_time DEF(-1));
UINT FUNC_CALL ZCAN_SetValue(DEVICE_HANDLE device_handle, const char *path, const void *value);
const void *FUNC_CALL ZCAN_GetValue(DEVICE_HANDLE device_handle, const char *path);

IProperty *FUNC_CALL GetIProperty(DEVICE_HANDLE device_handle);
UINT FUNC_CALL       ReleaseIProperty(IProperty *pIProperty);

void FUNC_CALL ZCLOUD_SetServerInfo(const char *httpSvr, unsigned short httpPort, const char *authSvr,
                                    unsigned short authPort);
// return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt
// connection error, 5:no device
UINT FUNC_CALL ZCLOUD_ConnectServer(const char *username, const char *password);
// return 0:not connected, 1:connected
UINT FUNC_CALL ZCLOUD_IsConnected();
// return 0:success, 1:failure
UINT FUNC_CALL                    ZCLOUD_DisconnectServer();
const ZCLOUD_USER_DATA *FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
UINT FUNC_CALL                    ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME *pReceive, UINT len,
                                                    int wait_time DEF(-1));

CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT lin_index,
                                      PZCAN_LIN_INIT_CONFIG pLINInitConfig);
UINT FUNC_CALL           ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
UINT FUNC_CALL           ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL           ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len, int WaitTime);

UINT FUNC_CALL ZCAN_SetLINSubscribe(CHANNEL_HANDLE channel_handle, PZCAN_LIN_SUBSCIBE_CFG pSend, UINT nSubscribeCount);
UINT FUNC_CALL ZCAN_SetLINPublish(CHANNEL_HANDLE channel_handle, PZCAN_LIN_PUBLISH_CFG pSend, UINT nPublishCount);
UINT FUNC_CALL ZCAN_SetLINPublishEx(CHANNEL_HANDLE channel_handle, PZCAN_LIN_PUBLISH_CFG_EX pSend, UINT nPublishCount);

UINT FUNC_CALL ZCAN_WakeUpLIN(CHANNEL_HANDLE channel_handle);

/**
 * @brief UDS诊断请求 (DoCAN)
 * @param[in] device_handle 设备句柄
 * @param[in] req 请求信息
 * @param[out] resp 响应信息，可为nullptr，表示不关心响应数据
 * @param[out] dataBuf
 * 响应数据缓存区，存放积极响应的诊断数据(不包含SID)，实际长度为resp.positive.data_len
 * @param[in] dataBufSize 响应数据缓存区总大小，如果小于响应诊断数据长度，返回
 * STATUS_BUFFER_TOO_SMALL
 * @return 执行结果状态
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_Request(DEVICE_HANDLE device_handle, const ZCAN_UDS_REQUEST *req,
                                           ZCAN_UDS_RESPONSE *resp, BYTE *dataBuf, UINT dataBufSize);

/**
 * @brief UDS诊断控制, 如停止正在执行的UDS请求 (DoCAN)
 * @param[in] device_handle 设备句柄
 * @param[in] ctrl 控制请求信息
 * @param[out] resp 响应信息，可为nullptr，表示不关心响应数据
 * @return 执行结果状态
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_Control(DEVICE_HANDLE device_handle, const ZCAN_UDS_CTRL_REQ *ctrl,
                                           ZCAN_UDS_CTRL_RESP *resp);

/**
 * @brief UDS诊断请求(总)
 * @param[in] device_handle 设备句柄
 * @param[in] requestData 请求信息
 * @param[out] resp 响应信息，可为nullptr，表示不关心响应数据
 * @param[out] dataBuf
 * 响应数据缓存区，存放积极响应的诊断数据(不包含SID)，实际长度为resp.positive.data_len
 * @param[in] dataBufSize 响应数据缓存区总大小，如果小于响应诊断数据长度，返回
 * STATUS_BUFFER_TOO_SMALL
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_RequestEX(DEVICE_HANDLE device_handle, const ZCANUdsRequestDataObj *requestData,
                                             ZCAN_UDS_RESPONSE *resp, BYTE *dataBuf, UINT dataBufSize);

/**
 * @brief UDS诊断控制，如停止正在执行的UDS请求(总)
 * @param[in] device_handle 设备句柄
 * @param[in] dataType 数据类型
 * @param[in] ctrl 控制请求信息
 * @param[out] resp 响应信息，可为nullptr，表示不关心响应数据
 * @return 执行结果状态
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_ControlEX(DEVICE_HANDLE device_handle, ZCAN_UDS_DATA_DEF dataType,
                                             const ZCAN_UDS_CTRL_REQ *ctrl, ZCAN_UDS_CTRL_RESP *resp);

/*已弃用*/
UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE *pLINID, UINT nIDCount);

#ifdef __cplusplus
}
#endif

#endif  // ZLGCAN_H_
