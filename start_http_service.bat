@echo off
REM ========================================
REM 启动人脸识别HTTP服务（开发/测试模式）
REM ========================================

echo.
echo ========================================
echo 启动人脸识别HTTP服务
echo ========================================
echo.

REM 检查是否已打包
if exist "deploy\face_http_service.exe" (
    echo [模式] 使用打包的exe文件
    echo [地址] http://localhost:8081
    echo [日志] logs\face_service.log
    echo.
    echo 服务启动中...
    echo.
    
    REM 创建日志目录
    if not exist "logs" mkdir logs
    
    REM 启动服务
    cd deploy
    start "人脸识别HTTP服务" face_http_service.exe
    cd ..
    
    echo ✅ 服务已启动！
    echo.
    echo 测试服务是否正常:
    echo   curl http://localhost:8081/health
    echo.
    echo 查看日志:
    echo   type logs\face_service.log
    echo.
    
) else (
    echo [模式] 使用Python脚本（开发模式）
    echo.
    echo 检查Python环境...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 未检测到Python环境
        echo 请先安装Python或运行 build_http_service.bat 生成exe
        pause
        exit /b 1
    )
    
    echo 启动服务...
    python face_service.py
)

pause

