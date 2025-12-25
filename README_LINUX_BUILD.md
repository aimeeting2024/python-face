# Linux 版本编译指南

## 📋 概述

由于开发环境在 Windows，但需要编译 Linux 版本，有以下几种方式：

---

## 🚀 方式1：使用 WSL（推荐，最简单）

### 前提条件

- Windows 10/11 系统
- 已安装 WSL（Windows Subsystem for Linux）

### 步骤

1. **打开 WSL 终端**
   ```powershell
   wsl
   ```

2. **进入项目目录**
   ```bash
   cd /mnt/d/workspace/python-face
   ```

3. **运行编译脚本**
   ```bash
   chmod +x build_http_service.sh
   ./build_http_service.sh
   ```

4. **编译完成后，文件在**
   ```bash
   deploy/face_http_service
   ```

5. **复制到 Windows（可选）**
   ```bash
   cp deploy/face_http_service /mnt/d/workspace/python-face/deploy/
   ```

### 或者使用批处理脚本（自动）

在 Windows PowerShell 或 CMD 中运行：
```powershell
.\build_http_service_linux.bat
```

脚本会自动检测 WSL 并执行编译。

---

## 🐳 方式2：使用 Docker

### 前提条件

- 已安装 Docker Desktop

### 步骤

1. **运行批处理脚本**
   ```powershell
   .\build_http_service_linux.bat
   ```

   脚本会自动：
   - 创建临时 Dockerfile
   - 构建包含编译环境的镜像
   - 在容器中执行编译
   - 将结果复制到 `deploy/` 目录

2. **编译完成后，文件在**
   ```
   deploy\face_http_service
   ```

---

## 🖥️ 方式3：直接在 Linux 服务器上编译（推荐用于生产环境）

### 步骤

1. **上传源代码到 Linux 服务器**

   **方式A：使用 scp（命令行）**
   ```bash
   # 在 Windows PowerShell 中
   scp -r D:\workspace\python-face\* user@server:/opt/face-service/
   ```

   **方式B：使用宝塔面板（推荐）**
   - 登录宝塔面板
   - 进入"文件"管理
   - 创建目录 `/opt/face-service`
   - 上传必需文件：
     - `face_service.py`
     - `face_extractor.py`
     - `requirements.txt`
     - `build_http_service.sh`

   **方式C：打包上传**
   ```bash
   # 在 Windows 中打包
   cd D:\workspace
   tar -czf python-face.tar.gz python-face/
   
   # 上传
   scp python-face.tar.gz user@server:/opt/
   
   # 在服务器上解压
   cd /opt
   tar -xzf python-face.tar.gz
   mv python-face face-service
   ```

2. **SSH 登录服务器**
   ```bash
   ssh user@server
   ```

3. **进入项目目录**
   ```bash
   cd /opt/face-service
   ```

4. **安装依赖**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y python3 python3-pip python3-dlib
   sudo apt install -y build-essential cmake libopenblas-dev
   
   # 安装 Python 依赖（使用官方 PyPI）
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```

5. **运行编译脚本**
   ```bash
   chmod +x build_http_service.sh
   ./build_http_service.sh
   ```

6. **编译完成后，文件在**
   ```bash
   deploy/face_http_service
   ```

**详细步骤请参考**：`UBUNTU_SERVER_BUILD.md`

---

## 🔧 方式4：使用 GitHub Actions（CI/CD）

### 创建 `.github/workflows/build-linux.yml`

```yaml
name: Build Linux Face Service

on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-dlib
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build
        run: |
          chmod +x build_http_service.sh
          ./build_http_service.sh
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: face_http_service_linux
          path: deploy/face_http_service
```

---

## 📝 编译后的使用

### 1. 上传到 Linux 服务器

```bash
# 使用 scp
scp deploy/face_http_service user@server:/opt/face-service/

# 或使用宝塔面板文件管理上传
```

### 2. 设置执行权限

```bash
chmod +x /opt/face-service/face_http_service
```

### 3. 运行服务

```bash
# 直接运行（前台）
./face_http_service

# 后台运行
nohup ./face_http_service > logs/face_service.log 2>&1 &

# 或使用 systemd 管理（推荐）
```

### 4. 配置 systemd 服务（推荐）

创建 `/etc/systemd/system/face-service.service`：

```ini
[Unit]
Description=Face Recognition HTTP Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/face-service
ExecStart=/opt/face-service/face_http_service
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable face-service
sudo systemctl start face-service
sudo systemctl status face-service
```

---

## ✅ 验证

### 健康检查

```bash
curl http://localhost:8081/health
```

**预期响应：**
```json
{
  "status": "healthy",
  "service": "face-recognition-service",
  "version": "1.0.0"
}
```

---

## 🐛 常见问题

### Q: WSL 中找不到 Python？

```bash
# 在 WSL 中安装 Python
sudo apt update
sudo apt install -y python3 python3-pip
```

### Q: Docker 编译失败？

检查 Docker Desktop 是否运行，或尝试：
```bash
docker pull python:3.9-slim
```

### Q: 编译后的文件很大（160-180MB）？

这是正常的，因为包含了：
- Python 运行时
- face_recognition 库
- dlib 模型文件（~100MB）
- 所有依赖

### Q: 在 Linux 服务器上运行失败？

检查：
1. 文件权限：`chmod +x face_http_service`
2. 系统库依赖：`ldd face_http_service`（查看依赖）
3. 日志：查看服务输出日志

---

## 📚 相关文档

- `README_HTTP_SERVICE.md` - HTTP 服务使用说明
- `DEPLOYMENT_GUIDE.md` - 完整部署指南

---

**推荐方式**：使用 WSL 或直接在 Linux 服务器上编译（最简单可靠）

