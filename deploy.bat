@echo off
chcp 65001 >nul
REM 部署新编译的face_extractor.exe
echo ========================================
echo 部署face_extractor.exe
echo ========================================
echo.

REM 等待编译完成
echo [1/4] 检查编译输出...
:WAIT_LOOP
if not exist "dist\face_extractor.exe" (
    echo 等待编译完成...
    timeout /t 5 /nobreak >nul
    goto WAIT_LOOP
)

echo [√] 编译完成！
echo.

REM 显示文件信息
echo [2/4] 检查文件大小...
for %%I in (dist\face_extractor.exe) do set "filesize=%%~zI"
set /a "filesize_mb=%filesize% / 1048576"
echo 文件大小: %filesize_mb% MB
echo.

REM 复制到meeting-server/test目录
echo [3/4] 部署到test目录...
if not exist "..\meeting-server\test" (
    mkdir "..\meeting-server\test"
)
copy /y "dist\face_extractor.exe" "..\meeting-server\test\face_extractor.exe"
if %errorlevel% equ 0 (
    echo [√] 已复制到 ..\meeting-server\test\face_extractor.exe
) else (
    echo [X] 复制到test目录失败
)
echo.

REM 替换meeting-server/face-extractor目录的旧版本
echo [4/4] 替换生产版本...
if exist "..\meeting-server\face-extractor\face-extractor.exe" (
    echo 备份旧版本...
    copy /y "..\meeting-server\face-extractor\face-extractor.exe" "..\meeting-server\face-extractor\face-extractor.exe.old"
    
    echo 部署新版本...
    copy /y "dist\face_extractor.exe" "..\meeting-server\face-extractor\face-extractor.exe"
    if %errorlevel% equ 0 (
        echo [√] 生产版本已更新
    ) else (
        echo [X] 更新生产版本失败
    )
) else (
    echo 创建face-extractor目录...
    if not exist "..\meeting-server\face-extractor" mkdir "..\meeting-server\face-extractor"
    copy /y "dist\face_extractor.exe" "..\meeting-server\face-extractor\face-extractor.exe"
    echo [√] 生产版本已部署
)
echo.

echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 已部署到：
echo   1. ..\meeting-server\test\face_extractor.exe
echo   2. ..\meeting-server\face-extractor\face-extractor.exe
echo.
echo 下一步：
echo   1. 重启后端服务（meeting-server）
echo   2. 测试人脸上传功能
echo.
pause

