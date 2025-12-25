@echo off
chcp 65001 >nul
REM ========================================
REM 在Windows环境下编译Linux版本的人脸识别HTTP服务
REM 使用WSL或Docker进行交叉编译
REM ========================================

echo.
echo ========================================
echo 人脸识别HTTP服务 - Linux版本编译工具
echo ========================================
echo.

REM 检查WSL是否可用
wsl --list >nul 2>&1
if %errorlevel% equ 0 (
    echo [检测] 发现WSL环境
    echo.
    echo [选项] 请选择编译方式:
    echo   1. 使用 Docker 编译（推荐，在WSL中已安装Docker时使用）
    echo   2. 直接在WSL中编译（需要WSL中安装Python和依赖）
    echo.
    set /p choice="请输入选项 (1 或 2，默认1): "
    if "!choice!"=="" set choice=1
    if "!choice!"=="1" (
        echo [选择] 使用 Docker 编译...
        wsl bash -c "cd /mnt/d/workspace/python-face && chmod +x build_http_service_docker.sh && ./build_http_service_docker.sh"
    ) else (
        echo [选择] 直接在WSL中编译...
        wsl bash -c "cd /mnt/d/workspace/python-face && chmod +x build_http_service.sh && ./build_http_service.sh"
    )
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo ✅ Linux版本编译成功！
        echo ========================================
        echo.
        echo 生成的文件位置:
        echo   WSL路径: ~/workspace/python-face/deploy/face_http_service
        echo   或: /mnt/d/workspace/python-face/deploy/face_http_service
        echo.
        echo 下一步:
        echo   1. 从WSL复制到Windows: wsl cp /mnt/d/workspace/python-face/deploy/face_http_service ./
        echo   2. 或直接在WSL中测试: wsl ./deploy/face_http_service
        echo   3. 上传到Linux服务器使用
        echo.
    ) else (
        echo.
        echo [错误] WSL编译失败，请检查WSL环境
        echo.
    )
    pause
    exit /b %errorlevel%
)

REM 检查Docker是否可用
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [检测] 发现Docker环境，使用Docker编译...
    echo.
    echo [提示] 正在创建临时Docker容器进行编译...
    echo.
    
    REM 创建临时Dockerfile
    (
        echo FROM python:3.9-slim
        echo WORKDIR /app
        echo COPY requirements.txt .
        echo RUN pip install --no-cache-dir -r requirements.txt
        echo RUN pip install --no-cache-dir pyinstaller
        echo COPY . .
        echo RUN chmod +x build_http_service.sh
        echo RUN ./build_http_service.sh
    ) > Dockerfile.build
    
    echo [1/3] 构建Docker镜像...
    docker build -f Dockerfile.build -t face-service-builder .
    
    if %errorlevel% neq 0 (
        echo [错误] Docker镜像构建失败
        del Dockerfile.build
        pause
        exit /b 1
    )
    
    echo [2/3] 在Docker容器中编译...
    docker run --rm -v "%CD%\deploy:/app/deploy" face-service-builder
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo ✅ Linux版本编译成功！
        echo ========================================
        echo.
        echo 生成的文件位置:
        echo   deploy\face_http_service
        echo.
        echo 下一步:
        echo   1. 将 deploy\face_http_service 上传到Linux服务器
        echo   2. 在服务器上设置执行权限: chmod +x face_http_service
        echo   3. 运行服务: ./face_http_service
        echo.
    ) else (
        echo [错误] Docker编译失败
    )
    
    REM 清理临时文件
    del Dockerfile.build
    pause
    exit /b %errorlevel%
)

REM 如果都没有，提供手动指导
echo [警告] 未检测到WSL或Docker环境
echo.
echo ========================================
echo 编译Linux版本的几种方式:
echo ========================================
echo.
echo 方式1: 使用WSL (推荐)
echo   1. 安装WSL: wsl --install
echo   2. 在WSL中运行: wsl bash build_http_service.sh
echo.
echo 方式2: 使用Docker
echo   1. 安装Docker Desktop
echo   2. 运行此脚本，会自动使用Docker编译
echo.
echo 方式3: 直接在Linux服务器上编译
echo   1. 将整个python-face目录上传到Linux服务器
echo   2. 在Linux服务器上运行: bash build_http_service.sh
echo.
echo 方式4: 使用GitHub Actions或其他CI/CD
echo   在Linux环境中自动编译
echo.
echo ========================================
echo.
pause

