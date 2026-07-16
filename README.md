# Vision Assist Handoff

AI 视觉语音助盲项目交接仓库。这个仓库用于在新设备上恢复项目上下文、服务器算法服务、Android 调试状态和下一步工作计划。

> 不包含任何 Featurize 密码、SSH 密码、API Token 或私钥。

## 当前状态

- 手机浏览器已能访问算法服务健康检查：
  - 临时地址：`http://192.168.110.34:18000/health`
  - 返回：`{"ok":true,"model":"yolo11n","device":"cuda:0"}`
- Featurize RTX 4090 服务器已跑通 YOLO + FastAPI。
- FastAPI 服务内部监听：`0.0.0.0:8000`
- 因 Featurize 不公开自定义端口，目前通过 Mac SSH 隧道中转：
  - Mac `18000` -> Featurize `127.0.0.1:8000`
- Android App 原仓库默认写死 `127.0.0.1:8000/analyze`，在真机上不可用。
- 临时 APK 已生成过，但安装后闪退。建议下一步先做 `phone-camera-only` 测试版，暂时移除 UVC 外置摄像头依赖。

## 推荐下一步

1. 恢复 Featurize 镜像或重新租 RTX 4090 实例。
2. 部署 `server/vision_service/app.py`。
3. 在 Mac 上重建 SSH 隧道。
4. 做一个不含 UVC 的手机摄像头测试版 APK。
5. 手机摄像头上传图片到 `/analyze`，验证识别和 TTS 播报。
6. 稳定后再恢复 UVC 外置摄像头逻辑。

详细说明见：

- [项目交接](docs/project-handoff-2026-07-16.md)
- [服务器恢复手册](docs/server-runbook.md)
- [Android 调试记录](docs/android-build-notes.md)
- [下一步路线](docs/next-steps.md)

