# 项目交接文档

日期：2026-07-16

## 项目目标

面向视障用户做一个智能环境感知辅助系统：

- 手机或外置摄像头采集第一视角画面。
- 上传服务器进行 AI 视觉分析。
- 服务器返回简洁语音提示文本。
- 手机 TTS 播报危险预警或环境信息。

第一阶段目标不是完整导航，而是跑通：

```text
手机摄像头 -> 上传服务器 -> YOLO识别 -> 返回speak -> 手机播报
```

## 已完成

### 硬件与网络

- 红米 Note 14 已能通过浏览器访问 Mac 中转地址。
- Featurize RTX 4090 实例已验证 CUDA 可用。
- Mac 局域网 IP 当时为：`192.168.110.34`
- Mac 到 Featurize 的 SSH 隧道已验证可用：

```bash
ssh -N -L 0.0.0.0:18000:127.0.0.1:8000 -p <SSH_PORT> featurize@workspace.featurize.cn
```

手机浏览器访问：

```text
http://192.168.110.34:18000/health
```

成功返回：

```json
{"ok": true, "model": "yolo11n", "device": "cuda:0"}
```

### 服务器算法服务

已在 Featurize 上跑通：

- PyTorch CUDA
- Ultralytics YOLO
- FastAPI
- `GET /health`
- `POST /analyze`

YOLO 预热后单张图片推理延迟约 `17-47ms`。

### Android App

原仓库：

```text
https://github.com/userrr003/vision-assist-prototype.git
```

关键问题：

- `MainActivity.java` 里服务器地址写死为 `http://127.0.0.1:8000/analyze`
- 在 Android 手机上，`127.0.0.1` 指手机自己，不是 Mac/服务器。
- 临时改成 `http://192.168.110.34:18000/analyze` 后生成了 APK，但安装后闪退。

## 当前阻塞点

### Featurize 端口

Featurize 的 `proxy.featurize.cn` 只开放 JupyterLab，不能直接暴露 `8000` API。

当前临时方案：

```text
手机 -> Mac:18000 -> SSH隧道 -> Featurize:8000
```

正式演示建议：

- 租有公网 IP 的云服务器，或
- 找 Featurize 是否有公开 HTTP 服务功能，或
- 使用稳定公网隧道服务。

### APK 闪退

推测原因：

- 用 Ubuntu apt 里的旧 Android 构建工具临时打包，不是标准 Android Studio/Gradle 构建。
- App 启动时初始化 UVC 外置摄像头库。
- UVC AAR 中包含 Java 8/新字节码特性，旧工具链兼容性较差。

建议下一步：

- 先做 `phone-camera-only` 版本。
- 暂时移除 UVC 依赖和 UVC UI。
- 只保留手机内置摄像头、上传测试、TTS。

## 不要提交的信息

以下内容不要写入公开仓库：

- Featurize SSH 密码
- Featurize API Token
- 私钥文件
- 个人账号 Cookie
- 可长期访问的公网密钥

