# 服务器恢复手册

## 1. 租用或恢复实例

推荐配置：

- GPU：RTX 4090 / A10 / L4
- 显存：16GB 以上，优先 24GB
- 系统：Ubuntu 22.04
- Python：3.10 或 3.11

Featurize 当前已验证 RTX 4090 可用，但自定义端口不直接公网开放。

## 2. 安装依赖

```bash
mkdir -p ~/vision-assist-server
cd ~/vision-assist-server

python -m pip install -U pip
python -m pip install \
  "numpy==1.26.4" \
  "opencv-python-headless==4.9.0.80" \
  ultralytics \
  fastapi \
  "uvicorn[standard]" \
  python-multipart \
  pillow \
  requests
```

注意：如果已有 `torch 2.2.2+cu121`，不要把 NumPy 升到 2.x，否则可能出现：

```text
RuntimeError: Numpy is not available
```

## 3. 启动服务

把 `server/vision_service/app.py` 放到：

```text
~/vision-assist-server/app.py
```

启动：

```bash
cd ~/vision-assist-server
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

检查：

```bash
curl http://127.0.0.1:8000/health
```

应返回：

```json
{"ok": true, "model": "yolo11n", "device": "cuda:0"}
```

## 4. Mac 中转隧道

Featurize 不直接暴露 `8000` 时，在 Mac 终端执行：

```bash
ssh -N -L 0.0.0.0:18000:127.0.0.1:8000 -p <SSH_PORT> featurize@workspace.featurize.cn
```

然后在 Mac 上测试：

```bash
curl http://127.0.0.1:18000/health
```

查 Mac 局域网 IP：

```bash
ifconfig | grep "inet "
```

手机同 Wi-Fi 下访问：

```text
http://<Mac局域网IP>:18000/health
```

App 服务器地址：

```text
http://<Mac局域网IP>:18000/analyze
```

## 5. 常见问题

### Featurize proxy 访问 401

`https://*.proxy.featurize.cn/proxy/8000/health` 返回 401 或跳转，说明该代理只服务 JupyterLab，不适合手机 App。

### 隧道断开

重新执行 SSH 隧道命令即可。Mac 睡眠、网络切换、终端关闭都会导致隧道断开。

