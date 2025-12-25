#!/usr/bin/env python3
"""
跨平台编译脚本 - 人脸特征提取器
支持自动检测操作系统并执行相应的编译流程
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(command, shell=True):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python():
    """检查Python环境"""
    print("🔍 检查Python环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Python版本过低: {python_version.major}.{python_version.minor}")
        print("   需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    return True

def setup_virtual_env():
    """设置虚拟环境"""
    system = platform.system().lower()
    venv_name = f"venv_{system}"
    
    print(f"🏗️  设置虚拟环境: {venv_name}")
    
    # 删除已存在的虚拟环境
    if os.path.exists(venv_name):
        print(f"   删除已存在的虚拟环境...")
        shutil.rmtree(venv_name)
    
    # 创建虚拟环境
    success, _, error = run_command([sys.executable, "-m", "venv", venv_name], shell=False)
    if not success:
        print(f"❌ 创建虚拟环境失败: {error}")
        return False, None
    
    # 确定激活脚本路径
    if system == "windows":
        activate_script = os.path.join(venv_name, "Scripts", "activate.bat")
        python_exe = os.path.join(venv_name, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_name, "Scripts", "pip.exe")
    else:
        activate_script = os.path.join(venv_name, "bin", "activate")
        python_exe = os.path.join(venv_name, "bin", "python")
        pip_exe = os.path.join(venv_name, "bin", "pip")
    
    return True, {"python": python_exe, "pip": pip_exe, "activate": activate_script}

def install_dependencies(pip_exe):
    """安装依赖"""
    print("📦 安装依赖包...")
    
    # 升级pip
    print("   升级pip...")
    success, _, error = run_command([pip_exe, "install", "--upgrade", "pip"], shell=False)
    if not success:
        print(f"⚠️  升级pip失败: {error}")
    
    # 安装requirements.txt
    if os.path.exists("requirements.txt"):
        print("   安装Python依赖...")
        success, _, error = run_command([pip_exe, "install", "-r", "requirements.txt"], shell=False)
        if not success:
            print(f"❌ 安装依赖失败: {error}")
            return False
    
    # 安装PyInstaller
    print("   安装PyInstaller...")
    success, _, error = run_command([pip_exe, "install", "pyinstaller"], shell=False)
    if not success:
        print(f"❌ 安装PyInstaller失败: {error}")
        return False
    
    return True

def compile_binary(venv_info):
    """编译二进制文件"""
    system = platform.system().lower()
    print(f"🔨 开始编译 ({system} 平台)...")
    
    # 清理旧文件
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            print(f"   清理 {dir_name}...")
            shutil.rmtree(dir_name)
    
    # 执行PyInstaller
    pyinstaller_exe = os.path.join(os.path.dirname(venv_info["pip"]), "pyinstaller")
    if system == "windows":
        pyinstaller_exe += ".exe"
    
    print("   执行PyInstaller编译...")
    success, stdout, error = run_command([
        pyinstaller_exe, 
        "face_extractor.spec"
    ], shell=False)
    
    if not success:
        print(f"❌ 编译失败: {error}")
        return False
    
    # 检查输出文件
    if system == "windows":
        output_file = "dist/face-extractor.exe"
    else:
        output_file = "dist/face-extractor"
    
    if not os.path.exists(output_file):
        print(f"❌ 编译输出文件不存在: {output_file}")
        return False
    
    print(f"✅ 编译成功: {output_file}")
    
    # 创建发布目录
    release_dir = f"release/{system}"\n    os.makedirs(release_dir, exist_ok=True)
    
    # 复制文件
    target_file = os.path.join(release_dir, os.path.basename(output_file))
    shutil.copy2(output_file, target_file)
    
    # 设置执行权限 (Unix系统)
    if system != "windows":
        os.chmod(target_file, 0o755)
    
    print(f"📁 发布文件: {target_file}")
    
    return True, output_file, target_file

def test_binary(binary_path):
    """测试二进制文件"""
    print("🧪 测试可执行文件...")
    
    # 测试版本信息
    success, stdout, error = run_command([binary_path, "--version"], shell=False)
    if success:
        print(f"   版本信息: {stdout.strip()}")
    else:
        print(f"⚠️  版本测试失败: {error}")
    
    # 测试系统信息
    success, stdout, error = run_command([binary_path, "--info"], shell=False)
    if success:
        print("   系统信息测试通过")
    else:
        print(f"⚠️  系统信息测试失败: {error}")
    
    # 显示文件大小
    file_size = os.path.getsize(binary_path)
    size_mb = file_size / (1024 * 1024)
    print(f"   文件大小: {size_mb:.2f} MB")

def main():
    """主函数"""
    print("🚀 人脸特征提取器 - 跨平台编译工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("face_extractor.py"):
        print("❌ 未找到face_extractor.py文件")
        print("   请在face-extractor目录下运行此脚本")
        return 1
    
    # 检查Python环境
    if not check_python():
        return 1
    
    # 设置虚拟环境
    success, venv_info = setup_virtual_env()
    if not success:
        return 1
    
    # 安装依赖
    if not install_dependencies(venv_info["pip"]):
        return 1
    
    # 编译二进制文件
    success, output_file, release_file = compile_binary(venv_info)
    if not success:
        return 1
    
    # 测试二进制文件
    test_binary(output_file)
    
    # 清理编译临时文件
    print("🧹 清理临时文件...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    print("\n🎉 编译完成!")
    print(f"📦 可执行文件: {output_file}")
    print(f"📋 发布版本: {release_file}")
    print("\n使用方法:")
    print(f"  {os.path.basename(output_file)} --version")
    print(f"  {os.path.basename(output_file)} extract --base64 <data> --output result.json")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ 编译被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 编译过程中发生错误: {e}")
        sys.exit(1)