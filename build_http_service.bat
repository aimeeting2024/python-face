@echo off
chcp 65001 >nul
REM ========================================
REM 构建人脸识别HTTP服务为独立exe文件
REM ========================================

echo.
echo ========================================
echo 人脸识别HTTP服务打包工具
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/5] 检查依赖...
python -c "import face_recognition, flask, flask_cors" 2>nul
if %errorlevel% neq 0 (
    echo [错误] 缺少必要的依赖，正在安装...
    pip install face-recognition flask flask-cors
)

echo [2/5] 检查PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

echo [3/4] 查找模型文件路径...
for /f "delims=" %%i in ('python -c "import face_recognition_models, os; print(os.path.dirname(face_recognition_models.__file__))"') do set MODEL_PATH=%%i
echo 模型路径: %MODEL_PATH%

echo [4/5] 开始打包HTTP服务（包含模型文件）...
echo 这可能需要几分钟，请耐心等待...
echo 提示: 模型文件约100MB，打包后约160-180MB
pyinstaller --onefile ^
    --name face_http_service ^
    --add-data "face_extractor.py;." ^
    --add-data "%MODEL_PATH%;face_recognition_models" ^
    --hidden-import face_recognition ^
    --hidden-import face_recognition_models ^
    --hidden-import flask ^
    --hidden-import flask_cors ^
    --hidden-import cv2 ^
    --hidden-import PIL ^
    --hidden-import numpy ^
    --hidden-import dlib ^
    --clean ^
    --noconfirm ^
    face_service.py

if %errorlevel% neq 0 (
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo [5/5] 复制文件到部署目录...
if not exist "deploy" mkdir deploy
copy /Y dist\face_http_service.exe deploy\
echo.

echo ========================================
echo ✅ 打包成功！
echo ========================================
echo.
echo 生成的文件:
echo   - deploy\face_http_service.exe (HTTP服务，约160-180MB)
echo   - 已包含dlib模型文件（~100MB）
echo.
echo 下一步:
echo   1. 将 deploy\face_http_service.exe 复制到服务器
echo   2. 运行 install_service.bat 安装为Windows服务
echo   3. 启动Go后端服务（会自动连接HTTP服务）
echo.
echo 性能提升: 9秒 → 200-500ms (提升95%%)
echo ========================================
echo.
pause

