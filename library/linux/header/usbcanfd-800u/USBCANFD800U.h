#ifndef USBCANFD_800U_H_
#define USBCANFD_800U_H_

#include <stdint.h>
#include "zlgcan.h"

#define MAX_DEVICE_COUNT                        32  //支持的设备数量
#define DEVICE_CAN_CHNL_COUNT_MAX               8   //支持最大的CAN通道数量,实际通道数量可能小于此数值
#define DEVICE_LIN_CHNL_COUNT_MAX               4   //支持最大的LIN通道数量,实际通道数量可能小于此数值
#define DEVICE_TOTAL_CHNL_COUNT                 (DEVICE_CAN_CHNL_COUNT_MAX + DEVICE_LIN_CHNL_COUNT_MAX)
#define FILTER_RULE_COUNT_MAX                   64  //设备允许的过滤条数
#define DEV_AUTO_SEND_INDEX_MAX                 32  //定时发送索引最大值

//SetReference/GetReference ref type
//控制器类型(协议)
#define SETREF_SET_CONTROLLER_TYPE              1   //pData 指向uint32_t, 0:CAN; 1：ISO CANFD; 2:Non-ISO CANFD, 需要在StartCAN之前设置
//过滤功能，添加过滤，库对过滤条目进行缓存，调用Apply后启用过滤，调用Clear清除过滤
#define SETREF_ADD_FILTER                       2   //添加通道过滤条目，pData Pointer to RefFilterItem(12 Bytes)
#define SETREF_APPLY_FILTER                     3   //应用通道过滤
#define SETREF_CLEAR_FILTER                     4   //清除通道过滤
//更新固件,参数类型和reftype和USBCANFD200U系列保持一致，可以使用同样的升级工具升级
#define SETREF_UPDATE_FIRMWARE                  5   //pData Pointer to FirmwareUpdateParam结构,指示固件路径
#define GETREF_GET_UPDATE_STATUS                6   //pData Pointer to FirmwareUpdateStatus
//以下定时发送使用流程，Add CAN/CANFD后进入缓存，调用Apply才进行定时发送，Clear会停止之前Apply的数据并清空缓存
#define SETREF_ADD_TIMER_SEND_CAN               7   //pData Pointer to ZCAN_AUTO_TRANSMIT_OBJ
#define SETREF_ADD_TIMER_SEND_CANFD             8   //pData Pointer to ZCANFD_AUTO_TRANSMIT_OBJ
#define SETREF_APPLY_TIMER_SEND                 9   //Start Timer Send
#define SETREF_CLEAR_TIMER_SEND                 10  //Stop Timer Send & Clear Send List
//终端电阻
#define SETREF_ENABLE_INTERNAL_RESISTANCE       11   //pData 指向uint32_t, 0:断开内置终端电阻；1：使用设备内部终端电阻, 需要在StartCAN之前设置
//设备名称
#define SETREF_SET_DEVICE_NAME                  12  //设备设备名称，pData Pointer to char*
#define GETREF_GET_DEVICE_NAME                  13  //设备设备名称，pData 指向用户申请内存，大小需要足够容纳设备名字
//设备日志
#define SETREF_CLEAR_DEVICE_LOG                 14  //清除设备日志
#define GETREF_GET_DEVICE_LOG_SIZE              15  //获取设备日志大小，pData Pointer to uint32_t
#define GETREF_GET_DEVICE_LOG_DATA              16  //设备设备日志内容，pData 指向用户申请内存，大小需要足够容纳设备日志
//开启关闭合并接收
#define SETREF_SET_DATA_RECV_MERGE              17   //设置合并接收数据，CAN/LIN/GPS以及不同通道的数据合并接收,pData Pointer to uint32_t, 0:关闭合并接收，1：开启合并接收
#define GETREF_GET_DATA_RECV_MERGE              18  //获取合并接收数据状态，pData Pointer to uint32_t, 0:合并接收关闭，1：合并接收处于开启状态
//内部测试
#define SETREF_INTERNAL_TEST                    19   //pData Point to InternalTestData
//验证设备
#define SETREF_VIRIFY_DEVICE_BY_PASS            20  //ZCANPRO验证设备，pData数据类型为指向VerifyDeviceData的指针
//总线利用率
#define SETREF_ENABLE_BUS_USAGE                 21   //pData 指向uint32_t, 0:关闭总线利用率上报，1：开启总线利用率上报，需要在StartCAN之前设置
#define SETREF_SET_BUS_USAGE_PERIOD             22  //pData 指向uint32_t, 表示设备上报周期，单位毫秒，范围20-2000ms, 需要在StartCAN之前设置
#define GETREF_GET_BUS_USAGE                    23  //获取总线利用率, pData指向 BusUsage
//获取队列发送可用空间,清空队列发送
#define GETREF_GET_DELAY_SEND_AVALIABLE_COUNT   24  //获取设备端延迟发送可用数量 pData Pointer to uint32_t
#define SETREF_CLEAR_DELAY_SEND_QUEUE           25  //如果队列发送中有数据因为时间未到未发送，取消设备当前的队列发送
//获取LIN 发送Fifo大小
#define GETREF_GET_LIN_TX_FIFO_TOTAL            26  //获取LIN发送缓冲区大小
#define GETREF_GET_LIN_TX_FIFO_AVAILABLE        27  //获取LIN发送缓冲区可用大小
//发送定时数据,调用完毕即马上发送
#define SETREF_ADD_TIMER_SEND_CAN_DIRECT        28  //pData Pointer to ZCAN_AUTO_TRANSMIT_OBJ
#define SETREF_ADD_TIMER_SEND_CANFD_DIRECT      29  //pData Pointer to ZCANFD_AUTO_TRANSMIT_OBJ
//获取设备定时发送数量，设备调用获取CAN或者CANFD定时发送数量时(REF为31,33)，库和设备进行通讯，获取设备端定时发送列表，然后通过(REF 32,34)分别获取CAN,CANFD定时发送帧内容
#define GETREF_GET_DEV_CAN_AUTO_SEND_COUNT      30  //获取设备端定时发送CAN帧的数量，pData指向uint32_t,表示设备端定时发送CAN帧数量
#define GETREF_GET_DEV_CAN_AUTO_SEND_DATA       31  //获取设备端定时发送CAN帧的数据，用户根据查询到的CAN帧数量申请内存 sizeof(ZCAN_AUTO_TRANSMIT_OBJ) * N，将申请到的内存地址填入pData
#define GETREF_GET_DEV_CANFD_AUTO_SEND_COUNT    32  //获取设备端定时发送CANFD帧的数量，pData指向uint32_t,表示设备端定时发送CANFD帧数量
#define GETREF_GET_DEV_CANFD_AUTO_SEND_DATA     33  //获取设备端定时发送CANFD帧的数据，用户根据查询到的CAN帧数量申请内存 sizeof(ZCANFD_AUTO_TRANSMIT_OBJ) * N，将申请到的内存地址填入pData
//设置发送回显
#define SETREF_SET_TX_ECHO                      34  //设置库强制发送回显,pData指向uint32_t，0表示不开启发送回显，1表示开启发送回显，开启后，普通发送也会设置发送回显请求标志
#define GETREF_GET_TX_ECHO                      35  //查询是否设置了强制发送回显,pData指向uint32_t，0表示不开启发送回显，1表示开启发送回显
#define USBCANFD_SETREF_SET_TX_RETRY_POLICY     36  //发送失败是否重传：0：发送失败不重传；1：发送失败重传，直到总线关闭。
//发送超时时间（2022.07.09新加，为了规避设备端buff区满pc下发失败的现象）
#define SETREF_SET_TX_TIMEOUT                   37  //发送超时时间，单位ms；设置后发送达到超时时间后，取消当前报文发送；取值范围0-2000ms。
#define SETREF_GET_TX_TIMEOUT                   38

#pragma pack(push ,1)

struct DeviceInfo
{
    int         nCANChnl;
    int         nLINChnl;
    uint32_t    nDeviceMaxDataLen;  //设备可以处理的数据量
};

struct RefFilterItem
{
    uint32_t    nExt;
    uint32_t    nBeginID;
    uint32_t    nEndID;
};
#pragma pack(pop)


#ifdef __cplusplus
extern "C"
{
#endif
    UINT FUNC_CALL ZCAN_GetReference(UINT DeviceType, UINT nDevIndex, UINT nChnlIndex, UINT nRefType, void* pData);
    UINT FUNC_CALL ZCAN_SetReference(UINT DeviceType, UINT nDevIndex, UINT nChnlIndex, UINT nRefType, void* pData);

#ifdef __cplusplus
}
#endif

#endif // USBCANFD_800U_H_
