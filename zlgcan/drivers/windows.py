import os
import warnings

from ctypes import *

from ..codes import *
from ..structs import *
from ..structs.windows.cloud.gps import *
from ..structs.windows.can import *
from ..structs.windows.gps import *
from ..structs.windows.lin import *
from ..types import *
from ..exceptions import *
from ..utils import _library_run, _library_path, _current_path, _system_bit
from .zlgcan import _ZLGCAN


_path = lambda ch, path: f'{ch}/{path}' if ch is not None else f'{path}'


class _ZCANWindows(_ZLGCAN):

    def __init__(self, dev_index: int, dev_type: int, resend: bool, derive: bool = False, **kwargs):
        super().__init__(dev_index, dev_type, resend, derive, **kwargs)

        try:
            import yaml  # load baud-rate configuration file
            with open(os.path.join(_current_path, 'baudrate.conf.yaml'), 'r', encoding='utf-8') as stream:
                self._baudrate_config = yaml.full_load(stream)
        except ImportError as e:
            raise ZCANException(e)
        except (FileNotFoundError, PermissionError, ValueError, yaml.YAMLError) as e:
            raise ZCANException(e)

        if _system_bit == "32bit":
            try:
                import win32api
                import win32con
                import pywintypes
                _name = "ZCANPRO.exe"
                _reg = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{_name}"
                _key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, _reg, 0, win32con.KEY_READ)
                _info = win32api.RegQueryInfoKey(_key)
                for i in range(_info[1]):
                    _prog_path: str = win32api.RegEnumValue(_key, i)[1]
                    if _name in _prog_path:
                        _prog_path = _prog_path.replace(_name, "")
                        try:
                            self._library = windll.LoadLibrary(os.path.join(_prog_path, 'zlgcan.dll'))
                            break
                        except OSError:
                            break

                win32api.RegCloseKey(_key)
            except ImportError:       # pywin32 is not installed
                pass
            except pywintypes.error:  # ZCANPRO is not installed
                pass

            if self._library is None:
                self._library = windll.LoadLibrary(os.path.join(_library_path, 'windows/x86/zlgcan.dll'))
        elif _system_bit == "64bit":
            self._library = windll.LoadLibrary(os.path.join(_library_path, 'windows/x86_64/zlgcan.dll'))

        if self._library is None:
            raise ZCANException(
                        "The ZLG-CAN driver could not be loaded. "
                        "Check that you are using 32-bit/64-bit Python on Windows."
                    )

    def _get_can_init_config(self, mode, filter, **kwargs):
        config = ZCAN_CHANNEL_INIT_CONFIG()
        assert self._dev_is_canfd is not None, f'The device{self._dev_index} is not opened!'
        # clock = kwargs.get('clock', None)
        # if clock:
        #     self.SetValue()
        config.type = ZCANCanType.CANFD if self._dev_is_canfd else ZCANCanType.CAN
        acc_code = kwargs.get('acc_code', 0)
        acc_mask = kwargs.get('acc_mask', 0xFFFFFFFF)
        if self._dev_is_canfd:
            # USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI acc_code, acc_mask ignored
            if self._dev_type not in ZUSBCANFD_TYPE:
                config.config.canfd.acc_code = acc_code
                config.config.canfd.acc_mask = acc_mask
            config.config.canfd.abit_timing = kwargs.get('abit_timing', 104286)     # ignored
            config.config.canfd.dbit_timing = kwargs.get('dbit_timing', 8487694)    # ignored
            config.config.canfd.brp = kwargs.get('brp', 0)
            config.config.canfd.filter = filter
            config.config.canfd.mode = mode
            config.config.canfd.brp = kwargs.get('pad', 0)
        else:
            # if self._dev_type in (ZCANDeviceType.ZCAN_PCI5010U, ZCANDeviceType.ZCAN_PCI5020U,
            #                       ZCANDeviceType.ZCAN_USBCAN_E_U, ZCANDeviceType.ZCAN_USBCAN_2E_U,
            #                       ZCANDeviceType.ZCAN_USBCAN_4E_U, ZCANDeviceType.ZCAN_CANDTU_200UR,
            #                       ZCANDeviceType.ZCAN_CANDTU_MINI, ZCANDeviceType.ZCAN_CANDTU_NET,
            #                       ZCANDeviceType.ZCAN_CANDTU_100UR, ZCANDeviceType.ZCAN_CANDTU_NET_400):
            #     config.config.can.acc_code = acc_code
            #     config.config.can.acc_mask = acc_mask
            _cfg = self._baudrate_config[self._dev_type]['bitrate'].get(kwargs.get('bitrate'))
            if not _cfg:
                raise ZCANException(f"buadrate: {kwargs.get('bitrate')} not configured in file(baudrate.conf.yaml)")

            config.config.can.acc_code = acc_code
            config.config.can.acc_mask = acc_mask
            config.config.can.filter = filter

            timing0 = _cfg.get('timing0')
            timing1 = _cfg.get('timing1')
            config.config.can.timing0 = kwargs.get('timing0', timing0)                   # ignored
            config.config.can.timing1 = kwargs.get('timing0', timing1)                  # ignored
            config.config.can.mode = mode
        return config

    # UINT FUNC_CALL ZCAN_SetValue(DEVICE_HANDLE device_handle, const char* path, const void* value);
    def SetValue(self, channel, **kwargs):
        """
        设置通道波特率/时钟频率/终端电阻使能等属性信息
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param kwargs: 其他关键字参数/字典:
| 名称                              | 参数功能                             | 值说明                                                                              | 默认值                   | 时机                     | 备注                                                                  |
|---------------------------------|----------------------------------|----------------------------------------------------------------------------------|-----------------------|------------------------|---------------------------------------------------------------------|
| canfd_standard                  | 设置协议类型                           | 0 – CANFD ISO <br/> 1 – CANFD Non-ISO                                            | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用USBCANFD-100U 、USBCANFD-200U 、USBCANFD-MINI 设备                    |
| protocol                        | 设置协议类型                           | 0 – CAN <br/> 1 – CANFD ISO <br/> 2 – CANFD Non-ISO                              | CANFD ISO 类型          | 需在 init_channel 之前设置   | 适用 USBCANFD-800U 设备                                                 |
| clock                           | 设置时钟频率, 直接影响波特率                  | 不同设备支持的时钟频率不同                                                                    | 上一次设置值                | 在设置波特率之前               |                                                                     |
| canfd_abit_baud_rate            | 设置仲裁域波特率                         | 1000000,800000,500000, <br/> 250000,125000,100000,50000                          | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| canfd_dbit_baud_rate            | 设置数据域波特率                         | 5000000,4000000,2000000, <br/> 1000000,800000,500000, <br/> 250000,125000,100000 | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| baud_rate_custom                | 设置自定义波特率                         | 需计算                                                                              | 上一次设置值                | 需在 init_channel 之前设置   |                                                                     |
| initenal_resistance             | 设置终端电阻                           | 0 - 禁能 <br/> 1 - 使能                                                              | 上一次设置值                | 需在 init_channel 之后设置   |                                                                     |
| tx_timeout                      | 设置发送超时时间                         | 0 ~ 4000 ms                                                                      |                       |                        | 只适用 100U/200U/MINI/设备、不适用 USBCANFD-800U                             |
| auto_send                       | 设置定时发送CAN 帧                      |                                                                                  |                       | 需在 start_channel 之后设置  |                                                                     |
| auto_send_canfd                 | 设置定时发送 CANFD 帧                   |                                                                                  |                       | 需在 start_channel 之后设置  | USBCANFD 支持每通道最大 100 条定时发送列表（USBCANFD-800U 支持每通道最大 32条定时发送列表）       |
| auto_send_param                 | 定时发送附加参数（用于设定特定索引定时发送帧的延时启动）     |                                                                                  | 需在 start_channel 之后设置 | 需在 start_channel 之后设置  | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| clear_auto_send                 | 清空定时发送                           | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| apply_auto_send                 | 应用定时发送（使能定时发送属性设置）               | 0 - 固定值                                                                          |                       | 需在 start_channel 之后设置  |                                                                     |
| set_send_mode                   | 设置设备发送模式                         | 0 – 正常模式 <br/> 1 – 队列模式                                                          | 0 正常模式                |                        | 适用 USBCANFD-100U、USBCANFD-200U、USBCANFD-MINI 设备，USBCANFD-800U 不适用   |
| get_device_available_tx_count/1 | 获取发送队列可用缓存数量（仅队列模式）              | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| clear_delay_send_queue          | 清空发送缓存（仅队列模式，缓存中未发送的帧将被清空，停止时使用） | 0 - 固定值                                                                          |                       |                        |                                                                     |
| set_device_recv_merge           | 设置合并接收功能开启/关闭                    | 0 – 关闭合并接收功能 <br/> 1 – 开启合并接收功能                                                  | 0 – 关闭合并接收功能          |                        |                                                                     |
| get_device_recv_merge/1         | 获取设备当前是否开启了合并接收                  | 无                                                                                |                       |                        | 最后的数字“1”只是内部标志，可以是任意数字                                              |
| set_cn                          | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备                    |
| set_name                        | 设置自定义序列号                         | 自定义字符串, 最多 128 字符                                                                |                       |                        | 适用 USBCANFD-800U 设备                                                 |
| get_cn/1                        | 获取自定义序列号                         | 无                                                                                |                       |                        | 适用 USBCANFD-100U 、USBCANFD-200U、USBCANFD-MINI 设备, 后面的 1 必须，也可以是任意数字 |
| get_name/1                      | 获取自定义序列号                         |                                                                                  |                       |                        | 适用 USBCANFD-800U 设备, 后面的 1 必须，也可以是任意数字                              |
| filter_mode                     | 设置滤波模式                           | 0 – 标准帧 <br/> 1 – 扩展帧                                                            |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_start                    | 设置滤波起始帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_end                      | 设置滤波结束帧 ID                       | 16 进制字符如: 0x00000000                                                             |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_ack                      | 滤波生效（全部滤波 ID 同时生效）               | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| filter_clear                    | 清除滤波                             | 0 - 固定值                                                                          |                       | 需在 init_channel 之后设置   |                                                                     |
| set_bus_usage_enable            | 设置总线利用率信息上报开关                    | 0 - 禁能 <br/> 1 - 使能                                                              |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| set_bus_usage_period            | 设置总线利用率信息上报周期                    | 20 ~ 2000 ms                                                                     |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备                                                |
| get_bus_usage/1                 | 获取总线利用率信息                        | 无                                                                                |                       | 	需在 start_channel 之后获取 | 只适用 USBCANFD-800U 设备, 最后的数字“1”只是内部标志，可以是任意数字                        |
| set_tx_retry_policy             | 设置发送失败时重试策略                      | 0 – 发送失败不重传 <br/> 1 -发送失败重传，直到总线关闭                                               |                       | 需在 start_channel 之前设置  | 只适用 USBCANFD-800U 设备，其他 USBCANFD 设备通过设置工作模式来写入属性                    |

        :return: None
        """
        prop = self.GetIProperty()
        try:
            for path, value in kwargs.items():
                func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
                # _path = f'{channel}/{path}' if channel else f'{path}'
                ret = func(c_char_p(_path(channel, path).encode("utf-8")), c_char_p(f'{value}'.encode("utf-8")))
                if ret != Status.ZCAN_STATUS_OK:
                    raise ZCANException(f'ZLG: Set channel{channel} property: {path} = {value} failed, code {ret}!')
                self._logger.debug(f'ZLG: Set channel{channel} property: {path} = {value} success.')
                assert str(value) == self.GetValue(channel, path, prop)
        finally:
            self.ReleaseIProperty(prop)

    # const void* FUNC_CALL ZCAN_GetValue(DEVICE_HANDLE device_handle, const char* path);
    def GetValue(self, channel, path, prop=None) -> str:
        """
        获取属性值
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param path: 参考zlg_set_properties说明中的字典参数
        :param prop: 属性对象, None即可(内部调用使用)
        :return: 属性值
        """
        _prop = prop or self.GetIProperty()
        try:
            func = CFUNCTYPE(c_char_p, c_char_p)(_prop.contents.GetValue)
            # _path = f'{channel}/{path}' if channel else f'{path}'
            ret = func(c_char_p(_path(channel, path).encode("utf-8")))
            if ret:
                return ret.decode('utf-8')
        finally:
            if not prop:
                self.ReleaseIProperty(_prop)

    def MergeEnabled(self):
        """
        设备是否开启合并收发模式
        :return: True if enabled else False
        """
        return self.GetValue(None, 'get_device_recv_merge/1') is not None

    # UINT FUNC_CALL ZCAN_TransmitData(DEVICE_HANDLE device_handle, ZCANDataObj* pTransmit, UINT len);
    def TransmitData(self, msgs, size=None):
        """
        合并发送数据[只有在设备支持合并发送功能并开启合并发送功能后才可以正常的发送到各种数据]
        :param msgs: 消息内容
        :param size: 消息长度
        :return: 实际发送的消息长度
        """
        self._merge_support()
        _size = size or len(msgs)
        ret = self._library.ZCAN_TransmitData(self._dev_handler, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCANDataObj expect: {_size}, actual: {ret}')
        return ret

    # UINT FUNC_CALL ZCAN_ReceiveData(DEVICE_HANDLE device_handle, ZCANDataObj* pReceive, UINT len, int wait_time DEF(-1));
    def ReceiveData(self, size=1, timeout=-1):
        """
        合并接收数据[只有在设备支持合并接收功能并开启合并接收功能后才可以正常的接收到各种数据]
        :param size: 期待接收的数据大小
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        # warnings.warn('ZLG: Library not support.', DeprecationWarning, 2)
        # self.zlg_get_property()
        if timeout is not None:
            timeout = int(timeout)
        self._merge_support()
        if not self.MergeEnabled():
            raise ZCANException('ZLG: device merge receive is not enable!')
        msgs = (ZCANDataObj * size)()
        ret = self._library.ZCAN_ReceiveData(self._dev_handler, byref(msgs), size, c_int(timeout))
        self._logger.debug(f'ZLG: Received {ret} ZCANDataObj messages.')
        return msgs, ret

    # IProperty* FUNC_CALL GetIProperty(DEVICE_HANDLE device_handle);
    def GetIProperty(self):
        self._library.GetIProperty.restype = POINTER(IProperty)
        return self._library.GetIProperty(self._dev_handler)

    # UINT FUNC_CALL ReleaseIProperty(IProperty * pIProperty);
    def ReleaseIProperty(self, prop: IProperty):
        return self._library.ReleaseIProperty(prop)

    # UINT FUNC_CALL ZCAN_IsDeviceOnLine(DEVICE_HANDLE device_handle);
    def DeviceOnLine(self):
        ret = self._library.ZCAN_IsDeviceOnLine(self._dev_handler)
        self._logger.debug(f'ZLG: get device is online return code: {ret}.')
        return ret == Status.ZCAN_STATUS_ONLINE

    # void FUNC_CALL ZCLOUD_SetServerInfo(const char* httpSvr, unsigned short httpPort, const char* authSvr, unsigned short authPort);
    def SetServerInfo(self, auth_host: str, auth_port, data_host=None, data_post=None):
        _library_run(self._library, 'ZCLOUD_SetServerInfo',
                           c_char_p(auth_host.encode('utf-8')), c_ushort(auth_port),
                           c_char_p((data_host or auth_host).encode('utf-8')),
                           c_ushort(data_post or auth_port))

    # // return 0:success, 1:failure, 2:https error, 3:user login info error, 4:mqtt connection error, 5:no device
    # UINT FUNC_CALL ZCLOUD_ConnectServer(const char* username, const char* password);
    def ConnectServer(self, username, password):
        ret = self._library.ZCLOUD_ConnectServer(c_char_p(username.encode('utf-8')), c_char_p(password.encode('utf-8')))
        if ret == 0:
            return
        elif ret == 1:
            raise ZCANException('ZLG: connect server failure')
        elif ret == 2:
            raise ZCANException('ZLG: connect server https error')
        elif ret == 3:
            raise ZCANException('ZLG: connect server user login info error')
        elif ret == 4:
            raise ZCANException('ZLG: connect server mqtt connection error')
        elif ret == 5:
            raise ZCANException('ZLG: connect server no device')
        else:
            raise ZCANException(f'ZLG: connect server undefined error: {ret}')

    # bool FUNC_CALL ZCLOUD_IsConnected();
    def CloudConnected(self):
        return self._library.ZCLOUD_IsConnected()

    # // return 0:success, 1:failure
    # UINT FUNC_CALL ZCLOUD_DisconnectServer();
    def DisconnectServer(self):
        ret = self._library.ZCLOUD_IsConnected()
        return ret == 0

    # const ZCLOUD_USER_DATA* FUNC_CALL ZCLOUD_GetUserData(int update DEF(0));
    def GetUserData(self, userid) -> ZCLOUD_USER_DATA:
        return self._library.ZCLOUD_GetUserData(userid)

    # UINT FUNC_CALL ZCLOUD_ReceiveGPS(DEVICE_HANDLE device_handle, ZCLOUD_GPS_FRAME* pReceive, UINT len, int wait_time DEF(-1));
    def ReceiveGPS(self, size=1, timeout=-1):
        if timeout is not None:
            timeout = int(timeout)
        msgs = (ZCLOUD_GPS_FRAME * size)()
        ret = self._library.ZCLOUD_ReceiveGPS(self._dev_handler, byref(msgs), size, timeout)
        self._logger.debug(f'ZLG: Master Transmit ZCLOUD_GPS_FRAME expect: {size}, actual: {ret}')
        return msgs, ret

    # CHANNEL_HANDLE FUNC_CALL ZCAN_InitLIN(DEVICE_HANDLE device_handle, UINT can_index, PZCAN_LIN_INIT_CONFIG pLINInitConfig);
    def InitLIN(self, channel, config: ZCAN_LIN_INIT_CONFIG):
        ret = self._library.ZCAN_InitLIN(self._dev_handler, channel, byref(config))
        if ret == DeviceHandle.INVALID_CHANNEL_HANDLE:
            raise ZCANException('ZLG: ZCAN_InitLIN failed!')
        self._channel_handlers['LIN'][channel] = ret

    # UINT FUNC_CALL ZCAN_StartLIN(CHANNEL_HANDLE channel_handle);
    def StartLIN(self, channel):
        handler = self._get_channel_handler('LIN', channel)
        _library_run(self._library, 'ZCAN_StartLIN', handler)

    # UINT FUNC_CALL ZCAN_ResetLIN(CHANNEL_HANDLE channel_handle);
    def ResetLIN(self, channel):
        handler = self._get_channel_handler('LIN', channel)
        _library_run(self._library, 'ZCAN_ResetLIN', handler)

    # UINT FUNC_CALL ZCAN_TransmitLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT Len);
    def TransmitLIN(self, channel, msgs, size=None):
        handler = self._get_channel_handler('LIN', channel)
        _size = size or len(msgs)
        ret = self._library.ZCAN_TransmitLIN(handler, byref(msgs), _size)
        self._logger.debug(f'ZLG: Master Transmit ZCAN_LIN_MSG expect: {_size}, actual: {ret}')
        return ret

    # UINT FUNC_CALL ZCAN_ReceiveLIN(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pReceive, UINT Len,int WaitTime);
    def ReceiveLIN(self, channel, size=1, timeout=-1):
        if timeout is not None:
            timeout = int(timeout)
        msgs = (ZCAN_LIN_MSG * size)()
        handler = self._get_channel_handler('LIN', channel)
        ret = self._library.ZCAN_ReceiveLIN(handler, byref(msgs), size, c_int(timeout))
        self._logger.debug(f'ZLG: Master Received {ret} ZCAN_LIN_MSG messages')
        return msgs, ret

    # UINT FUNC_CALL ZCAN_SetLINSlaveMsg(CHANNEL_HANDLE channel_handle, PZCAN_LIN_MSG pSend, UINT nMsgCount);
    def SetLINSlaveMsg(self, channel, msgs):
        handler = self._get_channel_handler('LIN', channel)
        ret = self._library.ZCAN_SetLINSlaveMsg(handler, byref(msgs), len(msgs))
        self._logger.debug(f'ZLG: Slave Transmit {ret} ZCAN_LIN_MSG messages')
        return ret

    # UINT FUNC_CALL ZCAN_ClearLINSlaveMsg(CHANNEL_HANDLE channel_handle, BYTE* pLINID, UINT nIDCount);
    def ClearLINSlaveMsg(self, channel, lin_ids):
        handler = self._get_channel_handler('LIN', channel)
        _library_run(self._library, 'ZCAN_ClearLINSlaveMsg', handler, byref(lin_ids), len(lin_ids))

    def ResistanceStatus(self, channel, status=None):
        if self._dev_type in ZCAN_RESISTANCE_NOT_SUPPORT:
            return

        if status is not None:
            self.SetValue(channel, initenal_resistance=status)
        return self.GetValue(channel, 'initenal_resistance')

    def SetFilters(self, channel, filters=None):
        if filters is None:
            return self.SetValue(channel, filter_clear=0)
        if len(filters) > 64:
            filters = filters[:64]
        for _filter in filters:
            mode = _filter[0]
            start = _filter[1]
            end = _filter[2]
            self.SetValue(channel, filter_mode=mode, filter_start=start, filter_end=end)

    # DEVICE_HANDLE FUNC_CALL ZCAN_OpenDevice(UINT device_type, UINT device_index, UINT reserved);
    def OpenDevice(self, reserved=0):
        ret = self._library.ZCAN_OpenDevice(self._dev_type, self._dev_index, reserved)
        if ret == DeviceHandle.INVALID_DEVICE_HANDLE:
            raise ZCANException('ZLG: ZCAN_OpenDevice failed!')
        self._dev_handler = ret
        if not self._dev_derive:
            try:
                self._dev_info = self.GetDeviceInf()
                self._channels = tuple(i for i in range(self._dev_info.can_num))
                self._dev_is_canfd = 'CANFD' in self._dev_info.hw_type
            except ZCANException:
                raise ZCANException("can't get device info, consider set derive as True")
        else:
            self._channels = (0, )
            self._dev_is_canfd = False

    # UINT FUNC_CALL ZCAN_CloseDevice(DEVICE_HANDLE device_handle);
    def CloseDevice(self):
        can_channels = self._channel_handlers['CAN']
        lin_channels = self._channel_handlers['LIN']
        for channel, _ in can_channels.items():
            self.ResetCAN(channel)
        for channel, _ in lin_channels.items():
            self.ResetLIN(channel)
        _library_run(self._library, 'ZCAN_CloseDevice', self._dev_handler)
        self._dev_handler = None
        can_channels.clear()
        lin_channels.clear()

    # UINT FUNC_CALL ZCAN_GetDeviceInf(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO* pInfo);
    def GetDeviceInf(self) -> ZCAN_DEVICE_INFO:
        dev_info = ZCAN_DEVICE_INFO()
        _library_run(self._library, 'ZCAN_GetDeviceInf', self._dev_handler, byref(dev_info))
        return dev_info

    # CHANNEL_HANDLE FUNC_CALL ZCAN_InitCAN(DEVICE_HANDLE device_handle, UINT can_index, ZCAN_CHANNEL_INIT_CONFIG* pInitConfig);
    def InitCAN(self, channel, mode: ZCANCanMode = ZCANCanMode.NORMAL,
                filter: ZCANCanFilter = ZCANCanFilter.DOUBLE,
                **kwargs):
        """
        初始化CAN(FD)通道
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param mode: CAN(FD)模式, 可选值0: 正常模式, 1: 只听(只读)模式, 默认0
| mode        | 通道工作模式         | 0 - 正常模式 <br/> 1 - 只听模式 |     |
        :param filter: CAN(FD)滤波方式, 可选值0: 双滤波, 1: 单滤波, 默认0
        :param kwargs: 其他关键字参数, 说明如下:
| 名称          | 功能             | 值说明                     | 默认值 | 备注            |
|-------------|----------------|-------------------------|-----|---------------|
| acc_code    | SJA1000的帧过滤验收码 | 推荐设置为0x0                |     |               |
| acc_mask    | SJA1000的帧过滤屏蔽码 | 推荐设置为0xffffffff         |     |               |
| filter      | 滤波方式           | 0 - 双滤波 <br/> 1 - 单滤波   | 0   |               |
| brp         | 滤波预分频因子        | 设置为0                    |     | 仅CANFD, 影响波特率 |
| abit_timing | ignored        | NA                      | NA  | 仅CANFD        |
| dbit_timing | ignored        | NA                      | NA  | 仅CANFD        |

        :return: None
        """
        if "bitrate" not in kwargs:
            raise ZCANException("'bitrate' is required in config")

        clock = kwargs.get('clock', None)
        if clock:
            self.SetValue(channel, clock=clock)

        config = self._get_can_init_config(mode, filter, **kwargs)
        ret = self._library.ZCAN_InitCAN(self._dev_handler, channel, byref(config))
        if ret == DeviceHandle.INVALID_CHANNEL_HANDLE:
            raise ZCANException('ZLG: ZCAN_InitCAN failed!')

        self._channel_handlers['CAN'][channel] = ret
        self.ResistanceStatus(channel, kwargs.get('initenal_resistance', 1))

    # UINT FUNC_CALL ZCAN_StartCAN(CHANNEL_HANDLE channel_handle);
    def StartCAN(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'ZCAN_StartCAN', handler)

    # UINT FUNC_CALL ZCAN_ResetCAN(CHANNEL_HANDLE channel_handle);
    def ResetCAN(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'ZCAN_ResetCAN', handler)

    # UINT FUNC_CALL ZCAN_ClearBuffer(CHANNEL_HANDLE channel_handle);
    def ClearBuffer(self, channel):
        handler = self._get_channel_handler('CAN', channel)
        _library_run(self._library, 'ZCAN_ClearBuffer', handler)

    # UINT FUNC_CALL ZCAN_ReadChannelErrInfo(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO* pErrInfo);
    def ReadChannelErrInfo(self, channel, chl_type='CAN'):
        error_info = ZCAN_CHANNEL_ERR_INFO()
        handler = self._get_channel_handler(chl_type, channel)
        # TODO 统一
        _library_run(self._library, 'ZCAN_ReadChannelErrInfo', handler, byref(error_info))
        return error_info

    # UINT FUNC_CALL ZCAN_ReadChannelStatus(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_STATUS* pCANStatus);
    def ReadChannelStatus(self, channel, chl_type='CAN'):
        warnings.warn('ZLG: no device supported.', DeprecationWarning, 2)
        status_info = ZCAN_CHANNEL_STATUS()
        handler = self._get_channel_handler(chl_type, channel)
        # TODO 统一
        _library_run(self._library, 'ZCAN_ReadChannelStatus', handler, byref(status_info))
        return status_info

    # UINT FUNC_CALL ZCAN_GetLINReceiveNum(CHANNEL_HANDLE channel_handle);
    # UINT FUNC_CALL ZCAN_GetReceiveNum(CHANNEL_HANDLE channel_handle, BYTE type);//type:TYPE_CAN, TYPE_CANFD, TYPE_ALL_DATA
    def GetReceiveNum(self, channel, msg_type: ZCANMessageType = ZCANMessageType.CAN):
        """
        获取指定通道已经接收到消息数量
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msg_type: 消息类型: 0 - CAN; 1 - CANFD; '-1' - LIN
        :return: 消息数量
        """
        if msg_type == ZCANMessageType.LIN:
            return self._library.ZCAN_GetLINReceiveNum(self._get_channel_handler('LIN', channel))
        return self._library.ZCAN_GetReceiveNum(self._get_channel_handler('CAN', channel), msg_type)

    # UINT FUNC_CALL ZCAN_TransmitFD(CHANNEL_HANDLE channel_handle, ZCAN_TransmitFD_Data* pTransmit, UINT len);
    def TransmitFD(self, channel, msgs, size=None):
        handler = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = self._library.ZCAN_TransmitFD(handler, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCAN_TransmitFD_Data expect: {_size}, actual: {ret}')
        return ret

    # UINT FUNC_CALL ZCAN_ReceiveFD(CHANNEL_HANDLE channel_handle, ZCAN_ReceiveFD_Data* pReceive, UINT len, int timeout DEF(-1));
    def ReceiveFD(self, channel, size=1, timeout=-1):
        if timeout is not None:
            timeout = int(timeout)
        handler = self._get_channel_handler('CAN', channel)
        can_msgs = (ZCAN_ReceiveFD_Data * size)()
        ret = self._library.ZCAN_ReceiveFD(handler, byref(can_msgs), size, timeout)
        self._logger.debug(f'ZLG: Receive ZCAN_ReceiveFD_Data expect: {size}, actual: {ret}')
        for i in range(ret):
            can_msg = can_msgs[i]
            can_msg.channel = channel
            can_msg.is_rx = True
            yield can_msg

    # # UINT FUNC_CALL ZCAN_Transmit(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data* pTransmit, UINT len);
    def Transmit(self, channel, msgs, size=None):
        """
        发送CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param msgs: 消息报文
        :param size: 报文大小
        :return: 实际发送报文长度
        """
        handler = self._get_channel_handler('CAN', channel)
        _size = size or len(msgs)
        ret = self._library.ZCAN_Transmit(handler, byref(msgs), _size)
        self._logger.debug(f'ZLG: Transmit ZCAN_Transmit_Data expect: {_size}, actual: {ret}')
        return ret

    # UINT FUNC_CALL ZCAN_Receive(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data* pReceive, UINT len, int wait_time DEF(-1));
    def Receive(self, channel, size=1, timeout=-1):
        """
        接收CAN报文
        :param channel: 通道号, 范围 0 ~ 通道数-1
        :param size: 期待接收报文个数
        :param timeout: 缓冲区无数据, 函数阻塞等待时间, 单位毫秒, 若为-1 则表示一直等待
        :return: 消息内容及消息实际长度
        """
        if timeout is not None:
            timeout = int(timeout)
        handler = self._get_channel_handler('CAN', channel)
        can_msgs = (ZCAN_Receive_Data * size)()
        ret = self._library.ZCAN_Receive(handler, byref(can_msgs), size, timeout)
        for i in range(ret):
            can_msg = can_msgs[i]
            can_msg.channel = channel
            can_msg.is_rx = True
            yield can_msg

    def TransmitInterval(self, channel, interval_msgs=None):
        """
        定时发送消息
        :param channel: 通道号, 从0开始
        :param interval_msgs: 周期消息, 以字典列表的形式传入, 最大长度8, 超过8的截取前8个
            Windows下:
                字典内容为:
                    enable: [可选, 默认值0] 0-此帧禁用定时发送, 1-此帧使能定时发送
                    index: [可选, 自动根据列表顺序编号]定时发送帧索引, 即第几条定时发送报文
                    interval: [可选, 默认值0] 发送间隔, 单位ms
                    trans_type: [可选, 默认值0] 0=正常发送, 1=单次发送, 2=自发自收, 3=单次自发自收
                    msg: [必须] ZCAN_CANFD_FRAME|ZCAN_CAN_FRAME
                    delay: [可选, 默认值None], 延迟发送时间, 单位ms
            Linux下:
                字典内容为:
                    enable: [可选, 默认值0] 0-此帧禁用定时发送, 1-此帧使能定时发送
                    index: [可选, 自动根据列表顺序编号]定时发送帧索引, 即第几条定时发送报文
                    interval: [可选, 默认值0] 发送间隔, 单位0.1ms
                    repeat: [可选, 默认值0] 发送次数, 0则表示无限次数
                    msg: [必须] ZCAN_CANFD_FRAME 报文内容
        :return: None
        """
        prop = self.GetIProperty()
        func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(prop.contents.SetValue)
        func1 = CFUNCTYPE(c_uint, c_char_p, c_void_p)(prop.contents.SetValue)
        try:
            ret = func(c_char_p(f'{channel}/clear_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
            if ret != Status.ZCAN_STATUS_OK:
                raise ZCANException(f'ZLG: Set {channel}/clear_auto_send failed!')
            if interval_msgs:
                if len(interval_msgs) > 8:
                    interval_msgs = interval_msgs[:8]
                for index, msg_dict in enumerate(interval_msgs):
                    is_fd = False
                    msg = msg_dict.get('msg')
                    if isinstance(msg, ZCAN_Transmit_Data):
                        data = ZCAN_AUTO_TRANSMIT_OBJ()
                    elif isinstance(msg, ZCAN_TransmitFD_Data):
                        data = ZCANFD_AUTO_TRANSMIT_OBJ()
                        is_fd = True
                    else:
                        raise ZCANException(f'ZLG: Unsupported message type {type(msg)}')
                    data.enable = msg_dict.get('enable', 0)
                    data.index = msg_dict.get('index', index)
                    data.interval = msg_dict.get('interval', 0)
                    data.obj.transmit_type = msg_dict.get('trans_type', 0)
                    data.obj.frame = msg
                    ret = func1(c_char_p(f'{channel}/auto_send{"fd" if is_fd else ""}'.encode("utf-8")),
                                cast(byref(data), c_void_p))
                    if ret != Status.ZCAN_STATUS_OK:
                        raise ZCANException(f'ZLG: Set {channel} auto transmit object failed!')
                    delay = msg_dict.get('delay', None)
                    if delay:
                        delay_param = ZCAN_AUTO_TRANSMIT_OBJ_PARAM()
                        delay_param.index = msg_dict.get('index', index)
                        delay_param.type = 1
                        delay_param.value = delay
                        ret = func1(c_char_p(f'{channel}/auto_send_param'.encode("utf-8")),
                                    cast(byref(delay_param), c_void_p))
                        if ret != Status.ZCAN_STATUS_OK:
                            raise ZCANException(f'ZLG: Set {channel} auto transmit object param failed!')

                    ret = func(c_char_p(f'{channel}/apply_auto_send'.encode("utf-8")), c_char_p('0'.encode('utf-8')))
                    if ret != Status.ZCAN_STATUS_OK:
                        raise ZCANException(f'ZLG: Set {channel}/apply_auto_send failed!')
        finally:
            self.ReleaseIProperty(prop)






