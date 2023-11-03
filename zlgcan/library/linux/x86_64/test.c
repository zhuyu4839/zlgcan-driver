#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <pthread.h>
#include "zcan.h"

#define msleep(ms)  usleep((ms)*1000)
#define min(a,b)  (((a) < (b)) ? (a) : (b))

#define CANFD_TEST  1

#define MAX_CHANNELS  4
#define CHECK_POINT  200
#define RX_WAIT_TIME  100
#define RX_BUFF_SIZE  1000

unsigned gDevType = 0;
unsigned gDevIdx = 0;
unsigned gChMask = 0;
unsigned gTxType = 0;
unsigned gTxSleep = 0;
unsigned gTxFrames = 0;
unsigned gTxCount = 0;
unsigned gDebug = 0;

unsigned s2n(const char *s)
{
    unsigned l = strlen(s);
    unsigned v = 0;
    unsigned h = (l > 2 && s[0] == '0' && (s[1] == 'x' || s[1] == 'X'));
    unsigned char c;
    unsigned char t;
    if (!h) return atoi(s);
    if (l > 10) return 0;
    for (s += 2; c = *s; s++) {
        if (c >= 'A' && c <= 'F') c += 32;
        if (c >= '0' && c <= '9') t = c - '0';
        else if (c >= 'a' && c <= 'f') t = c - 'a' + 10;
        else return 0;
        v = (v << 4) | t;
    }
    return v;
}

U8 len_to_dlc(U8 len)
{
    if (len < 8) return len;
    U8 idx = ((len - 8) >> 2) & 0x0f;
    static const U8 tbl[16] = {
        8, 9, 10, 11, 12, 0,
        13, 0, 0, 0,
        14, 0, 0, 0,
        15, 0
    };
    return tbl[idx];
}

U8 dlc_to_len(U8 dlc)
{
    static const U8 tbl[16] = {
        0, 1, 2, 3, 4, 5, 6, 7, 
        8, 12, 16, 20, 24, 32, 48, 64
    };
    return tbl[dlc & 0x0f];
}

#if CANFD_TEST
void generate_frame(U8 chn, ZCAN_FD_MSG *can)
{
    U8 i, dlc = rand() % 16; // random data length（0~64）
    memset(can, 0, sizeof(ZCAN_FD_MSG));
    can->hdr.inf.fmt = 1; // canfd
    can->hdr.inf.brs = 1; // 1M+4M
#else
void generate_frame(U8 chn, ZCAN_20_MSG *can)
{
    U8 i, dlc = rand() % 9; // random data length（0~8）
    memset(can, 0, sizeof(ZCAN_20_MSG));
    can->hdr.inf.fmt = 0; // can2.0
    can->hdr.inf.brs = 0; // 1M+1M
#endif
    can->hdr.inf.txm = gTxType;
    can->hdr.inf.sdf = 0; // data frame
    can->hdr.inf.sef = rand() % 2; // random std/ext frame
    can->hdr.chn = chn;
    can->hdr.len = dlc_to_len(dlc);
    for (i = 0; i < can->hdr.len; i++) {
        can->dat[i] = rand() & 0x7f; // random data
        can->hdr.id ^= can->dat[i]; // id: bit0~6, checksum of data0~N
    }
    can->hdr.id |= (U32)dlc << 7; // id: bit7~bit10 = encoded_dat_len
    if (!can->hdr.inf.sef)
        return;
    can->hdr.id |= can->hdr.id << 11; // id: bit11~bit21 == bit0~bit10
    can->hdr.id |= can->hdr.id << 11; // id: bit22~bit28 == bit0~bit7
}

#if CANFD_TEST
int verify_frame(ZCAN_FD_MSG *can)
#else
int verify_frame(ZCAN_20_MSG *can)
#endif
{
    unsigned i;
    unsigned bcc = 0;
    // fixme
    //return 1;
    if (can->hdr.len > 64) return -1; // error: data length
    for (i = 0; i < can->hdr.len; i++)
        bcc ^= can->dat[i];
    if ((can->hdr.id & 0x7f) != (bcc & 0x7f)) return -2; // error: data checksum
    if (((can->hdr.id >> 7) & 0x0f) != len_to_dlc(can->hdr.len)) return -3; // error: data length
    if (!can->hdr.inf.sef) return 1; // std-frame ok
    if (((can->hdr.id >> 11) & 0x7ff) != (can->hdr.id & 0x7ff)) return -4; // error: frame id
    if (((can->hdr.id >> 22) & 0x7f) != (can->hdr.id & 0x7f)) return -5; // error: frame id
    return 1; // ext-frame ok
}

typedef struct {
    unsigned channel; // channel index, 0~3
    unsigned stop; // stop RX-thread
    unsigned total; // total received
    unsigned error; // error(s) detected
} THREAD_CTX;

void* rx_thread(void *data)
{
    THREAD_CTX *ctx = (THREAD_CTX *)data;
    ctx->total = 0; // reset counter

#if CANFD_TEST
    ZCAN_FD_MSG buff[RX_BUFF_SIZE]; // buffer
#else
    ZCAN_20_MSG buff[RX_BUFF_SIZE]; // buffer
#endif
    int cnt; // current received
    int i;

    unsigned check_point = 0;
    while (!ctx->stop && !ctx->error)
    {
#if CANFD_TEST
        cnt = VCI_ReceiveFD(gDevType, gDevIdx, ctx->channel, buff, RX_BUFF_SIZE, RX_WAIT_TIME);
#else
        cnt = VCI_Receive(gDevType, gDevIdx, ctx->channel, buff, RX_BUFF_SIZE, RX_WAIT_TIME);
#endif
        if (!cnt)
            continue;

        for (i = 0; i < cnt; i++) {
            int ret = verify_frame(&buff[i]);
            if (ret > 0) continue;
            printf("CAN%d: RX: verify_frame() failed: ret=%d\n", ctx->channel, ret);
            ctx->error = 1;
            break;
        }
        if (ctx->error) break;

        ctx->total += cnt;
        if (ctx->total / CHECK_POINT >= check_point) {
            printf("CAN%d: RX: %d frames received & verified\n", ctx->channel, ctx->total);
            check_point++;
        }
    }

    printf("CAN%d: RX: rx-thread terminated, %d frames received & verified: %s\n",
        ctx->channel, ctx->total, ctx->error ? "error(s) detected" : "no error");

    pthread_exit(0);
    return NULL;
}

void* tx_thread(void *data)
{
    THREAD_CTX *ctx = (THREAD_CTX *)data;
    int port = ctx->channel;
    time_t tm1, tm2;
    unsigned tx;
    int j;

    ctx->total = 0; // reset counter

    if ((gChMask & (1 << port)) == 0) {
        pthread_exit(0);
        return NULL;
    }

#if CANFD_TEST
    int msgsz = sizeof(ZCAN_FD_MSG);
    ZCAN_FD_MSG *buff = (ZCAN_FD_MSG *)malloc(msgsz * gTxFrames);
#else
    int msgsz = sizeof(ZCAN_20_MSG);
    ZCAN_20_MSG *buff = (ZCAN_20_MSG *)malloc(msgsz * gTxFrames);
#endif
    if (buff) {
        memset(buff, 0, msgsz * gTxFrames);
        time(&tm1);
        for (tx = 0; !ctx->error && tx < gTxCount; tx++) {
            for (j = 0; j < gTxFrames; j++)
                generate_frame(port, &buff[j]);
#if CANFD_TEST
            if (gTxFrames != VCI_TransmitFD(gDevType, gDevIdx, port, buff, gTxFrames))
#else
            if (gTxFrames != VCI_Transmit(gDevType, gDevIdx, port, buff, gTxFrames))
#endif
            {
                printf("CAN%d TX failed: ID=%08x\n", port, buff->hdr.id);
                ctx->error = 1;
                break;
            }
            ctx->total += gTxFrames;
            if (gTxSleep) msleep(gTxSleep);
        }
        time(&tm2);
        free(buff);
    }
    else ctx->error = -1;

    if (!ctx->error) {
        printf("CAN%d: TX: %d frames sent, %ld seconds elapsed\n",
            port, gTxFrames * gTxCount, tm2 - tm1);
        if (tm2 - tm1)
            printf("CAN%d: TX: %ld frames/second\n", port, gTxFrames * gTxCount / (tm2 - tm1));
    }

    pthread_exit(0);
    return NULL;
}

int test()
{
    // ----- device info --------------------------------------------------

    ZCAN_DEV_INF info;
    memset(&info, 0, sizeof(info));
    VCI_ReadBoardInfo(gDevType, gDevIdx, &info);
    char sn[21];
    char id[41];
    memcpy(sn, info.sn, 20);
    memcpy(id, info.id, 40);
    sn[20] = '\0';
    id[40] = '\0';
    printf("HWV=0x%04x, FWV=0x%04x, DRV=0x%04x, API=0x%04x, IRQ=0x%04x, CHN=0x%02x, SN=%s, ID=%s\n",
        info.hwv, info.fwv, info.drv, info.api, info.irq, info.chn, sn, id);

    // ----- init & start -------------------------------------------------

    ZCAN_INIT init;
    init.clk = 60000000; // clock: 60M
    init.mode = 0;
#if CANFD_TEST
    init.aset.tseg1 = 46; // 1M
    init.aset.tseg2 = 11;
    init.aset.sjw = 3;
    init.aset.smp = 0;
    init.aset.brp = 0;
    init.dset.tseg1 = 10; // 4M
    init.dset.tseg2 = 2;
    init.dset.sjw = 2;
    init.dset.smp = 0;
    init.dset.brp = 0;
#else
    init.aset.tseg1 = 46; // 1M
    init.aset.tseg2 = 11;
    init.aset.sjw = 3;
    init.aset.smp = 0;
    init.aset.brp = 2;
    init.dset.tseg1 = 14; // 1M
    init.dset.tseg2 = 3;
    init.dset.sjw = 3;
    init.dset.smp = 0;
    init.dset.brp = 0;
#endif

    int i;
    for (i = 0; i < MAX_CHANNELS; i++) {
        if ((gChMask & (1 << i)) == 0) continue;

        if (!VCI_InitCAN(gDevType, gDevIdx, i, &init)) {
            printf("VCI_InitCAN(%d) failed\n", i);
            return 0;
        }
        printf("VCI_InitCAN(%d) succeeded\n", i);

        if (!VCI_StartCAN(gDevType, gDevIdx, i)) {
            printf("VCI_StartCAN(%d) failed\n", i);
            return 0;
        }
        printf("VCI_StartCAN(%d) succeeded\n", i);
    }

    // ----- Settings -----------------------------------------------------

    enum {
        CMD_CAN_FILTER = 0x14,
        CMD_CAN_TRES = 0x18,
        CMD_CAN_TX_TIMEOUT = 0x44,
        CMD_CAN_TTX = 0x16,
        CMD_CAN_TTX_CTL = 0x17,
    };

    // transmit timeout
    U32 tx_timeout = 2000; // 2 seconds
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TX_TIMEOUT, &tx_timeout)) {
        printf("CMD_CAN_TX_TIMEOUT failed\n");
    }

    // terminal resistor
    U32 on = 1;
    // EXTERN_C U32 ZCAN_API VCI_SetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TRES, &on)) {
        printf("CMD_CAN_TRES failed\n");
    }
    
    U32 res = 0;
    // EXTERN_C U32 ZCAN_API VCI_GetReference(U32 Type, U32 Card, U32 Port, U32 Ref, void *pData);
    if (!VCI_GetReference(gDevType, gDevIdx, 0, CMD_CAN_TRES, &res)) {
        printf("CMD_CAN_TRES result: %d\n", res);
    }

#if 0
    // filter
    struct {
        U32 size;
        ZCAN_FILTER table[64];
    } filter = {
        sizeof(ZCAN_FILTER) * 3,
        {
            { 0, {0}, 0x100, 0x111 },
            { 1, {0}, 0x200, 0x222 },
            { 1, {0}, 0x300, 0x333 },
        }
    };
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_FILTER, &filter)) {
        printf("CMD_CAN_FILTER failed\n");
    }

    // terminal resistor
    U32 on = 1;
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TRES, &on)) {
        printf("CMD_CAN_TRES failed\n");
    }
    
    // transmit timeout
    U32 tx_timeout = 2000; // 2 seconds
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TX_TIMEOUT, &tx_timeout)) {
        printf("CMD_CAN_TX_TIMEOUT failed\n");
    }

    // timed tx
    typedef struct {
        U32 interval;
        U16 repeat;
        U8 index;
        U8 flags;
        ZCAN_FD_MSG msg;
    } ZCAN_TTX;
    struct {
        U32 size;
        ZCAN_TTX table[8];
    } ttx_cfg = {
        sizeof(ZCAN_TTX) * 3, // 3 frames to config
        {
            {
                2, // 200us
                0, // send repeatedly
                0, // 1st item of tx-table
                1, // enabled
                {
                    {0, 0x111, {0}, 0, 0, 4}, // hdr
                    {0x11,0x22,0x33,0x44} // dat
                }
            },
            {
                5, // 500us
                10, // send 10 frames
                1, // 2nd item of tx-table
                1, // enabled
                {
                    {0, 0x222, {0}, 0, 0, 8}, // hdr
                    {0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88} // dat
                }
            },
            {
                1000, // 1ms
                3, // send 3 frames
                2, // 3rd item of tx-table
                1, // enabled
                {
                    {0, 0x333, {0}, 0, 0, 8}, // hdr
                    {0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88} // dat
                }
            },
        }
    };
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TTX, &ttx_cfg)) {
        printf("CMD_CAN_TTX failed\n");
    }
    U32 ttx_run = 1;
    if (!VCI_SetReference(gDevType, gDevIdx, 0, CMD_CAN_TTX_CTL, &ttx_run)) {
        printf("CMD_CAN_TTX_CTL failed\n");
    }
#endif

    // ----- RX-timeout test ----------------------------------------------

    ZCAN_FD_MSG can;
    time_t tm1, tm2;
#if 0
    for (i = 0; i < 3; i++) {
        time(&tm1);
        VCI_ReceiveFD(gDevType, gDevIdx, 0, &can, 1, (i + 1) * 1000/*ms*/);
        time(&tm2);
        printf("VCI_Receive returned: time ~= %ld seconds\n", tm2 - tm1);
    }
#endif

    // ----- create RX-threads --------------------------------------------

    THREAD_CTX rx_ctx[MAX_CHANNELS];
    pthread_t rx_threads[MAX_CHANNELS];
    for (i = 0; i < MAX_CHANNELS; i++) {
        if ((gChMask & (1 << i)) == 0) continue;

        rx_ctx[i].channel = i;
        rx_ctx[i].stop = 0;
        rx_ctx[i].total = 0;
        rx_ctx[i].error = 0;
        pthread_create(&rx_threads[i], NULL, rx_thread, &rx_ctx[i]);
    }

    // ----- wait --------------------------------------------------------

    printf("<ENTER> to start TX: %d*%d frames/channel ...\n", gTxFrames, gTxCount);
    getchar();

    // ----- start transmit -----------------------------------------------

    THREAD_CTX tx_ctx[MAX_CHANNELS];
    pthread_t tx_threads[MAX_CHANNELS];
    for (i = 0; i < MAX_CHANNELS; i++) {
        if ((gChMask & (1 << i)) == 0) continue;

        tx_ctx[i].channel = i;
        tx_ctx[i].stop = 0;
        tx_ctx[i].total = 0;
        tx_ctx[i].error = 0;
        pthread_create(&tx_threads[i], NULL, tx_thread, &tx_ctx[i]);
    }

    // ----- stop TX & RX -------------------------------------------------

    int err = 0;
    for (i = 0; i < MAX_CHANNELS; i++) {
        if ((gChMask & (1 << i)) == 0) continue;
        pthread_join(tx_threads[i], NULL);
        if (tx_ctx[i].error)
            err = 1;
    }

    sleep(2);
    printf("<ENTER> to stop RX ...\n");
    getchar();

    for (i = 0; i < MAX_CHANNELS; i++) {
        if ((gChMask & (1 << i)) == 0) continue;
        rx_ctx[i].stop = 1;
        pthread_join(rx_threads[i], NULL);
        if (rx_ctx[i].error)
            err = 1;
    }

    // ----- report -------------------------------------------------------

    printf(err ? "error(s) detected, test failed\n" : "test succeeded\n");

    while (1) {
        ZCAN_ERR_MSG err;
        if (!VCI_ReadErrInfo(gDevType, gDevIdx, 0, &err)) break;
        printf("err=%02x %02x %02x %02x %02x\n", err.dat[0],err.dat[1],err.dat[2],err.dat[3],err.dat[4]);
    }
    return !err;
}

int main(int argc, char* argv[])
{
    if (argc < 9) {
        printf("test [DevType] [DevIdx] [ChMask] [TxType] [TxSleep] [TxFrames] [TxCount] [Debug]\n"
            "    example: test 33 0 3 2 3 10 1000 0\n"
            "                  |  | | | | |  | 1000 times\n"
            "                  |  | | | | |\n"
            "                  |  | | | | |10 frames once\n"
            "                  |  | | | |\n"
            "                  |  | | | |tx > sleep(3ms) > tx > sleep(3ms) ....\n"
            "                  |  | | |\n"
            "                  |  | | |0-normal, 1-single, 2-self_test, 3-single_self_test, 4-single_no_wait....\n"
            "                  |  | |\n"
            "                  |  | |bit0-CAN1, bit1-CAN2, bit2-CAN3, bit3-CAN4, 3=CAN1+CAN2, 7=CAN1+CAN2+CAN3\n"
            "                  |  |\n"
            "                  |  |Card0\n"
            "                  |\n"
            "                  |4-usbcan-ii, 5-pci9820, 14-pci9840, 16-pci9820i, 33-usbcanfd....\n"
            );
        return 0;
    }

    gDevType = s2n(argv[1]);
    gDevIdx = s2n(argv[2]);
    gChMask = s2n(argv[3]);
    gTxType = s2n(argv[4]);
    gTxSleep = s2n(argv[5]);
    gTxFrames = s2n(argv[6]);
    gTxCount = s2n(argv[7]);
    gDebug = s2n(argv[8]);
    printf("DevType=%d, DevIdx=%d, ChMask=0x%x, TxType=%d, TxSleep=%d, TxFrames=0x%08x(%d), TxCount=0x%08x(%d), Debug=%d\n",
        gDevType, gDevIdx, gChMask, gTxType, gTxSleep, gTxFrames, gTxFrames, gTxCount, gTxCount, gDebug);

    unsigned VCI_Debug(unsigned);
    VCI_Debug(gDebug);

    if (!VCI_OpenDevice(gDevType, gDevIdx, 0)) {
        printf("VCI_OpenDevice failed\n");
        return 0;
    }
    printf("VCI_OpenDevice succeeded\n");

    test();

    VCI_CloseDevice(gDevType, gDevIdx);
    printf("VCI_CloseDevice\n");
    return 0;
}

