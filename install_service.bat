@echo off
REM ========================================
REM 安装人脸识别HTTP服务为Windows服务
REM 需要管理员权限运行
REM ========================================

echo.
echo ========================================
echo 安装人脸识别HTTP服务（Windows服务）
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 需要管理员权限！
    echo 请右键此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

REM 检查NSSM
set NSSM_PATH=%~dp0nssm.exe
if not exist "%NSSM_PATH%" (
    echo [错误] 未找到nssm.exe
    echo.
    echo 请下载NSSM（Non-Sucking Service Manager）:
    echo   https://nssm.cc/download
    echo.
    echo 下载后将nssm.exe放到此目录：
    echo   %~dp0
    echo.
    pause
    exit /b 1
)

REM 检查服务程序
set SERVICE_EXE=%~dp0deploy\face_http_service.exe
if not exist "%SERVICE_EXE%" (
    echo [错误] 未找到face_http_service.exe
    echo 请先运行 build_http_service.bat 生成exe文件
    pause
    exit /b 1
)

echo [1/4] 停止已存在的服务...
"%NSSM_PATH%" stop FaceRecognitionHTTP >nul 2>&1
"%NSSM_PATH%" remove FaceRecognitionHTTP confirm >nul 2>&1

echo [2/4] 安装Windows服务...
"%NSSM_PATH%" install FaceRecognitionHTTP "%SERVICE_EXE%"

echo [3/4] 配置服务参数...
REM 设置工作目录
"%NSSM_PATH%" set FaceRecognitionHTTP AppDirectory "%~dp0deploy"

REM 设置日志
"%NSSM_PATH%" set FaceRecognitionHTTP AppStdout "%~dp0logs\service_stdout.log"
"%NSSM_PATH%" set FaceRecognitionHTTP AppStderr "%~dp0logs\service_stderr.log"

REM 设置自动启动
"%NSSM_PATH%" set FaceRecognitionHTTP Start SERVICE_AUTO_START

REM 设置失败重启
"%NSSM_PATH%" set FaceRecognitionHTTP AppRestartDelay 5000

echo [4/4] 启动服务...
"%NSSM_PATH%" start FaceRecognitionHTTP

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 服务安装成功！
    echo ========================================
    echo.
    echo 服务名称: FaceRecognitionHTTP
    echo 服务地址: http://localhost:8081
    echo 服务状态: 已启动（开机自启动）
    echo.
    echo 管理命令:
    echo   启动: nssm start FaceRecognitionHTTP
    echo   停止: nssm stop FaceRecognitionHTTP
    echo   重启: nssm restart FaceRecognitionHTTP
    echo   卸载: nssm remove FaceRecognitionHTTP confirm
    echo.
    echo 查看日志:
    echo   type logs\face_service.log
    echo   type logs\service_stdout.log
    echo.
    echo 测试服务:
    echo   curl http://localhost:8081/health
    echo.
    echo ========================================
) else (
    echo.
    echo [错误] 服务启动失败！
    echo 请查看日志: logs\service_stderr.log
    echo.
)

pause

