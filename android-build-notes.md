# Android 调试记录

## 原始 App 仓库

```text
https://github.com/userrr003/vision-assist-prototype.git
```

## 关键问题

### 服务器地址写死

原代码：

```java
private static final String SERVER_URL = "http://127.0.0.1:8000/analyze";
```

真机上不可用，因为 `127.0.0.1` 指手机自己。

临时应改为：

```java
private static final String SERVER_URL = "http://<Mac局域网IP>:18000/analyze";
```

当时 Mac IP：

```text
192.168.110.34
```

所以临时地址：

```text
http://192.168.110.34:18000/analyze
```

## 服务端协议问题

原 App 上传逻辑发送原始 JPEG body：

```java
connection.setRequestProperty("Content-Type", "image/jpeg");
outputStream.write(jpegBytes);
```

因此服务端 `/analyze` 必须兼容：

- `multipart/form-data`
- `image/jpeg` raw body

`server/vision_service/app.py` 已按这个方向设计。

## 返回字段问题

原 App 只解析：

```json
{"message": "..."}
```

服务端当前返回：

```json
{"speak": "..."}
```

建议服务端同时返回：

```json
{
  "message": "正前方有公交车，请注意",
  "speak": "正前方有公交车，请注意"
}
```

这样不用立刻改 App 解析逻辑。

## APK 闪退

临时 APK 安装后闪退，推测原因：

- 使用旧 Android 构建工具 `aapt + dx` 临时打包。
- UVC AAR 包含较新字节码特性，旧工具链兼容性差。
- App 启动时初始化 UVC 组件，导致启动阶段崩溃。

## 建议下一版

先做 `phone-camera-only` 测试版：

- 删除 UVC 相关 import、字段、监听、按钮、初始化逻辑。
- 只保留手机内置摄像头预览。
- 保留“上传测试”。
- 保留 TTS 播报。
- 服务器地址支持手动输入或配置文件。

这样可以优先验证核心链路：

```text
手机摄像头 -> 服务器识别 -> 手机播报
```

之后再恢复 UVC。

