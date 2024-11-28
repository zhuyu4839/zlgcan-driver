# ZLGCAN驱动及集成到python-can(因内存模型不同，目前Windows下32位python会报内存非法访问的错误)

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

4. 将`zlgcan`文件夹拷贝到`can/interfaces/`文件夹下
5. 安装zlgcan-driver-py库:
   ```shell
   pip install zlgcan-driver-py

6. 准备
   * 确保安装相关驱动(USBCAN-I/II驱动得额外安装)
   * 确保安装相[VC++运行环境](https://manual.zlg.cn/web/#/152?page_id=5332)
   * 将[library](https://github.com/zhuyu4839/zlgcan-driver/tree/rust-dev/zlgcan-driver/library)文件夹及[bitrate.cfg.yaml](https://github.com/zhuyu4839/zlgcan-driver/blob/rust-dev/zlgcan-driver/library/bitrate.cfg.yaml)文件拷贝到当目录(v0.1.5前版本)
   * 在当前工程目录下新建一个`zcan.env`文件, 中间配置`ZCAN_LIBRARY`环境变量(相对路径/绝对路径),否则使用v0.1.5前版本默认路径:
     * `ZCAN_LIBRARY`为`library`父目录
     * 其中`v0.1.5`后版本文件夹内容示例如下:
     ```shell
     └─root
       └─library
         ├─linux
         │  └─x86_64
         ├─windows
         │  ├─x86
         │  └─x86_64
         └─ bitrate.cfg.yaml
     ```
      * `v0.1.5`前版本文件夹内容示例如下:
     ```shell
     └─root
       ├─library
       │  ├──linux
       │  │  └─x86_64
       │  └─windows
       │     ├─x86
       │     └─x86_64
       └─ bitrate.cfg.yaml
     ```
   * 以下为示例
   ```shell
   ZCAN_LIBRARY="C:/your_library_path"
   ```

7. 使用:
   ```python
   import can
   from can.interfaces.zlgcan import ZCanTxMode, ZCANDeviceType
   
   with can.Bus(interface="zlgcan", device_type=ZCANDeviceType.ZCAN_USBCANFD_200U,
                configs=[{'bitrate': 500000, 'resistance': 1}, {'bitrate': 500000, 'resistance': 1}]) as bus:
       bus.send(can.Message(
           arbitration_id=0x123,
           is_extended_id=False,
           channel=0,
           data=[0x01, 0x02, 0x03, ],
           dlc=3,
       ), tx_mode=ZCanTxMode.SELF_SR)
   
       # time.sleep(0.1)
       _msg = bus.recv()
       print(_msg)

8. CAN测试列表：
   * USBCAN-I-mini - ZCAN_USBCAN1, ZCAN_USBCAN2
   * USBCAN-4E-U - ZCAN_USBCAN_4E_U
   * USBCANFD-100U-mini - ZCAN_USBCANFD_MINI
   * USBCANFD-100U - ZCAN_USBCANFD_100U
   * USBCANFD-200U - ZCAN_USBCANFD_200U
   * USBCANFD-800U - ZCAN_USBCANFD_800U

9. 注意事项:
   * ZCAN_USBCAN1及ZCAN_USBCAN2类型的设备无论是windows还是Linux, 波特率支持均在`bitrate.cfg.yaml`中配置
     * 此时计算timing0及timing1请下载[CAN波特率计算软件](https://zlg.cn/can/down/down/id/22.html)
   * 其他CANFD类型的CAN卡仅仅在Linux上使用时`bitrate.cfg.yaml`中配置
     * 此时计算相关值可以通过`ZCANPRO`软件
   * 在Linux上使用ZCAN_USBCAN1衍生CAN卡时, 请在初始化时候设置`ZCanDeriveInfo`信息
   * 该库主要依赖[zlgcan-driver-rs](https://github.com/zhuyu4839/ecu-proto-rs),如有问题,请提[issue](https://github.com/zhuyu4839/ecu-proto-rs/issues/new)

10. 官方工具及文档:
   * [工具下载](https://zlg.cn/can/down/down/id/22.html)
   * [驱动下载](https://manual.zlg.cn/web/#/146)
   * [二次开发文档](https://manual.zlg.cn/web/#/42/1710)
   * [二次开发文档CANFD-Linux](https://manual.zlg.cn/web/#/188/6982)
   * [二次开发Demo](https://manual.zlg.cn/web/#/152/5332)

