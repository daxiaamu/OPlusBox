# OPLUS Box

[![APK 下载量](stats/downloads.svg)](stats/downloads.md)

统计包含本仓库和 Xposed 模块仓库的 APK 下载次数，提供合计及各仓库明细。

Official APK releases and update metadata for com.daxiaamu.oplusbox.

For ColorOS 17. Application source code is private.

支持运行在 ColorOS 16 上，但功能可用性不做保证。

### 2.5.1

- 修复部分 ROOT 环境下 AirDrop 组件安装时的 SELinux 策略读取兼容问题
- 修复 AirDrop 启用时 DexKit 本地库未初始化导致的失败

[Android 开心版软件下载](https://pan.quark.cn/s/14e8a6044f77)

### 2.5.0

- 新增“状态栏允许永久显秒”，长按时钟可在关闭、显秒 5 分钟、始终显秒之间切换
- 改进 AirDrop 兼容性
- 增强型本地安装进一步加强
- 新增英语、日语、韩语、繁体中文

### AirDrop 支持

通过“快速分享”与苹果设备互相发送和接收文件，仅支持部分较新的设备。需要 ROOT、LSPosed 和匹配的 Google 服务／无线后端；缺失组件由盒子按需下载安装，部分设备需要重启。以应用实际检查结果为准。 采用元模块挂载的 SukiSU／KernelSU 环境，请先安装并启用挂载元模块（如官方 meta-overlayfs），重启后再安装互传组件。

[Android 开心版软件下载](https://pan.quark.cn/s/14e8a6044f77)
