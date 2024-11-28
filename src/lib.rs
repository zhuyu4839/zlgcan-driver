use std::sync::{Arc, Mutex};
use pyo3::{exceptions, prelude::*, types::PyDict, wrap_pyfunction};
use rs_can::{Direct, Frame, Id};
use zlgcan::{can::{CanChlCfg, CanChlCfgExt, CanChlCfgFactory, CanMessage, ZCanFrameType}, device::DeriveInfo, driver::{ZCanDriver, ZDevice}};

#[pyclass]
#[derive(Clone)]
struct ZCanChlCfgPy {
    dev_type: u32,
    chl_type: u8,
    chl_mode: u8,
    bitrate: u32,
    filter: Option<u8>,
    dbitrate: Option<u32>,
    resistance: Option<bool>,
    acc_code: Option<u32>,
    acc_mask: Option<u32>,
    brp: Option<u32>,
}

#[pymethods]
impl ZCanChlCfgPy {
    #[new]
    #[pyo3(signature = (dev_type, chl_type, chl_mode, bitrate, filter=None, dbitrate=None, resistance=None, acc_code=None, acc_mask=None, brp=None))]
    fn new(
        dev_type: u32,
        chl_type: u8,
        chl_mode: u8,
        bitrate: u32,
        filter: Option<u8>,
        dbitrate: Option<u32>,
        resistance: Option<bool>,
        acc_code: Option<u32>,
        acc_mask: Option<u32>,
        brp: Option<u32>,
    ) -> Self {
        ZCanChlCfgPy {
            dev_type,
            chl_type,
            chl_mode,
            bitrate,
            filter,
            dbitrate,
            resistance,
            acc_code,
            acc_mask,
            brp,
        }
    }
}

impl ZCanChlCfgPy {
    fn try_convert(&self, factory: &ZCanChlCfgFactoryWrap) -> PyResult<CanChlCfg> {
        factory.inner.new_can_chl_cfg(
            self.dev_type,
            self.chl_type,
            self.chl_mode,
            self.bitrate,
            CanChlCfgExt::new(
                self.filter,
                self.dbitrate,
                self.resistance,
                self.acc_code,
                self.acc_mask,
                self.brp
            )
        ).map_err(|e| exceptions::PyValueError::new_err(e.to_string()))
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct ZCanMessagePy {
    timestamp: u64,
    arbitration_id: u32,
    is_extended_id: bool,
    is_remote_frame: bool,
    is_error_frame: bool,
    channel: u8,
    data: Vec<u8>,
    is_fd: bool,
    is_rx: bool,
    bitrate_switch: bool,
    error_state_indicator: bool,
    tx_mode: u8,
}

impl From<CanMessage> for ZCanMessagePy {
    fn from(value: CanMessage) -> Self {
        let data = Vec::from(value.data());
        let id = value.id();
        let is_extended_id = id.is_extended();
        ZCanMessagePy {
            timestamp: value.timestamp(),
            arbitration_id: id.as_raw(),
            is_extended_id,
            is_remote_frame: value.is_remote(),
            is_error_frame: value.is_error_frame(),
            channel: value.channel(),
            data,
            is_fd: value.is_can_fd(),
            is_rx: match value.direct() {
                Direct::Transmit => false,
                Direct::Receive => true,
            },
            bitrate_switch: value.is_bitrate_switch(),
            error_state_indicator: value.is_error_frame(),
            tx_mode: value.tx_mode(),
        }
    }
}

impl TryInto<CanMessage> for ZCanMessagePy {
    type Error = PyErr;

    fn try_into(self) -> Result<CanMessage, Self::Error> {
        let mut msg = if self.is_error_frame {
            CanMessage::new_remote(
                Id::from_bits(self.arbitration_id, false),
                self.data.len(),
            )
        }
        else {
            CanMessage::new(
                Id::from_bits(self.arbitration_id, false),
                self.data.as_slice(),
            )
        }.ok_or(PyErr::new::<exceptions::PyRuntimeError, String>("Can't new CAN message".into()))?;
        msg.set_timestamp(None)
            .set_direct(if self.is_rx { Direct::Receive } else { Direct::Transmit })
            .set_channel(self.channel)
            .set_tx_mode(self.tx_mode)
            .set_can_fd(self.is_fd)
            .set_bitrate_switch(self.bitrate_switch)
            .set_esi(self.error_state_indicator)
            .set_error_frame(self.is_error_frame);
        Ok(msg)
    }
}

impl ZCanMessagePy {

    fn to_python<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let can_mod = py.import("can")?;
        let message_class = can_mod.getattr("Message")?;

        let kwargs = PyDict::new(py);
        kwargs.set_item("timestamp", self.timestamp as f64 / 1000.)?;
        kwargs.set_item("arbitration_id", self.arbitration_id)?;
        kwargs.set_item("is_extended_id", self.is_extended_id)?;
        kwargs.set_item("is_remote_frame", self.is_remote_frame)?;
        kwargs.set_item("is_error_frame", self.is_error_frame)?;
        kwargs.set_item("channel", self.channel)?;
        kwargs.set_item("dlc", self.data.len())?;
        kwargs.set_item("channel", self.channel)?;
        kwargs.set_item("data", self.data.clone())?;
        kwargs.set_item("is_fd", self.is_fd)?;
        kwargs.set_item("is_rx", self.is_rx)?;
        kwargs.set_item("bitrate_switch", self.bitrate_switch)?;
        kwargs.set_item("error_state_indicator", self.error_state_indicator)?;

        message_class.call((), Some(&kwargs))
    }

    fn from_python<'py>(_py: Python<'py>, py_message: &Bound<'py, PyAny>) -> PyResult<Self> {
        let timestamp: f64 = py_message.getattr("timestamp")?.extract()?;
        let timestamp = (timestamp * 1000.) as u64;
        let arbitration_id: u32 = py_message.getattr("arbitration_id")?.extract()?;
        let is_extended_id: bool = py_message.getattr("is_extended_id")?.extract()?;
        let is_remote_frame: bool = py_message.getattr("is_remote_frame")?.extract()?;
        let is_error_frame: bool = py_message.getattr("is_error_frame")?.extract()?;
        let channel: u8 = py_message.getattr("channel")?.extract()?;
        let data: Vec<u8> = py_message.getattr("data")?.extract()?;
        let is_fd: bool = py_message.getattr("is_fd")?.extract()?;
        let is_rx: bool = py_message.getattr("is_rx")?.extract()?;
        let bitrate_switch: bool = py_message.getattr("bitrate_switch")?.extract()?;
        let error_state_indicator: bool = py_message.getattr("error_state_indicator")?.extract()?;

        Ok(ZCanMessagePy {
            timestamp,
            arbitration_id,
            is_extended_id,
            is_remote_frame,
            is_error_frame,
            channel,
            data,
            is_fd,
            is_rx,
            bitrate_switch,
            error_state_indicator,
            tx_mode: 0,
        })
    }
}

#[pyfunction]
fn convert_to_python<'py>(py: Python<'py>, rust_message: ZCanMessagePy) -> PyResult<Bound<'py, PyAny>> {
    rust_message.to_python(py)
}

#[allow(dead_code)]
#[pyfunction]
fn convert_from_python<'py>(py: Python<'py>, py_message: &Bound<'py, PyAny>) -> PyResult<ZCanMessagePy> {
    ZCanMessagePy::from_python(py, py_message)
}

#[pyclass]
#[derive(Default, Clone)]
struct ZDeriveInfoPy {
    pub(crate) canfd: bool,
    pub(crate) channels: u8,
}

#[pymethods]
impl ZDeriveInfoPy {
    #[new]
    fn new(canfd: bool, channels: u8) -> Self {
        Self { canfd, channels }
    }
}

impl Into<DeriveInfo> for ZDeriveInfoPy {
    fn into(self) -> DeriveInfo {
        DeriveInfo::new(self.canfd, self.channels)
    }
}

#[pyclass]
#[derive(Clone)]
struct ZCanChlCfgFactoryWrap {
    inner: Arc<CanChlCfgFactory>
}

#[pyclass]
#[derive(Clone)]
struct ZCanDriverWrap {
    inner: Arc<Mutex<ZCanDriver>>,
}

#[pyfunction]
fn zlgcan_cfg_factory_can() -> PyResult<ZCanChlCfgFactoryWrap> {
    let factory = CanChlCfgFactory::new()
        .map_err(|e| PyErr::new::<exceptions::PyRuntimeError, String>(e.to_string()))?;
    Ok(ZCanChlCfgFactoryWrap { inner: Arc::new(factory) })
}

#[pyfunction]
#[pyo3(signature = (dev_type, dev_idx, derive=None))]
fn zlgcan_open(
    dev_type: u32,
    dev_idx: u32,
    derive: Option<ZDeriveInfoPy>
) -> PyResult<ZCanDriverWrap> {
    let derive_info = match derive {
        Some(v) => Some(v.into()),
        None => None,
    };
    let mut device = ZCanDriver::new(dev_type, dev_idx, derive_info)
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    device.open()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;

    Ok(ZCanDriverWrap { inner: Arc::new(Mutex::new(device)) })
}

#[pyfunction]
fn zlgcan_device_info(device: &ZCanDriverWrap) -> PyResult<String> {
    let device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    Ok(
        device.device_info()
            .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?
            .to_string()
    )
}

#[pyfunction]
fn zlgcan_init_can(
    device: &ZCanDriverWrap,
    factory: ZCanChlCfgFactoryWrap,
    cfg: Vec<ZCanChlCfgPy>
) -> PyResult<()> {
    let mut device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    let cfg = cfg.into_iter()
        .map(|c| c.try_convert(&factory))
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| e)?;
    device.init_can_chl(cfg)
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))
}

#[pyfunction]
fn zlgcan_clear_can_buffer(
    device: &ZCanDriverWrap,
    channel: u8,
) -> PyResult<()> {
    let device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    device.clear_can_buffer(channel)
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))
}

#[pyfunction]
fn zlgcan_send(
    device: &ZCanDriverWrap,
    msg: ZCanMessagePy,
) -> PyResult<u32> {
    let device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    let message: CanMessage = msg.try_into()?;
    if message.is_can_fd() {
        device.transmit_canfd(message.channel(), vec![message, ])
            .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))
    }
    else {
        device.transmit_can(message.channel(), vec![message, ])
            .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))
    }
}

#[pyfunction]
#[pyo3(signature = (device, channel, timeout=None))]
fn zlgcan_recv<'py>(
    device: &ZCanDriverWrap,
    channel: u8,
    timeout: Option<u32>,
) -> PyResult<Vec<ZCanMessagePy>> {
    let device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;

    let can_cnt = device.get_can_num(channel, ZCanFrameType::CAN)
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    let canfd_cnt = device.get_can_num(channel, ZCanFrameType::CANFD)
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    let mut results = Vec::with_capacity((can_cnt + canfd_cnt) as usize);

    if can_cnt > 0 {
        let mut can_frames = device.receive_can(channel, can_cnt, timeout)
            .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
        results.append(&mut can_frames);
    }
    if canfd_cnt > 0 {
        let mut canfd_frames = device.receive_canfd(channel, canfd_cnt, timeout)
            .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
        results.append(&mut canfd_frames);
    }

    Ok(results.into_iter()
        .map(ZCanMessagePy::from)
        .collect::<Vec<_>>())
}

#[pyfunction]
fn zlgcan_close(
    device: &ZCanDriverWrap
) -> PyResult<()> {
    let mut device = device.inner.lock()
        .map_err(|e| exceptions::PyValueError::new_err(e.to_string()))?;
    device.close();
    Ok(())
}

#[pyfunction]
fn set_message_mode(msg: &mut ZCanMessagePy, mode: u8) {
    msg.tx_mode = mode;
}

#[pymodule]
fn zlgcan_driver_py(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ZCanChlCfgPy>()?;
    m.add_class::<ZCanMessagePy>()?;
    m.add_class::<ZDeriveInfoPy>()?;
    m.add_class::<ZCanChlCfgFactoryWrap>()?;
    m.add_class::<ZCanDriverWrap>()?;

    m.add_function(wrap_pyfunction!(convert_to_python, m)?)?;
    m.add_function(wrap_pyfunction!(convert_from_python, m)?)?;
    m.add_function(wrap_pyfunction!(set_message_mode, m)?)?;

    m.add_function(wrap_pyfunction!(zlgcan_cfg_factory_can, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_open, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_device_info, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_init_can, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_clear_can_buffer, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_send, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_recv, m)?)?;
    m.add_function(wrap_pyfunction!(zlgcan_close, m)?)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use std::time::Instant;
    use zlgcan::can::{ZCanChlMode, ZCanChlType};
    use zlgcan::device::ZCanDeviceType;
    use super::*;

    #[test]
    fn test_receive() -> anyhow::Result<()> {
        pyo3::prepare_freethreaded_python();

        let cfg_fct = zlgcan_cfg_factory_can()?;
        let device = zlgcan_open(ZCanDeviceType::ZCAN_USBCANFD_200U as u32, 0, None)?;

        let dev_info = zlgcan_device_info(&device)?;
        println!("{}", dev_info);

        let cfg = ZCanChlCfgPy::new(
            ZCanDeviceType::ZCAN_USBCANFD_200U as u32,
            ZCanChlType::CANFD_ISO as u8,
            ZCanChlMode::Normal as u8,
            500_000,
            None,
            Some(1_000_000),
            None,
            None,
            None,
            None,
        );
        zlgcan_init_can(&device, cfg_fct, vec![cfg, ])?;
        std::thread::sleep(std::time::Duration::from_secs(1));

        let start = Instant::now();
        let mut flag = false;
        while start.elapsed().as_secs() < 15 {
            let msgs = zlgcan_recv(&device, 0, None)?;
            println!("{:?}", msgs);
            if !msgs.is_empty() {
                flag = true;
            }
            drop(msgs);

            if flag {
                break;
            }
        }

        zlgcan_close(&device)?;

        Ok(())
    }
}
