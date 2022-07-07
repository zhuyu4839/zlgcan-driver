import collections
import ctypes
import logging
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
from zlgcan import ZCAN, ZCANDeviceType, ZCAN_Transmit_Data, ZCAN_TransmitFD_Data, ZCAN_Receive_Data, \
    ZCAN_ReceiveFD_Data, ZCANDataObj, ZCANException, ZCANMessageType, ZCANCanTransType

logger = logging.getLogger(__name__)

# AFTER_OPEN_DEVICE = [
#     'tx_timeout',
# ]
#
# BEFORE_INIT_CAN = [
#     'canfd_standard',
#     'protocol',
#     'canfd_abit_baud_rate',
#     'canfd_dbit_baud_rate',
#     'baud_rate_custom',
# ]
#
# AFTER_INIT_CAN = [
#     'initenal_resistance',
#     'filter_mode',
#     'filter_start',
#     'filter_end',
#     'filter_ack',
#     'filter_clear',
# ]
#
# BEFOR_START_CAN = [
#     'set_bus_usage_enable',
#     'set_bus_usage_period',
# ]
#
# AFTER_START_CAN = [
#     'auto_send',
#     'auto_send_canfd',
#     'auto_send_param',
#     'clear_auto_send',
#     'apply_auto_send',
#     'set_send_mode',
# ]
ZCAN_Transmit_Data_1 = (ZCAN_Transmit_Data * 1)
ZCAN_TransmitFD_Data_1 = (ZCAN_TransmitFD_Data * 1)
ZCANDataOb_1 = (ZCANDataObj * 1)


def _convert_msg(msg, **kwargs):                        # channel=None, trans_type=0, is_merge=False, **kwargs):

    if isinstance(msg, Message):                        # 发送报文转换
        is_merge = kwargs.get('is_merge', None)
        trans_type = kwargs.get('trans_type', ZCANCanTransType.NORMAL)
        assert is_merge is not None, 'is_merge required when convert to ZLG.'
        # assert trans_type is not None, 'trans_type required when convert to ZLG.'
        if not is_merge:
            if msg.is_fd:
                result = ZCAN_TransmitFD_Data_1()
                data = ZCAN_TransmitFD_Data()
                data.frame.len = msg.dlc
                data.frame.brs = msg.bitrate_switch
            else:
                result = ZCAN_Transmit_Data_1()
                data = ZCAN_Transmit_Data()
                data.frame.can_dlc = msg.dlc
            data.transmit_type = trans_type

            data.frame.can_id = msg.arbitration_id
            data.frame.err = msg.is_error_frame
            data.frame.rtr = msg.is_remote_frame
            data.frame.eff = msg.is_extended_id
            data.frame.data = (ctypes.c_ubyte * msg.dlc)(*msg.data)
            result[0] = data
            return result
        else:
            channel = kwargs.get('channel', None)
            assert channel is not None, 'channel required when merge send recv.'
            result = ZCANDataOb_1()
            data = ZCANDataObj()
            data.dataType = 1                     # can device always equal 1
            assert channel is not None
            data.chnl = channel
            data.data.zcanCANFDData.frame.can_id = msg.arbitration_id
            data.data.zcanCANFDData.frame.err = msg.is_error_frame
            data.data.zcanCANFDData.frame.rtr = msg.is_remote_frame
            data.data.zcanCANFDData.frame.eff = msg.is_extended_id

            data.data.zcanCANFDData.flag.transmitType = trans_type
            echo = kwargs.get('is_echo', False)
            data.data.zcanCANFDData.flag.txEchoRequest = echo
            delay = kwargs.get('delay_mode', 0)
            if delay:
                data.data.zcanCANFDData.flag.txDelay = delay
                data.data.zcanCANFDData.timeStamp = kwargs['delay_time']
            result[0] = data
            return result
    elif isinstance(msg, ZCAN_Receive_Data):                        # 接收CAN报文转换
        channel = kwargs.get('channel', None)
        assert channel is not None, 'channel required when convert ZLG CAN msg to std msg.'
        return Message(
            timestamp=msg.timestamp,
            arbitration_id=msg.frame.can_id,
            is_extended_id=msg.frame.eff,
            is_remote_frame=msg.frame.efr,
            is_error_frame=msg.frame.err,
            channel=channel,
            dlc=msg.frame.can_dlc,
            data=bytes(msg.frame.data),
        )
    elif isinstance(msg, ZCAN_ReceiveFD_Data):                          # 接收CANFD报文转换
        channel = kwargs.get('channel', None)
        assert channel is not None, 'channel required when convert ZLG CANFD msg to std msg.'
        return Message(
            timestamp=msg.timestamp,
            arbitration_id=msg.frame.can_id,
            is_extended_id=msg.frame.eff,
            is_remote_frame=msg.frame.efr,
            is_error_frame=msg.frame.err,
            channel=channel,
            dlc=msg.frame.len,
            data=bytes(msg.frame.data),
            is_fd=True,
            # is_rx=True,
            bitrate_switch=msg.frame.brs,
            error_state_indicator=msg.frame.esi,
        )
    elif isinstance(msg, ZCANDataObj):                                  # 合并接收CAN|CANFD报文转换
        data = msg.data.zcanCANFDData
        return Message(
            timestamp=data.timeStamp,
            arbitration_id=data.frame.can_id,
            is_extended_id=data.frame.eff,
            is_remote_frame=data.frame.efr,
            is_error_frame=data.frame.err,
            channel=msg.chnl,
            dlc=data.frame.len,
            data=bytes(data.frame.data),
            is_fd=data.flag.frameType,
            bitrate_switch=data.frame.brs,
            error_state_indicator=data.frame.esi,
        ), data.flag.txEchoed
    else:
        raise ZCANException(f'Unknown message type: {type(msg)}')


class ZCanBus(BusABC):

    def __init__(self,
                 device_type: ZCANDeviceType,
                 channel: Union[int, Sequence[int], str] = None,
                 device_index: int = 0,
                 rx_queue_size: Optional[int] = None,
                 configs: Union[list, tuple] = None,
                 can_filters: Optional[can.typechecking.CanFilters] = None,
                 **kwargs: object):
        super().__init__(channel=channel, can_filters=can_filters, **kwargs)

        cfg_length = len(configs)
        if cfg_length == 0:
            raise CanInitializationError('ZLG-CAN: Configuration dict of list or tuple is required.')

        self.rx_queue = collections.deque(
            maxlen=rx_queue_size
        )  # type: Deque[Tuple[int, Any]]               # channel, raw_msg

        self.device = ZCAN()
        self.device.OpenDevice(device_type, device_index)
        self.channels = self.device.channels
        self.available = []
        self.channel_info = f"ZLG-CAN: device {device_index}, channels {self.channels}"
        # {'mode': 0|1(NORMAL|LISTEN_ONLY), 'filter': 0|1(DOUBLE|SINGLE), 'acc_code': 0x0, 'acc_mask': 0xFFFFFFFF,
        # 'brp': 0, 'abit_timing': 0, 'dbit_timing': 0}

        for index, channel in enumerate(self.channels):
            try:
                config: dict = configs[index]
            except IndexError:
                LOG.warn(f'ZLG-CAN: channel{channel} not initialized.')
                return
            init_config = {}

            mode = config.get('mode', None)
            if mode:
                init_config['mode'] = mode
                del config['mode']
            filter = config.get('filter', None)
            if mode:
                init_config['filter'] = filter
                del config['filter']
            acc_code = config.get('acc_code', None)
            if mode:
                init_config['acc_code'] = acc_code
                del config['acc_code']
            acc_mask = config.get('acc_mask', None)
            if mode:
                init_config['acc_mask'] = acc_mask
                del config['acc_mask']
            brp = config.get('brp', None)
            if mode:
                init_config['brp'] = brp
                del config['brp']
            abit_timing = config.get('dbit_timing', None)
            if mode:
                init_config['abit_timing'] = abit_timing
                del config['abit_timing']
            dbit_timing = config.get('dbit_timing', None)
            if mode:
                init_config['dbit_timing'] = dbit_timing
                del config['dbit_timing']

            if 'canfd_abit_baud_rate' not in config.keys():
                raise CanInitializationError('ZLG-CAN: canfd_abit_baud_rate is required.')

            self.device.InitCAN(channel, **init_config)
            self.device.SetValue(channel, **config)
            self.device.StartCAN(channel)
            self.available.append(channel)

    def _apply_filters(self, filters: Optional[can.typechecking.CanFilters]) -> None:
        pass

    def _recv_from_queue(self) -> Tuple[Message, bool]:
        """Return a message from the internal receive queue"""
        channel, raw_msg = self.rx_queue.popleft()

        return _convert_msg(raw_msg, channel=channel), False

    def poll_received_messages(self):
        for channel in self.available:
            can_num = self.device.GetReceiveNum(channel, ZCANMessageType.CAN)
            canfd_num = self.device.GetReceiveNum(channel, ZCANMessageType.CAN)
            if can_num:
                LOG.debug(f'ZLG-CAN: can message received: {can_num}.')
                self.rx_queue.extend(
                    (channel, raw_msg) for raw_msg in self.device.Receive(channel, can_num, 10)
                )
            if canfd_num:
                LOG.debug(f'ZLG-CAN: canfd message received: {canfd_num}.')
                self.rx_queue.extend(
                    (channel, raw_msg) for raw_msg in self.device.ReceiveFD(channel, canfd_num, 10)
                )

    def _recv_internal(self, timeout: Optional[float]) -> Tuple[Optional[Message], bool]:

        if self.rx_queue:
            return self._recv_from_queue()

        deadline = None
        while deadline is None or time.time() < deadline:
            if deadline is None and timeout is not None:
                deadline = time.time() + timeout

            self.poll_received_messages()

            if self.rx_queue:
                return self._recv_from_queue()

        return None, False

    def send(self, msg: Message, timeout: Optional[float] = None, **kwargs) -> None:
        channel = msg.channel
        if channel not in self.available:
            raise CanOperationError(f'Channel: {channel} not in {self.available}')
        is_merge = self.device.MergeEnabled() if hasattr(self.device, 'MergeEnabled') else False
        if is_merge:
            return self.device.TransmitData(_convert_msg(msg, channel=channel, is_merge=is_merge, **kwargs), 1)
        else:
            if msg.is_fd:
                return self.device.TransmitFD(channel, _convert_msg(msg, channel=channel, is_merge=is_merge, **kwargs), 1)
            return self.device.Transmit(channel, _convert_msg(msg, channel=channel, is_merge=is_merge, **kwargs), 1)

    @staticmethod
    def _detect_available_configs():                    # -> List[can.typechecking.AutoDetectedConfig]:
        warnings.warn('Not supported by ZLG-CAN device.', DeprecationWarning, 2)

    def fileno(self):
        warnings.warn('Not supported by ZLG-CAN device.', DeprecationWarning, 2)

    def shutdown(self) -> None:
        super().shutdown()
        self.device.CloseDevice()



