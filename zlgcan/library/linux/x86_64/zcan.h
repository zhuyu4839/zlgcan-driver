#pragma once

#ifdef __cplusplus
#define EXTERN_C  extern "C"
#else
#define EXTERN_C
#endif

#define ZCAN_API
#define INVALID_HANDLE_VALUE  ((HANDLE)(-1))

typedef unsigned char U8;
typedef unsigned short U16;
typedef unsigned int U32;
typedef unsigned long long U64;

#pragma pack(push, 1)

typedef enum {
    ZCAN_TX_NORM = 0, /**< normal transmission */
    ZCAN_TX_ONCE = 1, /**< single-shot transmission */
    ZCAN_SR_NORM = 2, /**< self reception */
    ZCAN_SR_ONCE = 3, /**< single-shot transmission & self reception */
} ZCAN_TX_MODE;

/** CAN filter configuration */
typedef struct {
    U8 type; /**< 0-std_frame, 1-ext_frame */
    U8 pad[3];
    U32 sid; /**< start-id */
    U32 eid; /**< end-id */
} ZCAN_FILTER;

/** controller initialization */
typedef struct {
    U32 clk; /**< clock(Hz) */
    U32 mode; /**< bit0-normal/listen_only, bit1-ISO/BOSCH */
    struct {
        U8 tseg1;
        U8 tseg2;
        U8 sjw;
        U8 smp;
        U16 brp;
    } aset;
    struct {
        U8 tseg1;
        U8 tseg2;
        U8 sjw;
        U8 smp;
        U16 brp;
    } dset;
} ZCAN_INIT;

/** CAN message info */
typedef struct {
    U32 txm : 4; /**< TX-mode, @see ZCAN_TX_MODE */
    U32 fmt : 4; /**< 0-CAN2.0, 1-CANFD */
    U32 sdf : 1; /**< 0-data_frame, 1-remote_frame */
    U32 sef : 1; /**< 0-std_frame, 1-ext_frame */
    U32 err : 1; /**< error flag */
    U32 brs : 1; /**< bit-rate switch */
    U32 est : 1; /**< error state */
    U32 pad : 19;
} ZCAN_MSG_INF;

/** CAN message header */
typedef struct {
    U32 ts; /**< timestamp */
    U32 id; /**< CAN-ID */
    ZCAN_MSG_INF inf; /**< @see ZCAN_MSG_INF */
    U16 pad;
    U8 chn; /**< channel */
    U8 len; /**< data length */
} ZCAN_MSG_HDR;

/** CAN2.0-frame */
typedef struct {
    ZCAN_MSG_HDR hdr;
    U8 dat[8];
} ZCAN_20_MSG;

/** CANFD-frame */
typedef struct {
    ZCAN_MSG_HDR hdr;
    U8 dat[64];
} ZCAN_FD_MSG;

/** CANERR-frame */
typedef struct {
    ZCAN_MSG_HDR hdr;
    U8 dat[8];
} ZCAN_ERR_MSG;

/** device info */
typedef struct {
    U16 hwv; /**< hardware version */
    U16 fwv; /**< firmware version */
    U16 drv; /**< driver version */
    U16 api; /**< API version */
    U16 irq; /**< IRQ */
    U8 chn; /**< channels */
    U8 sn[20]; /**< serial number */
    U8 id[40]; /**< card id */
    U16 pad[4];
} ZCAN_DEV_INF;

/** controller status */
typedef struct {
    U8 IR; /**< not used(for backward compatibility) */
    U8 MOD; /**< not used */
    U8 SR; /**< not used */
    U8 ALC; /**< not used */
    U8 ECC; /**< not used */
    U8 EWL; /**< not used */
    U8 RXE; /**< RX errors */
    U8 TXE; /**< TX errors */
    U32 PAD;
} ZCAN_STAT;

#pragma pack(pop)

EXTERN_C U32 ZCAN_API VCI_OpenDevice(U32 Type, U32 Card, U32 Reserved);
EXTERN_C U32 ZCAN_API VCI_CloseDevice(U32 Type, U32 Card);
EXTERN_C U32 ZCAN_API VCI_InitCAN(U32 Type, U32 Card, U32 Port, ZCAN_INIT *pInit);
EXTERN_C U32 ZCAN_API VCI_ReadBoardInfo(U32 Type, U32 Card, ZCAN_DEV_INF *pInfo);
EXTERN_C U32 ZCAN_API VCI_ReadErrInfo(U32 Type, U32 Card, U32 Port, ZCAN_ERR_MSG *pErr);
EXTERN_C U32 ZCAN_API VCI_ReadCANStatus(U32 Type, U32 Card, U32 Port, ZCAN_STAT *pStat);
EXTERN_C U32 ZCAN_API VCI_GetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
EXTERN_C U32 ZCAN_API VCI_SetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
EXTERN_C U32 ZCAN_API VCI_GetReceiveNum(U32 Type, U32 Card, U32 Port);
EXTERN_C U32 ZCAN_API VCI_ClearBuffer(U32 Type, U32 Card, U32 Port);
EXTERN_C U32 ZCAN_API VCI_StartCAN(U32 Type, U32 Card, U32 Port);
EXTERN_C U32 ZCAN_API VCI_ResetCAN(U32 Type, U32 Card, U32 Port);
EXTERN_C U32 ZCAN_API VCI_Transmit(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count);
EXTERN_C U32 ZCAN_API VCI_TransmitFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count);
EXTERN_C U32 ZCAN_API VCI_Receive(U32 Type, U32 Card, U32 Port, ZCAN_20_MSG *pData, U32 Count, U32 Time);
EXTERN_C U32 ZCAN_API VCI_ReceiveFD(U32 Type, U32 Card, U32 Port, ZCAN_FD_MSG *pData, U32 Count, U32 Time);
EXTERN_C U32 ZCAN_API VCI_Debug(U32 Debug);
