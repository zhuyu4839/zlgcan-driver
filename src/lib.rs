pub(crate) mod wrappers;

use std::sync::{Arc, Mutex};
use pyo3::{exceptions, prelude::*};
use rs_can::Frame;
use zlgcan::{can::{CanChlCfgFactory, CanMessage, ZCanFrameType}, driver::{ZCanDriver, ZDevice}};
use crate::wrappers::{ZCanChlCfgFactoryWrap, ZCanChlCfgPy, ZCanDriverWrap, ZCanMessagePy, ZDeriveInfoPy};

#[pyfunction]
fn convert_to_python<'py>(py: Python<'py>, rust_message: ZCanMessagePy) -> PyResult<Bound<'py, PyAny>> {
    rust_message.to_python(py)
}

#[allow(dead_code)]
#[pyfunction]
fn convert_from_python<'py>(py: Python<'py>, py_message: &Bound<'py, PyAny>) -> PyResult<ZCanMessagePy> {
    ZCanMessagePy::from_python(py, py_message)
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
