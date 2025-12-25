#!/bin/bash
# 人脸特征提取器 - Linux/macOS跨平台编译脚本
# 使用PyInstaller编译为独立可执行文件

set -e  # 遇到错误就退出

echo "======================================"
echo "人脸特征提取器 - $(uname)平台编译"
echo "======================================"
echo

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "错误: 未找到pip"
    exit 1
fi

# 使用pip3或pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "1. 创建虚拟环境..."
if [ -d "venv_linux" ]; then
    echo "发现已存在的虚拟环境，正在删除..."
    rm -rf venv_linux
fi
python3 -m venv venv_linux
source venv_linux/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 安装PyInstaller
echo "安装PyInstaller..."
pip install pyinstaller

# 编译为独立可执行文件
echo "编译中..."
pyinstaller --onefile --name face-extractor face_extractor.py

# 检查编译结果
if [ -f "dist/face-extractor" ]; then
    echo "编译成功!"
    echo "可执行文件位置: dist/face-extractor"
    
    # 复制到项目根目录
    cp dist/face-extractor ./face-extractor
    echo "已复制到当前目录: face-extractor"
    
    # 测试
    echo "测试可执行文件..."
    ./face-extractor --version
    
    echo "编译完成!"
else
    echo "编译失败!"
    exit 1
fi