# Ubuntu 服务器 Python 开发环境安装指南

## 📋 完整安装步骤

### 步骤1：安装 Python 和基础工具

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装 Python 3、pip 和虚拟环境工具
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 验证安装
python3 --version  # 应该显示 Python 3.8+
pip3 --version     # 应该显示 pip 版本
```

### 步骤2：安装编译工具和系统依赖

```bash
# 安装编译工具（编译 C++ 扩展需要）
sudo apt install -y \
    build-essential \
    cmake \
    gcc \
    g++ \
    make \
    pkg-config

# 安装科学计算库依赖（numpy、dlib 等需要）
sudo apt install -y \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev

# 安装 OpenCV 依赖
sudo apt install -y \
    libx11-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev

# 安装 dlib 系统依赖（如果使用系统包）
sudo apt install -y python3-dlib
```

### 步骤3：配置 pip（使用官方源）

**使用官方 PyPI 源**（推荐，有科学上网时）：
- 不需要配置，直接使用 `pip install` 即可
- 官方源：https://pypi.org/simple

**如果之前配置了国内镜像，需要删除**：

```bash
# 删除 pip 配置文件
rm -f ~/.pip/pip.conf

# 或者删除整个配置目录
rm -rf ~/.pip

# 验证（应该没有配置）
pip3 config list
```

**如果需要使用国内镜像**（无科学上网时）：

```bash
# 创建 pip 配置目录
mkdir -p ~/.pip

# 创建配置文件
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

### 步骤4：升级 pip 和基础工具

```bash
# 升级 pip 到最新版本
python3 -m pip install --upgrade pip

# 可能会看到警告信息，这是正常的：
# "Not uninstalling pip at /usr/lib/python3/dist-packages, outside environment /usr"
# "Can't uninstall 'pip'. No files were found to uninstall."
# 这些警告不影响升级，最终会显示 "Successfully installed pip-X.X.X"

# 验证 pip 版本
pip3 --version

# 安装常用开发工具
pip3 install --upgrade setuptools wheel
```

### 步骤5：创建项目虚拟环境（推荐）

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

### 步骤6：在虚拟环境中安装项目依赖

```bash
# 确保虚拟环境已激活（提示符前有 (venv)）
# 如果没有，执行：source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装 PyInstaller（用于编译）
pip install pyinstaller
```

### 步骤7：验证安装

```bash
# 检查 Python 版本
python3 --version

# 检查已安装的包
pip list

# 测试导入关键库
python3 -c "import face_recognition; print('✅ face_recognition OK')"
python3 -c "import flask; print('✅ flask OK')"
python3 -c "import cv2; print('✅ opencv OK')"
python3 -c "import dlib; print('✅ dlib OK')"
python3 -c "import numpy; print('✅ numpy OK')"
python3 -c "import PIL; print('✅ Pillow OK')"
```

---

## 🔄 虚拟环境使用

### 激活虚拟环境

```bash
cd /opt/face-service
source venv/bin/activate
```

### 退出虚拟环境

```bash
deactivate
```

### 在虚拟环境中编译

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 执行编译
./build_http_service.sh
```

---

## 📦 一键安装脚本

创建 `install_python_env.sh`：

```bash
#!/bin/bash
set -e

echo "开始安装 Python 开发环境..."

# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装 Python 和基础工具
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 安装编译工具
sudo apt install -y build-essential cmake gcc g++ make pkg-config

# 安装系统依赖
sudo apt install -y \
    libopenblas-dev liblapack-dev libatlas-base-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libx11-dev libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev \
    python3-dlib

# 配置 pip（使用官方源，不需要配置）
# 如果之前配置了国内镜像，需要删除：
# rm -f ~/.pip/pip.conf

# 升级 pip
python3 -m pip install --upgrade pip setuptools wheel

echo "✅ Python 开发环境安装完成！"
echo ""
echo "下一步："
echo "  1. cd /opt/face-service"
echo "  2. python3 -m venv venv"
echo "  3. source venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. pip install pyinstaller"
```

使用：

```bash
chmod +x install_python_env.sh
./install_python_env.sh
```

---

## ⚠️ 常见问题

### Q: pip install 很慢？

**A**: 如果有科学上网，使用官方源即可。如果没有，可以临时指定镜像：

```bash
# 临时使用国内镜像（仅本次安装）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或配置镜像（永久）
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

### Q: dlib 安装失败？

**A**: 使用系统包管理器安装：

```bash
sudo apt install -y python3-dlib
```

### Q: 编译时找不到 Python 头文件？

**A**: 安装 python3-dev：

```bash
sudo apt install -y python3-dev
```

### Q: 虚拟环境激活后提示符没变化？

**A**: 检查是否正确激活：

```bash
which python3
# 应该显示项目目录下的 venv/bin/python3
```

---

## ✅ 验证清单

- [ ] Python 3.8+ 已安装
- [ ] pip 已安装并升级到最新
- [ ] 编译工具（gcc、cmake）已安装
- [ ] 系统依赖库已安装
- [ ] pip 镜像已配置
- [ ] 虚拟环境已创建
- [ ] 项目依赖已安装
- [ ] 所有库可以正常导入

完成以上步骤后，Python 开发环境就准备好了！

