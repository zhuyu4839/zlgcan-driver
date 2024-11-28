#ifndef ZLGCAN_H_
#define ZLGCAN_H_
#include <time.h>
#include"canframe.h"
#include "config.h"

//接口卡类型定义
#define ZCAN_PCI5121         1
#define ZCAN_PCI9810         2
#define ZCAN_USBCAN1         3
#define ZCAN_USBCAN2         4
#define ZCAN_USBCAN2A        4
#define ZCAN_PCI9820         5
#define ZCAN_CAN232          6
#define ZCAN_PCI5110         7
#define ZCAN_CANLITE         8
#define ZCAN_ISA9620         9
#define ZCAN_ISA5420         10
#define ZCAN_PC104CAN        11
#define ZCAN_CANETUDP        12
#define ZCAN_CANETE          12
#define ZCAN_DNP9810         13
#define ZCAN_PCI9840         14
#define ZCAN_PC104CAN2       15
#define ZCAN_PCI9820I        16
#define ZCAN_CANETTCP        17
#define ZCAN_PEC9920         18
#define ZCAN_PCIE_9220       18
#define ZCAN_PCI5010U        19
#define ZCAN_USBCAN_E_U      20
#define ZCAN_USBCAN_2E_U     21
#define ZCAN_PCI5020U        22
#define ZCAN_EG20T_CAN       23
#define ZCAN_PCIE9221        24
#define ZCAN_WIFICAN_TCP     25
#define ZCAN_WIFICAN_UDP     26
#define ZCAN_PCIe9120        27
#define ZCAN_PCIe9110        28
#define ZCAN_PCIe9140        29
#define ZCAN_USBCAN_4E_U     31
#define ZCAN_CANDTU          32
#define ZCAN_CANDTU_MINI     33
#define ZCAN_USBCAN_8E_U     34
#define ZCAN_CANREPLAY       35
#define ZCAN_CANDTU_NET      36
#define ZCAN_CANDTU_100UR    37
#define ZCAN_PCIE_CANFD_100U 38
#define ZCAN_PCIE_CANFD_200U 39
#define ZCAN_PCIE_CANFD_400U 40

#define ZCAN_VIRTUAL_DEVICE  99 //虚拟设备

//CAN错误码
#define ERR_CAN_OVERFLOW            0x0001 //CAN控制器内部FIFO溢出
#define ERR_CAN_ERRALARM            0x0002 //CAN控制器错误报警
#define	ERR_CAN_PASSIVE             0x0004 //CAN控制器消极错误
#define	ERR_CAN_LOSE                0x0008 //CAN控制器仲裁丢失
#define	ERR_CAN_BUSERR              0x0010 //CAN控制器总线错误
#define ERR_CAN_BUSOFF              0x0020 //总线关闭错误
#define ERR_CAN_BUFFER_OVERFLOW     0x0040 //CAN控制器内部BUFFER溢出
//通用错误码
#define	ERR_DEVICEOPENED            0x0100 //设备已经打开
#define	ERR_DEVICEOPEN              0x0200 //打开设备错误
#define	ERR_DEVICENOTOPEN           0x0400 //设备没有打开
#define	ERR_BUFFEROVERFLOW          0x0800 //缓冲区溢出
#define	ERR_DEVICENOTEXIST          0x1000 //此设备不存在
#define	ERR_LOADKERNELDLL           0x2000 //装载动态库失败
#define ERR_CMDFAILED               0x4000 //执行命令失败错误码
#define	ERR_BUFFERCREATE            0x8000 //内存不足

//CANET错误码
#define ERR_CANETE_PORTOPENED       0x00010000 //端口已经被打开
#define ERR_CANETE_INDEXUSED        0x00020000 //设备索引号已经被占用
#define ERR_REF_TYPE_ID             0x00030001 //SetReference或GetReference传递的RefType不存在
#define ERR_CREATE_SOCKET           0x00030002 //创建Socket失败
#define ERR_OPEN_CONNECT            0x00030003 //打开Socket的连接时失败，可能设备连接已经存在
#define ERR_NO_STARTUP              0x00030004 //设备没启动
#define ERR_NO_CONNECTED            0x00030005 //设备无连接
#define ERR_SEND_PARTIAL            0x00030006 //只发送了部分的CAN帧
#define ERR_SEND_TOO_FAST           0x00030007 //数据发得太快，Socket缓冲区满了

//函数调用返回状态值
#define	STATUS_OK                   1
#define STATUS_ERR                  0

#define CMD_DESIP                   0
#define CMD_DESPORT                 1
#define CMD_CHGDESIPANDPORT         2
#define CMD_SRCPORT                 2
#define CMD_TCP_TYPE                4 //tcp 工作方式，服务器:1 或是客户端:0
#define TCP_CLIENT                  0
#define TCP_SERVER                  1
//服务器方式下有效
#define CMD_CLIENT_COUNT            5 //连接上的客户端计数
#define CMD_CLIENT                  6 //连接上的客户端
#define CMD_DISCONN_CLINET          7 //断开一个连接
#define CMD_SET_RECONNECT_TIME      8 //使能自动重连

#define TYPE_CAN   0
#define TYPE_CANFD 1

typedef unsigned char    BYTE;
//typedef unsigned int     UINT;
typedef unsigned long long UINT64;
typedef int              INT;
//typedef unsigned short   USHORT;
//typedef unsigned char    UCHAR;

typedef void * DEVICE_HANDLE;
typedef void * CHANNEL_HANDLE;

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
    UINT can_type; // 0:can 1:canfd
    union
    {
        struct
        {
            UINT  acc_code; // 验收码
            UINT  acc_mask; // 屏蔽码
            UINT  reserved; // 保留
            BYTE  filter;   // 0-双验收, 1-单验收
            BYTE  timing0;  // 定时器0
            BYTE  timing1;  // 定时器1
            BYTE  mode;     // 0-正常, 1-只听
        }can;
        struct
        {
            UINT   acc_code; // 验收码
            UINT   acc_mask; // 屏蔽码
            UINT   timing0;  // 仲裁域定时器
            UINT   timing1;  // 数据域定时器
            UINT   brp;      // 波特率预分频因子
            BYTE   filter;   // 0-双验收, 1-单验收
            BYTE   mode;     // 0-正常, 1-只听
            USHORT pad;      // 对齐
            UINT   reserved; // 保留
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
    can_frame frame;
    UINT transmit_type;//0:正常发送, 1:单次发送, 2:自发自收, 3:单次自发自收
}ZCAN_Transmit_Data;

typedef struct tagZCAN_Receive_Data
{
    can_frame frame;
    UINT64    timestamp;       //单位为微秒
}ZCAN_Receive_Data;

typedef struct tagZCAN_TransmitFD_Data
{
    canfd_frame frame;
    UINT transmit_type;
}ZCAN_TransmitFD_Data;

typedef struct tagZCAN_ReceiveFD_Data
{
    canfd_frame frame;
    UINT64      timestamp;       //单位为微秒
}ZCAN_ReceiveFD_Data;

//CAN定时自动发送帧结构
typedef struct tagZCAN_AUTO_TRANSMIT_OBJ{
    USHORT enable;//使能本条报文.  0：禁能   1：使能
    USHORT index;  //报文编号, 0...
    UINT   interval;//定时发送时间。1ms为单位
    ZCAN_Transmit_Data obj;//报文
}ZCAN_AUTO_TRANSMIT_OBJ, *PZCAN_AUTO_TRANSMIT_OBJ;

//CANFD定时自动发送帧结构
typedef struct tagZCANFD_AUTO_TRANSMIT_OBJ{
    UINT interval;//定时发送时间。1ms为单位
    ZCAN_TransmitFD_Data obj;//报文
}ZCANFD_AUTO_TRANSMIT_OBJ, *PZCANFD_AUTO_TRANSMIT_OBJ;

#ifdef __cplusplus
extern "C"
{
#endif
//设备对象
#define INVALID_DEVICE_HANDLE 0
DEVICE_HANDLE ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
INT ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
INT ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);

//can通道对象
#define INVALID_CHANNEL_HANDLE 0
CHANNEL_HANDLE ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
INT ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
INT ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
INT ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
INT ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
INT ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
INT ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
INT ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);
INT ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, INT wait_time);
INT ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
INT ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, INT wait_time);

IProperty* GetIProperty(DEVICE_HANDLE device_handle);   //获取属性接口
INT ReleaseIProperty(IProperty * pIProperty);

#ifdef __cplusplus
}
#endif

#endif //ZLGCAN_H_
