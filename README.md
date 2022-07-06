# ZLGCAN驱动及集成到python-can

1. 安装python-can

```shell
pip install python-can
```

2. 找到python-can安装路径

   1. 一般不用虚拟环境安装则在python安装路径下Lib/site-packages
   2. 使用虚拟环境则在虚拟环境下Lib/site-packages

3. 修改python-can路径下的can/interfaces/\__init__.py文件, 在BACKENDS字典中添加一行:

   ```python
   	"zlgcan": ("can.interfaces.zlgcan", "ZCanBus"),

4. 把zlgcan文件夹拷贝到site-packages文件夹

5. 把zlgcan.py拷贝到can/interfaces/文件夹

6. 使用:

   ```python
   import can
   from can.interfaces.zlgcan import ZCANDeviceType
   
   with can.Bus(bustype='zlgcan', device_type=ZCANDeviceType.ZCAN_USBCANFD_200U, 
                configs=[{'canfd_abit_baud_rate': 500000, 'initenal_resistance':1}, 	# 1通道配置
                         {'canfd_abit_baud_rate': 500000, 'initenal_resistance':1}]	# 2通道配置
               ) as bus:
       msg = bus.recv()
   ```

   

