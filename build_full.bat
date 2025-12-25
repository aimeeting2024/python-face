@echo off
chcp 65001 >nul
REM 构建完整版人脸特征提取器（包含所有模型文件）
REM 作者: Meeting Server Team
REM 日期: 2025-10-12

echo ========================================
echo 完整版人脸特征提取器构建脚本
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/6] 检查依赖包...
python -c "import face_recognition" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 face_recognition，请运行: pip install face-recognition
    pause
    exit /b 1
)

python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 opencv-python，请运行: pip install opencv-python
    pause
    exit /b 1
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 Pillow，请运行: pip install Pillow
    pause
    exit /b 1
)

python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未安装 PyInstaller，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)

echo [✓] 所有依赖包检查完成
echo.

echo [2/6] 清理旧的构建文件...
if exist "build\face_extractor" (
    rmdir /s /q "build\face_extractor"
    echo [✓] 已清理 build\face_extractor
)
if exist "dist\face_extractor.exe" (
    del /q "dist\face_extractor.exe"
    echo [✓] 已删除旧的 dist\face_extractor.exe
)
echo.

echo [3/6] 开始打包（这可能需要几分钟）...
echo 使用配置文件: face_extractor_full.spec
echo.
pyinstaller --clean face_extractor_full.spec

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo [4/6] 检查输出文件...
if not exist "dist\face_extractor.exe" (
    echo [错误] 未找到输出文件 dist\face_extractor.exe
    pause
    exit /b 1
)

for %%I in (dist\face_extractor.exe) do set "filesize=%%~zI"
set /a "filesize_mb=%filesize% / 1048576"
echo [✓] 输出文件: dist\face_extractor.exe
echo [✓] 文件大小: %filesize_mb% MB
echo.

echo [5/6] 测试打包的程序...
dist\face_extractor.exe --version
if %errorlevel% neq 0 (
    echo [警告] 版本检查失败，但文件已生成
)
echo.

echo [6/6] 复制到目标位置...
REM 复制到meeting-server的test目录
if not exist "..\meeting-server\test" (
    mkdir "..\meeting-server\test"
)
copy /y "dist\face_extractor.exe" "..\meeting-server\test\face_extractor.exe"
if %errorlevel% equ 0 (
    echo [✓] 已复制到 ..\meeting-server\test\face_extractor.exe
)

REM 创建备份
copy /y "dist\face_extractor.exe" "dist\face_extractor_backup_%date:~0,4%%date:~5,2%%date:~8,2%.exe"
echo [✓] 已创建备份
echo.

echo ========================================
echo 构建完成！
echo ========================================
echo.
echo 输出文件位置:
echo   1. dist\face_extractor.exe
echo   2. ..\meeting-server\test\face_extractor.exe
echo.
echo 文件大小: %filesize_mb% MB
echo.
echo 使用方法:
echo   face_extractor.exe extract --input image.jpg --output result.json
echo   face_extractor.exe extract --base64 ^<data^> --output result.json
echo   face_extractor.exe --version
echo.
pause

