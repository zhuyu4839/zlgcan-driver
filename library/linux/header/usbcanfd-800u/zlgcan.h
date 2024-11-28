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
#define ZCAN_CANFDDTU_800ER_TCP             68
#define ZCAN_CANFDDTU_800ER_UDP             69
#define ZCAN_CANFDDTU_800EWGR_TCP           70
#define ZCAN_CANFDDTU_800EWGR_UDP           71
#define ZCAN_CANFDDTU_600EWGR_TCP           72
#define ZCAN_CANFDDTU_600EWGR_UDP           73
#define ZCAN_CANFDDTU_CASCADE_TCP           74
#define ZCAN_CANFDDTU_CASCADE_UDP           75
#define ZCAN_USBCANFD_400U                  76

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

typedef UINT ZCAN_RET_STATUS;
#define STATUS_ERR                          0
#define STATUS_OK                           1
#define STATUS_ONLINE                       2
#define STATUS_OFFLINE                      3
#define STATUS_UNSUPPORTED                  4
#define STATUS_BUFFER_TOO_SMALL             5

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

typedef struct tagZCAN_DEVICE_INFO {
    USHORT hw_Version;                      //Ӳ���汾
    USHORT fw_Version;                      //�̼��汾
    USHORT dr_Version;                      //�����汾
    USHORT in_Version;                      //��̬��汾
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

//�������ö�ʱ���Ͷ���Ĳ���, Ŀǰֻ֧��USBCANFD-X00Uϵ���豸
typedef struct tagZCAN_AUTO_TRANSMIT_OBJ_PARAM
{
    USHORT index;                           // ��ʱ����֡������
    USHORT type;                            // �������ͣ�Ŀǰ����ֻ��1����ʾ������ʱ
    UINT   value;                           // ������ֵ
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
    int     nWaitTime;                      //Wait Time ms, -1��ʾ�ȵ������ݲŷ���
}TxTimeStamp;

// Bus usage
typedef struct tagBusUsage
{
    UINT64  nTimeStampBegin;                //������ʼʱ�������λus
    UINT64  nTimeStampEnd;                  //��������ʱ�������λus
    BYTE    nChnl;                          //ͨ��
    BYTE    nReserved;                      //����
    USHORT  nBusUsage;                      //����������(%),����������*100չʾ��ȡֵ0~10000����8050��ʾ80.50%
    UINT    nFrameCount;                    //֡����
}BusUsage;

enum eZCANErrorDEF
{
    //���ߴ�������
    ZCAN_ERR_TYPE_NO_ERR                = 0,        //�޴���
    ZCAN_ERR_TYPE_BUS_ERR               = 1,        //���ߴ���
    ZCAN_ERR_TYPE_CONTROLLER_ERR        = 2,        //����������
    ZCAN_ERR_TYPE_DEVICE_ERR            = 3,        //�ն��豸����

    //�ڵ�״̬
    ZCAN_NODE_STATE_ACTIVE              = 1,        //���߻���
    ZCAN_NODE_STATE_WARNNING            = 2,        //���߸澯
    ZCAN_NODE_STATE_PASSIVE             = 3,        //��������
    ZCAN_NODE_STATE_BUSOFF              = 4,        //���߹ر�

    //���ߴ���������, errType = ZCAN_ERR_TYPE_BUS_ERR
    ZCAN_BUS_ERR_NO_ERR                 = 0,        //�޴���
    ZCAN_BUS_ERR_BIT_ERR                = 1,        //λ����
    ZCAN_BUS_ERR_ACK_ERR                = 2,        //Ӧ�����
    ZCAN_BUS_ERR_CRC_ERR                = 3,        //CRC����
    ZCAN_BUS_ERR_FORM_ERR               = 4,        //��ʽ����
    ZCAN_BUS_ERR_STUFF_ERR              = 5,        //������
    ZCAN_BUS_ERR_OVERLOAD_ERR           = 6,        //���ش���
    ZCAN_BUS_ERR_ARBITRATION_LOST       = 7,        //�ٲö�ʧ
    ZCAN_BUS_ERR_NODE_STATE_CHAGE       = 8,        //���߽ڵ�仯

    //����������, errType = ZCAN_ERR_TYPE_CONTROLLER_ERR
    ZCAN_CONTROLLER_RX_FIFO_OVERFLOW    = 1,        //����������FIFO���
    ZCAN_CONTROLLER_DRIVER_RX_BUFFER_OVERFLOW  = 2, //�������ջ������
    ZCAN_CONTROLLER_DRIVER_TX_BUFFER_OVERFLOW  = 3, //�������ͻ������
    ZCAN_CONTROLLER_INTERNAL_ERROR      = 4,        //�������ڲ�����

    //�ն��豸����, errType = ZCAN_ERR_TYPE_DEVICE_ERR
    ZCAN_DEVICE_APP_RX_BUFFER_OVERFLOW = 1,         //�ն�Ӧ�ý��ջ������
    ZCAN_DEVICE_APP_TX_BUFFER_OVERFLOW = 2,         //�ն�Ӧ�÷��ͻ������
    ZCAN_DEVICE_APP_AUTO_SEND_FAILED   = 3,         //��ʱ����ʧ��
    ZCAN_CONTROLLER_TX_FRAME_INVALID   = 4,         //���ͱ�����Ч
};

enum eZCANDataDEF
{
    //��������
    ZCAN_DT_ZCAN_CAN_CANFD_DATA     = 1,            // CAN/CANFD����
    ZCAN_DT_ZCAN_ERROR_DATA         = 2,            // ��������
    ZCAN_DT_ZCAN_GPS_DATA           = 3,            // GPS����
    ZCAN_DT_ZCAN_LIN_DATA           = 4,            // LIN����
    ZCAN_DT_ZCAN_BUSUSAGE_DATA      = 5,            // BusUsage����
    ZCAN_DT_ZCAN_LIN_ERROR_DATA     = 6,            // LIN��������

    //������ʱ��λ
    ZCAN_TX_DELAY_NO_DELAY          = 0,            // �޷�����ʱ
    ZCAN_TX_DELAY_UNIT_MS           = 1,            // ������ʱ��λ����
    ZCAN_TX_DELAY_UNIT_100US        = 2,            // ������ʱ��λ100΢��(0.1����)

};

#pragma pack(push, 1)

// CAN/CANFD����
typedef struct tagZCANCANFDData
{
    UINT64          timeStamp;                      // ʱ���,���ݽ���ʱ��λ΢��(us),������ʱ����ʱ,���ݵ�λȡ����flag.unionVal.txDelay
    union
    {
        struct{
            UINT    frameType : 2;                  // ֡����, 0:CAN֡, 1:CANFD֡
            UINT    txDelay : 2;                    // ���з�����ʱ, ������Ч. 0:�޷�����ʱ, 1:������ʱ��λms, 2:������ʱ��λ100us. ���ö��з�����ʱ����ʱʱ������timeStamp�ֶ�
            UINT    transmitType : 4;               // ��������, ������Ч. 0:��������, 1:���η���, 2:�Է�����, 3:�����Է�����. �����豸֧���������ͣ�����������ο�����ʹ���ֲ�
            UINT    txEchoRequest : 1;              // ���ͻ�������, ������Ч. ֧�ַ��ͻ��Ե��豸,��������ʱ����λ��1,�豸����ͨ�����սӿڽ����ͳ�ȥ������֡����,���յ��ķ�������ʹ��txEchoedλ���
            UINT    txEchoed : 1;                   // �����Ƿ��ǻ��Ա���, ������Ч. 0:�������߽��ձ���, 1:���豸���ͻ��Ա���.
            UINT    reserved : 22;                  // ����
        }unionVal;
        UINT    rawVal;                             // ֡��־λraw����
    }flag;                                          // CAN/CANFD֡��־λ
    BYTE        extraData[4];                       // ��������,��δʹ��
    canfd_frame frame;                              // can/canfd֡ID+����
}ZCANCANFDData;

// ��������
typedef struct tagZCANErrorData
{
    UINT64  timeStamp;                              // ʱ���, ��λ΢��(us)
    BYTE    errType;                                // ��������, �ο�eZCANErrorDEF�� ���ߴ������� ����ֵ����
    BYTE    errSubType;                             // ����������, �ο�eZCANErrorDEF�� ���ߴ��������� ����ֵ����
    BYTE    nodeState;                              // �ڵ�״̬, �ο�eZCANErrorDEF�� �ڵ�״̬ ����ֵ����
    BYTE    rxErrCount;                             // ���մ������
    BYTE    txErrCount;                             // ���ʹ������
    BYTE    errData;                                // ��������, �͵�ǰ���������Լ����������Ͷ���ľ���������, ������ο�ʹ���ֲ�
    BYTE    reserved[2];                            // ����
}ZCANErrorData;

// GPS����
typedef struct tagZCANGPSData
{
    struct {
        USHORT  year;                               // ��
        USHORT  mon;                                // ��
        USHORT  day;                                // ��
        USHORT  hour;                               // ʱ
        USHORT  min;                                // ��
        USHORT  sec;                                // ��
        USHORT  milsec;                             // ����
    }           time;                               // UTCʱ��
    union{
        struct{
            USHORT timeValid : 1;                   // ʱ�������Ƿ���Ч
            USHORT latlongValid : 1;                // ��γ�������Ƿ���Ч
            USHORT altitudeValid : 1;               // ���������Ƿ���Ч
            USHORT speedValid : 1;                  // �ٶ������Ƿ���Ч
            USHORT courseAngleValid : 1;            // ����������Ƿ���Ч
            USHORT reserved:13;                     // ����
        }unionVal;
        USHORT rawVal;
    }flag;                                          // ��־��Ϣ
    double latitude;                                // γ�� ������ʾ��γ, ������ʾ��γ
    double longitude;                               // ���� ������ʾ����, ������ʾ����
    double altitude;                                // ���� ��λ: ��
    double speed;                                   // �ٶ� ��λ: km/h
    double courseAngle;                             // �����
} ZCANGPSData;


// LIN����
typedef struct tagZCANLINData
{
    union {
        struct {
            BYTE    ID:6;                           // ֡ID
            BYTE    Parity:2;                       // ֡IDУ��
        }unionVal;
        BYTE    rawVal;                             // �ܱ�����IDԭʼֵ
    }       PID;                                    // �ܱ�����ID
    struct
    {
        UINT64  timeStamp;                          // ʱ�������λ΢��(us)
        BYTE    dataLen;                            // ���ݳ���
        BYTE    dir;                                // ���䷽��0-���� 1-����
        BYTE    chkSum;                             // ����У��, �����豸��֧��У�����ݵĻ�ȡ
        BYTE    reserved[13];                       // ����
        BYTE    data[8];                            // ����
    }RxData;                                        // ����������ʱ��Ч
	BYTE reserved[7];                               // ����
}ZCANLINData;

// ��������
typedef struct tagZCANLINErrData
{
	UINT64  timeStamp;                              // ʱ���, ��λ΢��(us)
	union {
		struct {
			BYTE    ID : 6;                           // ֡ID
			BYTE    Parity : 2;                       // ֡IDУ��
		}unionVal;
		BYTE    rawVal;                             // �ܱ�����IDԭʼֵ
	}       PID;                                    // �ܱ�����ID
	BYTE    dataLen;
	BYTE    data[8];
	union
	{
		struct
		{
			USHORT errStage : 4;                     // ����׶�
			USHORT errReason : 4;                    // ����ԭ��
			USHORT reserved : 8;                    // ����
		};
		USHORT unionErrData;
	}errData;
	BYTE    dir;                                    // ���䷽�� 
	BYTE    chkSum;                                 // ����У��, �����豸��֧��У�����ݵĻ�ȡ
	BYTE    reserved[10];                           // ����
}ZCANLINErrData;

// �ϲ������������ݽṹ��֧��CAN/CANFD/LIN/GPS/����Ȳ�ͬ��������
typedef struct tagZCANDataObj
{
    BYTE        dataType;                           // ��������, �ο�eZCANDataDEF�� �������� ���ֶ���
    BYTE        chnl;                               // ����ͨ��
    union{
        struct{
            USHORT reserved : 16;                   // ����
        }unionVal;
        USHORT rawVal;
    }flag;                                          // ��־��Ϣ, ��δʹ��
    BYTE        extraData[4];                       // ��������, ��δʹ��
    union
    {
        ZCANCANFDData           zcanCANFDData;      // CAN/CANFD����
        ZCANErrorData           zcanErrData;        // ��������
        ZCANGPSData             zcanGPSData;        // GPS����
        ZCANLINData             zcanLINData;        // LIN����
        ZCANLINErrData          zcanLINErrData;     // LIN��������
        BusUsage                busUsage;           // BusUsage����
        BYTE                    raw[92];            // RAW����
    } data;                                         // ʵ������, �����壬��Ч��Ա���� dataType �ֶζ���
}ZCANDataObj;

//LIN
typedef struct _VCI_LIN_MSG{
	BYTE        chnl;                               // ����ͨ��
	BYTE        dataType;                           // ��������, 0-LIN���� 1-LIN��������
	union
	{
		ZCANLINData             zcanLINData;        // LIN����
		ZCANLINErrData          zcanLINErrData;     // LIN��������
		BYTE                    raw[46];            // RAW����
	} data;                                         // ʵ������, �����壬��Ч��Ա���� dataType �ֶζ���
}ZCAN_LIN_MSG, *PZCAN_LIN_MSG;

enum eZLINChkSumMode
{
	DEFAULT = 0,                           // Ĭ�ϣ�����ʱ����
	CLASSIC_CHKSUM,                        // ����У��
	ENHANCE_CHKSUM,                        // ��ǿУ�� 
	AUTOMATIC,                             // �Զ����豸�Զ�ʶ��У�鷽ʽ����ZCAN_SetLINSubscribeʱ��Ч��
};
typedef struct _VCI_LIN_INIT_CONFIG
{
	BYTE    linMode;                       // �Ƿ���Ϊ������0-�ӻ���1-����
	BYTE    chkSumMode;                    // У�鷽ʽ��1-����У�� 2-��ǿУ�� 3-�Զ�(��ӦeZLINChkSumMode��ģʽ)
	USHORT  reserved;					   // ����
	UINT    linBaud;                       // �����ʣ�ȡֵ1000~20000
}ZCAN_LIN_INIT_CONFIG, *PZCAN_LIN_INIT_CONFIG;

typedef struct _VCI_LIN_PUBLISH_CFG
{
	BYTE    ID;                                     // �ܱ�����ID��IDȡֵ��ΧΪ0-63��
	BYTE    dataLen;                                // dataLen��ΧΪ1-8
	BYTE    data[8];
	BYTE    chkSumMode;                             // У�鷽ʽ��0-Ĭ�ϣ�����ʱ���� 1-����У�� 2-��ǿУ��(��ӦeZLINChkSumMode��ģʽ)
	BYTE    reserved[5];                            // ����
}ZCAN_LIN_PUBLISH_CFG, *PZCAN_LIN_PUBLISH_CFG;

typedef struct _VCI_LIN_SUBSCIBE_CFG
{
	BYTE    ID;                                     // �ܱ�����ID��IDȡֵ��ΧΪ0-63��
	BYTE    dataLen;                                // dataLen��ΧΪ1-8 ��Ϊ255��0xff�����ʾ�豸�Զ�ʶ���ĳ���
	BYTE    chkSumMode;                             // У�鷽ʽ��0-Ĭ�ϣ�����ʱ���� 1-����У�� 2-��ǿУ�� 3-�Զ�(��ӦeZLINChkSumMode��ģʽ)
	BYTE    reserved[5];                            // ����
}ZCAN_LIN_SUBSCIBE_CFG, *PZCAN_LIN_SUBSCIBE_CFG;

//end LIN


// UDS����Э��汾
typedef BYTE ZCAN_UDS_TRANS_VER;
#define ZCAN_UDS_TRANS_VER_0        0       // ISO15765-2(2004�汾)
#define ZCAN_UDS_TRANS_VER_1        1       // ISO15765-2(2016�汾)

// ֡����
typedef BYTE ZCAN_UDS_FRAME_TYPE;
#define ZCAN_UDS_FRAME_CAN          0       // CAN֡
#define ZCAN_UDS_FRAME_CANFD        1       // CANFD֡
#define ZCAN_UDS_FRAME_CANFD_BRS    2       // CANFD����֡

// UDS��������
typedef struct _ZCAN_UDS_REQUEST
{
    UINT req_id;                            // ��������ID����Χ0~65535�����������Ψһ��ʶ
    BYTE channel;                           // �豸ͨ������ 0~255
    ZCAN_UDS_FRAME_TYPE frame_type;         // ֡����
    BYTE reserved0[2];                      // ����
    UINT src_addr;                          // �����ַ
    UINT dst_addr;                          // ��Ӧ��ַ
    BYTE suppress_response;                 // 1:������Ӧ
    BYTE sid;                               // �������id
    BYTE reserved1[6];                      // ����
    struct {
        UINT timeout;                       // ��Ӧ��ʱʱ��(ms)����PC��ʱ�����������ò�С��200ms
        UINT enhanced_timeout;              // �յ�������Ӧ������Ϊ0x78��ĳ�ʱʱ��(ms)����PC��ʱ�����������ò�С��200ms
        BYTE check_any_negative_response:1; // ���յ��Ǳ�����������������Ӧʱ�Ƿ���Ҫ�ж�Ϊ��Ӧ����
        BYTE wait_if_suppress_response:1;   // ������Ӧʱ�Ƿ���Ҫ�ȴ�������Ӧ���ȴ�ʱ��Ϊ��Ӧ��ʱʱ��
        BYTE flag:6;                        // ����
        BYTE reserved0[7];                  // ����
    } session_param;                        // �Ự�����
    struct {
        ZCAN_UDS_TRANS_VER version;         // ����Э��汾, VERSION_0, VERSION_1
        BYTE max_data_len;                  // ��֡������ݳ���, can:8, canfd:64
        BYTE local_st_min;                  // ������������ʱ�ã�����֮֡�����С���, 0x00-0x7F(0ms~127ms), 0xF1-0xF9(100us~900us)
        BYTE block_size;                    // ����֡�Ŀ��С
        BYTE fill_byte;                     // ��Ч�ֽڵ��������
        BYTE ext_frame;                     // 0:��׼֡ 1:��չ֡
        BYTE is_modify_ecu_st_min;          // �Ƿ����ECU�������ص�STmin��ǿ��ʹ�ñ��������õ� remote_st_min
        BYTE remote_st_min;                 // ���Ͷ�֡ʱ��, is_ignore_ecu_st_min = 1 ʱ��Ч, 0x00-0x7F(0ms~127ms), 0xF1-0xF9(100us~900us)
        UINT fc_timeout;                    // �������س�ʱʱ��(ms), �緢����֡����Ҫ�ȴ���Ӧ����֡
        BYTE reserved0[4];                  // ����
    } trans_param;                          // ��������
    BYTE *data;                             // ��������(������SID)
    UINT data_len;                          // ��������ĳ���
    UINT reserved2;                         // ����
} ZCAN_UDS_REQUEST;

// UDS������
typedef BYTE ZCAN_UDS_ERROR;
#define ZCAN_UDS_ERROR_OK                   0    // û����
#define ZCAN_UDS_ERROR_TIMEOUT              1    // ��Ӧ��ʱ
#define ZCAN_UDS_ERROR_TRANSPORT            2    // ��������ʧ��
#define ZCAN_UDS_ERROR_CANCEL               3    // ȡ������
#define ZCAN_UDS_ERROR_SUPPRESS_RESPONSE    4    // ������Ӧ
#define ZCAN_UDS_ERROR_BUSY                 5    // æµ��
#define ZCAN_UDS_ERROR_REQ_PARAM            6    // �����������
#define ZCAN_UDS_ERROR_OTHTER               100

typedef BYTE ZCAN_UDS_RESPONSE_TYPE;
#define ZCAN_UDS_RT_NEGATIVE 0              // ������Ӧ
#define ZCAN_UDS_RT_POSITIVE 1              // ������Ӧ

// UDS��Ӧ���ݣ�ʹ�ú���Ҫ���� ZCAN_UDS_Release ���ͷ��ڴ�
typedef struct _ZCAN_UDS_RESPONSE
{
    ZCAN_UDS_ERROR status;                  // ��Ӧ״̬
    BYTE reserved[6];                       // ����
    ZCAN_UDS_RESPONSE_TYPE type;            // ��Ӧ����
    union {
        struct {
            BYTE sid;                       // ��Ӧ����id
            UINT data_len;                  // ���ݳ���(������SID), ���ݴ���ڽӿڴ����dataBuf��
        } positive;
        struct {
            BYTE  neg_code;                 // �̶�Ϊ0x7F
            BYTE  sid;                      // �������id
            BYTE  error_code;               // ������
        } negative;
        BYTE raw[8]; 
    };
} ZCAN_UDS_RESPONSE;

// UDS��������
typedef UINT ZCAN_UDS_CTRL_CODE;
#define ZCAN_UDS_CTRL_STOP_REQ 0            // ֹͣUDS����

// UDS��������
typedef struct _ZCAN_UDS_CTRL_REQ
{
    UINT reqID;                             // ��������ID��ָ��Ҫ������һ������
    ZCAN_UDS_CTRL_CODE cmd;                 // ��������
    BYTE reserved[8];                       // ����
} ZCAN_UDS_CTRL_REQ;

// UDS���ƽ��
typedef UINT ZCAN_UDS_CTRL_RESULT;
#define ZCAN_UDS_CTRL_RESULT_OK  0          // �ɹ�
#define ZCAN_UDS_CTRL_RESULT_ERR 1          // ʧ��

// UDS������Ӧ����
typedef struct _ZCAN_UDS_CTRL_RESP
{
    ZCAN_UDS_CTRL_RESULT result;            // �������
    BYTE reserved[8];                       // ����
} ZCAN_UDS_CTRL_RESP;



#pragma pack(pop)

#ifdef __cplusplus 
#define DEF(a) = a
#else 
#define DEF(a)
#endif 

#ifdef WIN32
#define FUNC_CALL __stdcall
#else
#define FUNC_CALL
#endif

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
// return 0:not connected, 1:connected
UINT FUNC_CALL ZCLOUD_IsConnected();
// return 0:success, 1:failure
UINT FUNC_CALL ZCLOUD_DisconnectServer();
const ZCLOUD_USER_DATA* FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
UINT FUNC_CALL ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));

CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT lin_index, PZCAN_LIN_INIT_CONFIG pLINInitConfig);
UINT FUNC_CALL ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
UINT FUNC_CALL ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len,int WaitTime);

UINT FUNC_CALL ZCAN_SetLINSubscribe(CHANNEL_HANDLE channel_handle, PZCAN_LIN_SUBSCIBE_CFG pSend, UINT nSubscribeCount);
UINT FUNC_CALL ZCAN_SetLINPublish(CHANNEL_HANDLE channel_handle, PZCAN_LIN_PUBLISH_CFG pSend, UINT nPublishCount);

/**
 * @brief UDS�������
 * @param[in] device_handle �豸���
 * @param[in] req ������Ϣ
 * @param[out] resp ��Ӧ��Ϣ, ��Ϊnullptr, ��ʾ��������Ӧ����
 * @param[out] dataBuf ��Ӧ���ݻ�����, ��Ż�����Ӧ���������(������SID), ʵ�ʳ���Ϊresp.positive.data_len
 * @param[out] dataBufSize ��Ӧ���ݻ������ܴ�С�����С����Ӧ������ݳ��ȣ����� STATUS_BUFFER_TOO_SMALL
 * @return ִ�н��״̬
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_Request(DEVICE_HANDLE device_handle, const ZCAN_UDS_REQUEST* req, ZCAN_UDS_RESPONSE* resp, BYTE* dataBuf, UINT dataBufSize);

/**
 * @brief UDS��Ͽ���, ��ֹͣ����ִ�е�UDS����
 * @param[in] device_handle �豸���
 * @param[in] ctrl ����������Ϣ
 * @param[out] resp ��Ӧ��Ϣ, ��Ϊnullptr, ��ʾ��������Ӧ����
 * @return ִ�н��״̬
 */
ZCAN_RET_STATUS FUNC_CALL ZCAN_UDS_Control(DEVICE_HANDLE device_handle, const ZCAN_UDS_CTRL_REQ *ctrl, ZCAN_UDS_CTRL_RESP* resp);

/*������*/
UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE* pLINID, UINT nIDCount);

#ifdef __cplusplus
}
#endif

#endif //ZLGCAN_H_
