use pyo3::prelude::*;
use std::sync::{Arc, Mutex};
use zlgcan::driver::ZDriver;

#[pyclass(from_py_object)]
#[derive(Clone)]
pub struct ZCanDriverWrap {
    pub(crate) inner: Arc<Mutex<ZDriver>>,
}

#[pyclass(from_py_object)]
#[derive(Clone)]
pub struct ZCanChlCfgPy {
    pub(crate) chl_type: u8,
    pub(crate) chl_mode: u8,
    pub(crate) bitrate: u32,
    pub(crate) filter: Option<u8>,
    pub(crate) dbitrate: Option<u32>,
    pub(crate) resistance: Option<bool>,
    pub(crate) acc_code: Option<u32>,
    pub(crate) acc_mask: Option<u32>,
    pub(crate) brp: Option<u32>,
}

#[pymethods]
impl ZCanChlCfgPy {
    #[new]
    #[pyo3(signature = (chl_type, chl_mode, bitrate, filter=None, dbitrate=None, resistance=None, acc_code=None, acc_mask=None, brp=None))]
    pub fn new(
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
