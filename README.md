# ZLGCAN驱动及集成到python-can

1. 安装python-can

    ```shell
    pip install python-can
    ```

2. 找到python-can安装路径

   1. 一般不用虚拟环境安装则在python安装路径下Lib/site-packages
   2. 使用虚拟环境则在虚拟环境下Lib/site-packages

3. 修改python-can路径下的can/interfaces/\_\_init__.py文件, 在BACKENDS字典中添加一行:

   ```
   	"zlgcan": ("can.interfaces.zlgcan", "ZCanBus"),
   ```

4. 把zlgcan文件夹拷贝到site-packages文件夹

5. 把zlgcan.py拷贝到can/interfaces/文件夹

6. 使用:

   - Windows下使用:

     ```python
     import can
     import time
     
     from zlgcan import ZCANDeviceType, ZCANCanTransType
     
     with can.Bus(bustype='zlgcan', device_type=ZCANDeviceType.ZCAN_USBCANFD_200U,
                  configs=[{'bitrate': 500000, 'initenal_resistance': 1}]  # 1通道配置
                  ) as bus:
         while True:
             msg = can.Message(
                 arbitration_id=0x01,
                 is_extended_id=False,
                 channel=0,
                 data=[0x01, 0x02, 0x01, 0x02, 0x01, 0x02, 0x01, 0x02, ],
                 is_rx=False,
             )
             bus.send(msg, trans_type=ZCANCanTransType.SELF_SR)
             time.sleep(0.05)
             print(bus.recv())
     ```

   - Linux下使用:

     ```python
     import can
     import time
     
     from zlgcan import ZCANDeviceType, ZCANCanTransType
     
     with can.Bus(bustype='zlgcan', device_type=ZCANDeviceType.ZCAN_USBCANFD_200U,
                  configs=[{'clock': 60_000_000, 'tseg1_abr': 7, 'tseg2_abr': 0, 'brp_abr': 11, 'sjw_abr': 0}]  # 1通道配置
                  ) as bus:
         while True:
             msg = can.Message(
                 arbitration_id=0x01,
                 is_extended_id=False,
                 channel=0,
                 data=[0x01, 0x02, 0x01, 0x02, 0x01, 0x02, 0x01, 0x02, ],
                 is_rx=False,
             )
             bus.send(msg, trans_type=ZCANCanTransType.SELF_SR)
             time.sleep(0.05)
             print(bus.recv())
     ```

     

