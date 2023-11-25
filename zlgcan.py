import collections
import ctypes
import logging
import platform
import time
import warnings

from can.bus import LOG

import can.typechecking
from can.exceptions import (
    CanError,
    CanInterfaceNotImplementedError,
    CanOperationError,
    CanInitializationError,
)
from typing import Optional, Tuple, Sequence, Union, Deque, Any
from can import BusABC, Message
from zlgcan import ZCAN, ZCANDeviceType, ZCANException, ZCANMessageType, ZCANCanTransType, ZUSBCAN_I_II_TYPE

logger = logging.getLogger(__name__)
_os = platform.system()


def zlg_convert_msg(msg, **kwargs):
    if _os.lower() == 'windows':
        return _zlg_convert_msg_win(msg, **kwargs)
    elif _os.lower() == 'linux':
        return _zlg_convert_msg_linux(msg, **kwargs)
    else:
        raise ZCANException(f'Unsupported platform: {_os}')


def _zlg_convert_msg_linux(msg, **kwargs):
    from zlgcan.linux import ZCAN_CAN_FRAME, ZCAN_CANFD_FRAME, ZCAN_CAN_FRAME_I_II
    if isinstance(msg, Message):
        channel = kwargs.get('channel')
        assert channel is not None or msg.channel is not None, 'channel is required!'
        trans_type = kwargs.get('trans_type', ZCANCanTransType.NORMAL if kwargs.get('resend', False) else ZCANCanTransType.SINGLE)
        device_type = kwargs.get("device_type")
        if device_type in ZUSBCAN_I_II_TYPE:
            result = (ZCAN_CAN_FRAME_I_II * 1)()
            result[0].SendType = trans_type
            result[0].ID = msg.arbitration_id
            result[0].RemoteFlag = int(msg.is_remote_frame)
            result[0].ExternFlag = int(msg.is_extended_id)
            result[0].DataLen = msg.dlc
            for _idx, _val in enumerate(msg.data):
                result[0].Data[_idx] = _val
            return result

        if msg.is_fd:
            result = (ZCAN_CANFD_FRAME * 1)()
        else:
            result = (ZCAN_CAN_FRAME * 1)()

        result[0].hdr.inf.txm = trans_type
        result[0].hdr.inf.fmt = int(msg.is_fd)
        result[0].hdr.inf.sdf = int(msg.is_remote_frame)
        result[0].hdr.inf.sef = int(msg.is_extended_id)
        result[0].hdr.inf.err = int(msg.is_error_frame)
        result[0].hdr.inf.brs = int(msg.bitrate_switch)
        result[0].hdr.inf.est = int(msg.error_state_indicator)

        result[0].hdr.id = msg.arbitration_id
        result[0].hdr.chn = msg.channel or channel
        result[0].hdr.len = msg.dlc
        for _idx, _val in enumerate(msg.data):
            result[0].dat[_idx] = _val

        return result
    elif isinstance(msg, (ZCAN_CAN_FRAME, ZCAN_CANFD_FRAME)):
        channel = kwargs.get('channel')
        assert channel is not None or msg.hdr.chn is not None, 'channel is required!'
        return Message(
            timestamp=msg.hdr.ts / 1000,
            arbitration_id=msg.hdr.id,
            is_extended_id=bool(msg.hdr.inf.sdf),
            is_remote_frame=bool(msg.hdr.inf.sef),
            is_error_frame=bool(msg.hdr.inf.err),
            channel=msg.hdr.chn or channel,
            dlc=msg.hdr.len,
            data=bytes(msg.dat),
            is_fd=bool(msg.hdr.inf.fmt),
            is_rx=kwargs.get("is_rx", False),
            bitrate_switch=bool(msg.hdr.inf.brs),
            error_state_indicator=bool(msg.hdr.inf.est),
        )
    elif isinstance(msg, ZCAN_CAN_FRAME_I_II):
        channel = kwargs.get('channel')
        assert channel is not None, 'channel is required!'
        return Message(
            timestamp=msg.TimeStamp / 1000,
            arbitration_id=msg.ID,
            is_extended_id=bool(msg.ExternFlag),
            is_remote_frame=bool(msg.RemoteFlag),
            is_error_frame=False,
            channel=channel,
            dlc=msg.DataLen,
            data=bytes(msg.Data),
            is_fd=False,
            is_rx=kwargs.get("is_rx", False),
            bitrate_switch=False,
            error_state_indicator=False,
        )
    else:
        raise ZCANException(f'Unknown message type: {type(msg)}')


def _zlg_convert_msg_win(msg, **kwargs):                        # channel=None, trans_type=0, is_merge=False, **kwargs):

    from zlgcan.windows import ZCAN_Transmit_Data, ZCAN_TransmitFD_Data, ZCANDataObj, ZCAN_Receive_Data, ZCAN_ReceiveFD_Data
    ZCAN_Transmit_Data_1 = (ZCAN_Transmit_Data * 1)
    ZCAN_TransmitFD_Data_1 = (ZCAN_TransmitFD_Data * 1)
    ZCANDataObj_1 = (ZCANDataObj * 1)

    if isinstance(msg, Message):                        # 发送报文转换
        is_merge = kwargs.get('is_merge', None)
        trans_type = kwargs.get('trans_type', ZCANCanTransType.NORMAL if kwargs.get('resend', False) else ZCANCanTransType.SINGLE)
        assert is_merge is not None, 'is_merge required when convert to ZLG.'
        # assert trans_type is not None, 'trans_type required when convert to ZLG.'
        if not is_merge:
            if msg.is_fd:
                result = ZCAN_TransmitFD_Data_1()
                result[0].frame.len = msg.dlc
                result[0].frame.brs = msg.bitrate_switch
                result[0].frame.data = (ctypes.c_ubyte * 64)(*msg.data)
            else:
                result = ZCAN_Transmit_Data_1()
                result[0].frame.can_dlc = msg.dlc
                result[0].frame.data = (ctypes.c_ubyte * msg.dlc)(*msg.data)
            result[0].transmit_type = trans_type

            result[0].frame.can_id = msg.arbitration_id
            result[0].frame.err = msg.is_error_frame
            result[0].frame.rtr = msg.is_remote_frame
            result[0].frame.eff = msg.is_extended_id
            return result
        else:
            channel = kwargs.get('channel', None)
            assert channel is not None, 'channel required when merge send recv.'
            result = ZCANDataObj_1()
            result[0].dataType = 1                     # can device always equal 1
            assert channel is not None
            result[0].chn = channel
            result[0].data.zcanCANFDData.frame.can_id = msg.arbitration_id
            result[0].data.zcanCANFDData.frame.err = msg.is_error_frame
            result[0].data.zcanCANFDData.frame.rtr = msg.is_remote_frame
            result[0].data.zcanCANFDData.frame.eff = msg.is_extended_id

            result[0].data.zcanCANFDData.flag.transmitType = trans_type
            echo = kwargs.get('is_echo', False)
            result[0].data.zcanCANFDData.flag.txEchoRequest = echo
            delay = kwargs.get('delay_mode', 0)
            if delay:
                result[0].data.zcanCANFDData.flag.txDelay = delay
                result[0].data.zcanCANFDData.timeStamp = kwargs['delay_time']
            return result
    elif isinstance(msg, ZCAN_Receive_Data):                        # 接收CAN报文转换
        channel = kwargs.get('channel', None)
        assert channel is not None, 'channel required when convert ZLG CAN msg to std msg.'
        return Message(
            timestamp=msg.timestamp / 1000,
            arbitration_id=msg.frame.can_id,
            is_extended_id=msg.frame.eff,
            is_remote_frame=msg.frame.rtr,
            is_error_frame=msg.frame.err,
            channel=channel,
            dlc=msg.frame.can_dlc,
            data=bytes(msg.frame.data),
            is_rx=True,
        )
    elif isinstance(msg, ZCAN_ReceiveFD_Data):                          # 接收CANFD报文转换
        channel = kwargs.get('channel', None)
        assert channel is not None, 'channel required when convert ZLG CANFD msg to std msg.'
        return Message(
            timestamp=msg.timestamp / 1000,
            arbitration_id=msg.frame.can_id,
            is_extended_id=msg.frame.eff,
            is_remote_frame=msg.frame.rtr,
            is_error_frame=msg.frame.err,
            channel=channel,
            dlc=msg.frame.len,
            data=bytes(msg.frame.data),
            is_fd=True,
            is_rx=True,
            bitrate_switch=msg.frame.brs,
            error_state_indicator=msg.frame.esi,
        )
    elif isinstance(msg, ZCANDataObj):                                  # 合并接收CAN|CANFD报文转换
        data = msg.data.zcanCANFDData
        return Message(
            timestamp=data.timeStamp / 1000,
            arbitration_id=data.frame.can_id,
            is_extended_id=data.frame.eff,
            is_remote_frame=data.frame.rtr,
            is_error_frame=data.frame.err,
            channel=msg.chn,
            dlc=data.frame.len,
            data=bytes(data.frame.data),
            is_fd=data.flag.frameType,
            is_rx=True,
            bitrate_switch=data.frame.brs,
            error_state_indicator=data.frame.esi,
        ), data.flag.txEchoed
    else:
        raise ZCANException(f'Unknown message type: {type(msg)}')


class ZCanBus(BusABC):

    def __init__(self,
                 channel: Union[int, Sequence[int], str] = None, *,
                 resend: bool = False,
                 device_type: ZCANDeviceType,
                 device_index: int = 0,
                 derive: bool = False,
                 rx_queue_size: Optional[int] = None,
                 configs: Union[list, tuple] = None,
                 can_filters: Optional[can.typechecking.CanFilters] = None,
                 **kwargs: object):
        """
        Init ZLG CAN Bus device.
        :param device_type: The device type in ZCANDeviceType.
        :param resend: Auto resend when transmit fail until success if True
        :param channel: A channel list(such as [0, 1]) or str split by ","(such as "0, 1") index cont from 0.
        :param device_index: The ZLG device index, default 0.
        :param rx_queue_size: The size of received queue.
        :param configs: The channel configs, is a list of dict:
            The index 0 is configuration for channel 0, index 1 is configuration for channel 1, and so on.
            When the system is Windows, the config key is:
                clock: [Optional] The clock of channel.
                bitrate: [Must] The arbitration phase baudrate.
                data_bitrate: [Optional] The data phase baudrate, default is baudrate.
                initenal_resistance: [Optional] the terminal resistance enable status, optional value{1:enable|0:disable}, default: 1
                mode: [Optional] The can mode, defined in ZCANCanMode, default is NORMAL
                filter: [Optional] The filter mode, defined in ZCANCanFilter, default is DOUBLE
                acc_code: [Optional] The frame filter acceptance code of SJA1000.
                acc_mask: [Optional] The frame mask code of SJA1000.
                brp: [Optional] The bit rate prescaler
                abit_timing: [Optional] The arbitration phase timing, ignored.
                dbit_timing: [Optional] The data phase timing, ignored.
                Other property value: please see: https://manual.zlg.cn/web/#/152/6364->设备属性, with out head "n/".
            When the system is Linux, the config key is:
                clock: [Must] The clock of channel.
                initenal_resistance: [Optional] the terminal resistance enable status, optional value{1:enable|0:disable}, default: 1
                arb_tseg1: [Must] The phase buffer time segment1 of arbitration phase.
                arb_tseg2: [Must] The phase buffer time segment2 of arbitration phase.
                arb_sjw: [Must] The synchronization jump width of arbitration phase.
                arb_smp: [Optional] Sample rate of arbitration phase, default is 0, Ignored.
                arb_brp: [Must] The bit rate prescaler of arbitration phase.
                data_tseg1: [Optional] The phase buffer time segment1 of data phase, default is arb_tseg1.
                data_tseg2: [Optional] The phase buffer time segment2 of data phase, default is arb_tseg2.
                data_sjw: [Optional] The synchronization jump width of data phase, default is arb_sjw.
                data_smp: [Optional] Sample rate of data phase, default is arb_smp, Ignored.
                data_brp: [Optional] The bit rate prescaler of data phase, default is arb_brp.
        :param can_filters: Not used.
        :param kwargs: Not used.
        """
        super().__init__(channel=channel, can_filters=can_filters, **kwargs)

        cfg_length = len(configs)
        if cfg_length == 0:
            raise CanInitializationError('ZLG-CAN - Configuration list or tuple of dict is required.')

        self.rx_queue = collections.deque(
            maxlen=rx_queue_size
        )  # type: Deque[Tuple[int, Any]]               # channel, raw_msg
        try:
            self.device = ZCAN(device_index, device_type, resend, derive)
            self.device.OpenDevice()
            self.channels = self.device.channels
            self.available = []
            self.channel_info = f"ZLG-CAN - device {device_index}, channels {self.channels}"
            # {'mode': 0|1(NORMAL|LISTEN_ONLY), 'filter': 0|1(DOUBLE|SINGLE), 'acc_code': 0x0, 'acc_mask': 0xFFFFFFFF,
            # 'brp': 0, 'abit_timing': 0, 'dbit_timing': 0}

            for index, channel in enumerate(self.channels):
                try:
                    config: dict = configs[index]
                except IndexError:
                    LOG.warning(f'ZLG-CAN - channel:{channel} not initialized.')
                    continue
                init_config = {}
                if _os.lower() == 'windows':
                    mode = config.get('mode', None)
                    if mode is not None:
                        init_config['mode'] = mode
                        del config['mode']
                    filter = config.get('filter', None)
                    if filter is not None:
                        init_config['filter'] = filter
                        del config['filter']
                    acc_code = config.get('acc_code', None)
                    if acc_code is not None:
                        init_config['acc_code'] = acc_code
                        del config['acc_code']
                    acc_mask = config.get('acc_mask', None)
                    if acc_mask is not None:
                        init_config['acc_mask'] = acc_mask
                        del config['acc_mask']
                    brp = config.get('brp', None)
                    if brp is not None:
                        init_config['brp'] = brp
                        del config['brp']
                    abit_timing = config.get('abit_timing', None)
                    if abit_timing is not None:
                        init_config['abit_timing'] = abit_timing
                        del config['abit_timing']
                    dbit_timing = config.get('dbit_timing', None)
                    if dbit_timing is not None:
                        init_config['dbit_timing'] = dbit_timing
                        del config['dbit_timing']

                    bitrate = config.get('bitrate', None)
                    if bitrate is None:
                        raise CanInitializationError('ZLG-CAN - bitrate is required.')
                    del config['bitrate']

                    if self.device.device_is_canfd:
                        config['canfd_abit_baud_rate'] = bitrate

                        data_bitrate = config.get('data_bitrate', None)
                        if data_bitrate is None:
                            config['canfd_dbit_baud_rate'] = bitrate
                        else:
                            del config['data_bitrate']
                            config['canfd_dbit_baud_rate'] = data_bitrate
                    else:
                        init_config['bitrate'] = bitrate

                    initenal_resistance = config.get("initenal_resistance", None)
                    if initenal_resistance is not None:
                        init_config['initenal_resistance'] = initenal_resistance
                        del config['initenal_resistance']

                    if hasattr(self.device, 'SetValue'):
                        # try:
                        #     self.device.SetValue(channel, **config)
                        # except ZCANException:
                        #     pass
                        LOG.debug(f"SetValue: {config}")
                        self.device.SetValue(channel, **config)
                elif _os.lower() == 'linux':
                    init_config = config
                LOG.debug(f"InitCAN: {init_config}")
                self.device.InitCAN(channel, **init_config)
                self.device.StartCAN(channel)
                self.available.append(channel)
        except ZCANException as e:
            self.shutdown()
            raise CanInitializationError(str(e))

    def _recv_from_queue(self) -> Tuple[Message, bool]:
        """Return a message from the internal receive queue"""
        channel, raw_msg = self.rx_queue.popleft()

        return zlg_convert_msg(raw_msg, channel=channel, is_rx=True, device_type=self.device.device_type), False

    def poll_received_messages(self, timeout):
        try:
            for channel in self.available:
                can_num = self.device.GetReceiveNum(channel, ZCANMessageType.CAN)
                canfd_num = self.device.GetReceiveNum(channel, ZCANMessageType.CANFD)
                if can_num:
                    LOG.debug(f'ZLG-CAN - can message received: {can_num}.')
                    self.rx_queue.extend(
                        (channel, raw_msg) for raw_msg in self.device.Receive(channel, can_num, timeout)
                    )
                if canfd_num:
                    LOG.debug(f'ZLG-CAN - canfd message received: {canfd_num}.')
                    self.rx_queue.extend(
                        (channel, raw_msg) for raw_msg in self.device.ReceiveFD(channel, canfd_num, timeout)
                    )
        except ZCANException as e:
            raise CanOperationError(str(e))

    def _recv_internal(self, timeout: Optional[float]) -> Tuple[Optional[Message], bool]:

        if self.rx_queue:
            return self._recv_from_queue()

        deadline = None
        while deadline is None or time.time() < deadline:
            if deadline is None and timeout is not None:
                deadline = time.time() + timeout

            self.poll_received_messages(timeout)

            if self.rx_queue:
                return self._recv_from_queue()

        return None, False

    def send(self, msg: Message, timeout: Optional[float] = None, **kwargs) -> None:
        try:
            channel = msg.channel
            if len(self.available) > 0 and channel is None:
                channel = self.available[0]
            if channel not in self.available:
                raise CanOperationError(f'Channel: {channel} not in {self.available}')
            is_merge = self.device.MergeEnabled() if hasattr(self.device, 'MergeEnabled') else False
            if is_merge:
                return self.device.TransmitData(zlg_convert_msg(msg, channel=channel, resend=self.device.resend, is_merge=is_merge, **kwargs), 1)
            else:
                if msg.is_fd:
                    return self.device.TransmitFD(channel, zlg_convert_msg(msg, resend=self.device.resend, channel=channel, is_merge=is_merge, **kwargs), 1)
                return self.device.Transmit(channel, zlg_convert_msg(msg, resend=self.device.resend, channel=channel, is_merge=is_merge, device_type=self.device.device_type, **kwargs), 1)
        except ZCANException as e:
            raise CanOperationError(str(e))

    @staticmethod
    def _detect_available_configs():                    # -> List[can.typechecking.AutoDetectedConfig]:
        warnings.warn('Not supported by ZLG-CAN device.', DeprecationWarning, 2)

    def fileno(self):
        warnings.warn('Not supported by ZLG-CAN device.', DeprecationWarning, 2)

    def shutdown(self) -> None:
        LOG.debug('ZLG-CAN - shutdown.')
        super().shutdown()
        self.device.CloseDevice()

    def clear_rx_buffer(self, channel=None):
        if channel:
            assert channel in self.available
            self.device.ClearBuffer(channel)
        else:
            for channel in self.available:
                self.device.ClearBuffer(channel)

    def set_hardware_filters(self, channel, filters: Optional[can.typechecking.CanFilters]):
        assert channel in self.available, f'channel: {channel} is not initialized!'
        _filters = []
        for flt in filters:
            can_id = flt.get('can_id')
            can_mask = flt.get('can_mask')
            extended = False
            if isinstance(flt, can.typechecking.CanFilterExtended):
                extended = flt.get('extended')
            end = ~(can_id ^ can_mask)
            if end < 0:
                end = -end
            LOG.debug(f'~(can_id ^ can_mask): {bin(end)}')
            _filters.append((1 if extended else 0, can_id, end))

        self.device.SetFilters(channel, _filters)
