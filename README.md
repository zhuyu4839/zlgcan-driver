# ZLGCAN驱动及集成到python-can(请先使用dev分支，main分支代码还有坑)

1. 安装python-can

    ```shell
    pip install python-can

2. 找到python-can安装路径

   1. windows下一般不用虚拟环境安装则在python安装路径下Lib/site-packages
   2. linux下一般不用虚拟环境安装则在用户home目录./locals/lib/PythonVersion/Lib目录下
   3. 使用虚拟环境则在虚拟环境下Lib/site-packages

3. 修改python-can路径下的can/interfaces/\_\_init\_\_.py文件, 在BACKENDS字典中添加一行:

   ```
   "zlgcan": ("can.interfaces.zlgcan", "ZCanBus"),

4. 把`zlgcan.py`及`library`文件夹及`libzlgcan_driver_rs_api.x86_64.so`或`zlgcan_driver_rs_api.x86.dll`或`zlgcan_driver_rs_api.x86_64.dll`拷贝到can/interfaces/文件夹

5. 使用:
     ```python
     import can
     import time
          
     with can.Bus(bustype='zlgcan', device_type=41,
                  configs=[{'bitrate': 500000, 'resistance': 1}, {'bitrate': 500000, 'resistance': 1}]  # 1通道配置
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

6. CAN测试列表：
   * USBCAN-I-mini - ZCAN_USBCAN1, ZCAN_USBCAN2
   * USBCANFD-100U-mini - ZCAN_USBCANFD_MINI
   * USBCANFD-100U - ZCAN_USBCANFD_100U
   * USBCANFD-200U - ZCAN_USBCANFD_200U

7. 注意事项:
   * ZCAN_USBCAN1及ZCAN_USBCAN2类型的设备无论是windows还是Linux, 波特率支持均在baudrate.conf.yaml中配置
     * 此时计算timing0及timing1请下载[CAN波特率计算软件](https://zlg.cn/can/down/down/id/22.html)
   * 其他CANFD类型的CAN卡仅仅在Linux上使用时baudrate.conf.yaml中配置
     * 此时计算相关值可以通过`ZCANPRO`软件
   * 在Linux上使用ZCAN_USBCAN1衍生CAN卡时, 请在初始化时候设置`ZCanDeriveInfo`信息
   * 该库主要依赖[zlgcan-driver-rs](https://github.com/zhuyu4839/zlgcan-driver-rs),如有问题,请提[issue](https://github.com/zhuyu4839/zlgcan-driver-rs/issues/new)

8. 官方工具及文档:
   * [工具下载](https://zlg.cn/can/down/down/id/22.html)
   * [驱动下载](https://manual.zlg.cn/web/#/146)
   * [二次开发文档](https://manual.zlg.cn/web/#/42/1710)
   * [二次开发文档CANFD-Linux](https://manual.zlg.cn/web/#/188/6982)
   * [二次开发Demo](https://manual.zlg.cn/web/#/152/5332)

