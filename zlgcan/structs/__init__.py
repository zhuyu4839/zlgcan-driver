"""
the c struct of ZLG-CAN that defined contains linux and windows
"""
__all__ = [
    "ZCAN_DEVICE_INFO",
]

from ctypes import Structure, c_uint16, c_uint8


class ZCAN_DEVICE_INFO(Structure):  # ZCAN_DEVICE_INFO

    _fields_ = [('hwv', c_uint16),  # /**< hardware version */
                ('fwv', c_uint16),  # /**< firmware version */
                ('drv', c_uint16),  # /**< driver version */
                ('api', c_uint16),  # /**< API version */
                ('irq', c_uint16),  # /**< IRQ */
                ('chn', c_uint8),  # /**< channels */
                ('sn', c_uint8 * 20),  # /**< serial number */
                ('id', c_uint8 * 40),  # /**< card id */
                ('pad', c_uint8 * 4)]

    def __str__(self):
        return f"Hardware Version : {self.hw_version}\n" \
               f"Firmware Version : {self.fw_version}\n" \
               f"Driver Version   : {self.dr_version}\n" \
               f"Interface Version: {self.in_version}\n" \
               f"Interrupt Number : {self.irq_num}\n" \
               f"CAN Number       : {self.can_num}\n" \
               f"Serial           : {self.serial}\n" \
               f"Hardware Type    : {self.hw_type}"

    @classmethod
    def _version(cls, version):
        return "V%02x.%02x" if version // 0xFF >= 9 else "V%d.%02x" % (version // 0xFF, version & 0xFF)

    @property
    def hw_version(self):
        return self._version(self.hwv)

    @property
    def fw_version(self):
        return self._version(self.fwv)

    @property
    def dr_version(self):
        return self._version(self.drv)

    @property
    def in_version(self):
        return self._version(self.api)

    @property
    def irq_num(self):
        return self.irq

    @property
    def can_num(self):
        return self.chn

    @property
    def serial(self):
        return bytes(self.sn).decode('utf-8')

    @property
    def hw_type(self):
        return bytes(self.id).decode('utf-8')