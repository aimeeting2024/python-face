# Ubuntu 服务器编译指南

## 📋 概述

在独立的 Ubuntu 服务器上编译 Linux 版本的人脸识别 HTTP 服务。

---

## 🚀 步骤1：获取源代码到服务器

### 方式1：使用 Git Clone（最快，推荐）⭐

**前提条件**：代码已提交到 Git 仓库（GitHub、GitLab、Gitee 等）

```bash
# 在服务器上执行
cd /opt

# Clone 仓库
git clone https://github.com/aimeeting2024/python-face.git face-service

# 或使用 SSH（如果配置了 SSH 密钥）
git clone git@github.com:aimeeting2024/python-face.git face-service

# 进入项目目录
cd face-service

# 查看文件
ls -la

# 如果使用特定分支或标签
git checkout main
# 或
git checkout v1.0.0
```

**优势**：
- ✅ 最快最简单
- ✅ 自动获取所有文件
- ✅ 可以切换分支/标签
- ✅ 可以随时更新代码

**如果代码在私有仓库**：

```bash
# 方法1：使用 HTTPS（需要输入用户名密码或 Personal Access Token）
git clone https://username:token@github.com/aimeeting2024/python-face.git

# 方法2：使用 SSH 密钥（推荐）
# 先在服务器上配置 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 将公钥添加到 GitHub/GitLab
cat ~/.ssh/id_rsa.pub
# 然后使用 SSH URL clone
git clone git@github.com:aimeeting2024/python-face.git
```

**如果遇到 Git 仓库损坏问题**：

参考 `GIT_CORRUPTION_FIX.md` 修复指南。

---

### 方式2：本地服务器 - 挂载磁盘拷贝

**详细步骤请参考**：`DISK_MOUNT_AND_COPY.md`

**快速步骤**：

```bash
# 1. 查看磁盘和分区
lsblk

# 2. 挂载磁盘（假设是 /dev/sdb1）
sudo mkdir -p /mnt/data
sudo mount /dev/sdb1 /mnt/data

# 3. 创建项目目录
sudo mkdir -p /opt/face-service

# 4. 拷贝文件
sudo cp /mnt/data/python-face/face_service.py /opt/face-service/
sudo cp /mnt/data/python-face/face_extractor.py /opt/face-service/
sudo cp /mnt/data/python-face/requirements.txt /opt/face-service/
sudo cp /mnt/data/python-face/build_http_service.sh /opt/face-service/

# 5. 设置权限
sudo chown -R $USER:$USER /opt/face-service
chmod +x /opt/face-service/build_http_service.sh

# 6. 验证
cd /opt/face-service
ls -la
```

#### 方式2：使用 scp（远程服务器）

```bash
# 在 Windows PowerShell 或 CMD 中
scp -r D:\workspace\python-face user@server:/opt/face-service/

# 或者只上传必需文件
scp face_service.py face_extractor.py requirements.txt build_http_service.sh user@server:/opt/face-service/
```

#### 方式3：使用宝塔面板（推荐）

1. 登录宝塔面板
2. 进入"文件"管理
3. 创建目录：`/opt/face-service`
4. 上传文件：
   - 选择 `python-face` 目录下的文件
   - 或打包为 zip 上传后解压

#### 方式4：使用 Git Clone（最快，推荐）⭐

**详细步骤见上方"方式1：使用 Git Clone"**

**快速命令**：
```bash
cd /opt
git clone https://your-repo-url/python-face.git face-service
cd face-service
```

#### 方式5：使用 FTP/SFTP 工具（推荐，简单）

**详细步骤请参考**：`FTP_TRANSFER.md`

**快速步骤（使用宝塔面板）**：

1. 登录宝塔面板
2. 文件管理 → `/opt` → 新建文件夹 `face-service`
3. 进入 `face-service` → 上传必需文件
4. 设置 `build_http_service.sh` 的执行权限

**或使用 FileZilla**：

1. 打开 FileZilla
2. 连接：`sftp://服务器IP`，端口 `22`
3. 左侧：`D:\workspace\python-face`
4. 右侧：`/opt/face-service`
5. 拖拽文件上传

---

## 🔧 步骤2：安装 Python 开发环境

**详细安装指南请参考**：`PYTHON_DEV_ENV.md`

### 快速安装（一键脚本）

```bash
# 创建安装脚本
cat > install_python_env.sh << 'EOF'
#!/bin/bash
set -e
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential cmake gcc g++ make
sudo apt install -y libopenblas-dev liblapack-dev libjpeg-dev libpng-dev
sudo apt install -y libx11-dev libgtk-3-dev python3-dlib
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'INNER_EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
INNER_EOF
python3 -m pip install --upgrade pip setuptools wheel
echo "✅ Python 开发环境安装完成！"
EOF

chmod +x install_python_env.sh
./install_python_env.sh
```

### 手动安装步骤

### 2.1 安装 Python 和基础工具

```bash
# 更新包列表
sudo apt update
sudo apt upgrade -y

# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 2.2 安装 Python 开发工具和系统依赖

```bash
# 安装 Python 开发头文件（编译扩展模块需要）
sudo apt install -y python3-dev python3-distutils

# 安装编译工具（用于编译 dlib 等 C++ 扩展）
sudo apt install -y \
    build-essential \
    cmake \
    gcc \
    g++ \
    make

# 安装科学计算库依赖（dlib、numpy 等需要）
sudo apt install -y \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libx11-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev
```

### 2.3 配置 pip（使用官方源）

**使用官方 PyPI 源**（推荐，有科学上网时）：
- 不需要配置，直接使用 `pip install` 即可
- 官方源：https://pypi.org/simple

**如果之前配置了国内镜像，需要删除**：

```bash
# 删除 pip 配置文件
rm -f ~/.pip/pip.conf
rm -rf ~/.pip

# 验证（应该没有配置）
pip3 config list
```

**如果需要使用国内镜像**（无科学上网时）：

```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

### 2.4 升级 pip 和基础工具

```bash
# 升级 pip 到最新版本
python3 -m pip install --upgrade pip

# 安装常用开发工具
pip3 install --upgrade setuptools wheel
```

### 2.5 创建虚拟环境（推荐，隔离项目依赖）

```bash
# 进入项目目录
cd /opt/face-service

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证（提示符前会显示 (venv)）
which python3
# 应该显示：/opt/face-service/venv/bin/python3
```

### 2.6 安装 Python 依赖

```bash
# 确保虚拟环境已激活（提示符前有 (venv)）
# 如果没有，执行：source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装项目依赖（使用官方 PyPI）
pip install -r requirements.txt

# 如果 face-recognition 安装失败，可能需要先安装 dlib
# 方法1：使用系统包管理器（推荐）
sudo apt install -y python3-dlib

# 然后重新安装
pip install face-recognition flask flask-cors

# 方法2：使用预编译的 wheel 包
# 下载对应版本的 wheel 包后安装
pip install dlib-*.whl
pip install face-recognition flask flask-cors

# 安装 PyInstaller（用于编译）
pip install pyinstaller
```

**注意**：
- 使用虚拟环境可以隔离项目依赖，避免冲突
- 编译时也需要在虚拟环境中进行
- 如果不想用虚拟环境，可以全局安装（不推荐）

### 2.7 验证开发环境

```bash
# 检查 Python 版本（应该是 3.8+）
python3 --version

# 检查已安装的包
pip list

# 测试导入关键库
python3 -c "import face_recognition; print('face_recognition OK')"
python3 -c "import flask; print('flask OK')"
python3 -c "import cv2; print('opencv OK')"
python3 -c "import dlib; print('dlib OK')"
```

如果所有测试通过，Python 开发环境就准备好了！

---

## 🏗️ 步骤3：编译

### 3.1 设置执行权限

```bash
cd /opt/face-service
chmod +x build_http_service.sh
```

### 3.2 执行编译

```bash
./build_http_service.sh
```

**或者手动编译**：

```bash
# 查找模型文件路径
MODEL_PATH=$(python3 -c "import face_recognition_models, os; print(os.path.dirname(face_recognition_models.__file__))" 2>/dev/null)

# 编译（包含模型文件）
if [ -n "$MODEL_PATH" ] && [ -d "$MODEL_PATH" ]; then
    pyinstaller --onefile \
        --name face_http_service \
        --add-data "face_extractor.py:." \
        --add-data "$MODEL_PATH:face_recognition_models" \
        --hidden-import face_recognition \
        --hidden-import face_recognition_models \
        --hidden-import flask \
        --hidden-import flask_cors \
        --hidden-import cv2 \
        --hidden-import PIL \
        --hidden-import numpy \
        --hidden-import dlib \
        --clean \
        --noconfirm \
        face_service.py
else
    pyinstaller --onefile \
        --name face_http_service \
        --add-data "face_extractor.py:." \
        --hidden-import face_recognition \
        --hidden-import face_recognition_models \
        --hidden-import flask \
        --hidden-import flask_cors \
        --hidden-import cv2 \
        --hidden-import PIL \
        --hidden-import numpy \
        --hidden-import dlib \
        --clean \
        --noconfirm \
        face_service.py
fi

# 复制到部署目录
mkdir -p deploy
cp -f dist/face_http_service deploy/
chmod +x deploy/face_http_service
```

### 3.3 验证编译结果

```bash
# 检查文件是否存在
ls -lh deploy/face_http_service

# 检查文件类型（应该是 Linux 可执行文件）
file deploy/face_http_service

# 应该显示：ELF 64-bit LSB executable, x86-64
```

---

## 🚀 步骤4：运行服务

### 方式1：直接运行（测试）

```bash
cd /opt/face-service
./deploy/face_http_service
```

### 方式2：后台运行

```bash
cd /opt/face-service
nohup ./deploy/face_http_service > logs/face_service.log 2>&1 &
```

### 方式3：使用 systemd 管理（推荐）

创建服务文件 `/etc/systemd/system/face-service.service`：

```ini
[Unit]
Description=Face Recognition HTTP Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/face-service
ExecStart=/opt/face-service/deploy/face_http_service
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

## ✅ 步骤5：验证

### 健康检查

```bash
curl http://localhost:8081/health
```

**预期响应**：
```json
{
  "status": "healthy",
  "service": "face-recognition-service",
  "version": "1.0.0"
}
```

---

## 📦 完整文件清单

### 必需文件（最小集）

```
/opt/face-service/
├── face_service.py          # HTTP 服务主文件
├── face_extractor.py        # 特征提取库
├── requirements.txt         # Python 依赖
├── build_http_service.sh    # 编译脚本
└── deploy/                  # 编译输出目录
    └── face_http_service    # 编译后的可执行文件
```

### 推荐上传的文件

```
/opt/face-service/
├── face_service.py
├── face_extractor.py
├── requirements.txt
├── build_http_service.sh
├── config.json              # 配置文件（可选）
└── README.md                # 说明文档（可选）
```

---

## 🔍 故障排查

### Q: 编译失败，找不到 face_recognition？

```bash
# 检查是否已安装
pip3 list | grep face-recognition

# 如果未安装，先安装 dlib
sudo apt install -y python3-dlib
pip3 install face-recognition
```

### Q: 编译后的文件无法运行？

```bash
# 检查文件权限
chmod +x deploy/face_http_service

# 检查依赖
ldd deploy/face_http_service

# 检查系统库
sudo apt install -y libc6 libstdc++6
```

### Q: 服务启动失败？

```bash
# 查看日志
tail -f logs/face_service.log

# 或使用 systemd
sudo journalctl -u face-service -f
```

---

## 📝 快速命令参考

```bash
# 1. 上传文件（在 Windows 中）
scp -r D:\workspace\python-face\* user@server:/opt/face-service/

# 2. SSH 登录服务器
ssh user@server

# 3. 进入项目目录
cd /opt/face-service

# 4. 安装依赖
sudo apt update
sudo apt install -y python3 python3-pip python3-dlib
pip3 install -r requirements.txt
pip3 install pyinstaller

# 5. 编译
chmod +x build_http_service.sh
./build_http_service.sh

# 6. 运行
./deploy/face_http_service
```

---

## ✅ 总结

1. ✅ **上传源代码**到服务器 `/opt/face-service/`
2. ✅ **安装依赖**（Python、系统库、Python 包）
3. ✅ **执行编译**脚本
4. ✅ **运行服务**或配置 systemd
5. ✅ **验证**健康检查接口

完成！

