@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   NewsOfficer 安装包构建工具
echo ========================================
echo.

:: 设置路径
set "PROJECT_DIR=%~dp0.."
set "INSTALLER_DIR=%~dp0"
set "DIST_DIR=%PROJECT_DIR%\dist"

:: 检查 exe 是否存在
if not exist "%DIST_DIR%\NewsOfficer.exe" (
    echo [!] 未找到 NewsOfficer.exe
    echo [*] 请先运行 python build.py 打包程序
    pause
    exit /b 1
)

echo [1/3] 准备安装文件...
echo.

:: 创建临时目录
set "TEMP_DIR=%INSTALLER_DIR%\temp"
if exist "%TEMP_DIR%" rmdir /S /Q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
mkdir "%TEMP_DIR%\dist"
mkdir "%TEMP_DIR%\dist\reports"

:: 复制文件
copy /Y "%DIST_DIR%\NewsOfficer.exe" "%TEMP_DIR%\dist\" >nul
copy /Y "%DIST_DIR%\config.py" "%TEMP_DIR%\dist\" >nul
copy /Y "%PROJECT_DIR%\README.md" "%TEMP_DIR%\" >nul
copy /Y "%PROJECT_DIR%\LICENSE" "%TEMP_DIR%\" >nul
copy /Y "%INSTALLER_DIR%\install.bat" "%TEMP_DIR%\" >nul

echo [OK] 文件准备完成
echo.

echo [2/3] 创建安装包...
echo.

:: 使用 PowerShell 创建 ZIP 压缩包
set "OUTPUT_FILE=%DIST_DIR%\NewsOfficer_v1.1.0_Windows.zip"
if exist "%OUTPUT_FILE%" del /Q "%OUTPUT_FILE%"

powershell -Command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%OUTPUT_FILE%' -CompressionLevel Optimal"

if %errorlevel% neq 0 (
    echo [!] 创建 ZIP 失败
    pause
    exit /b 1
)

echo [OK] ZIP 安装包已创建: %OUTPUT_FILE%
echo.

echo [3/3] 清理临时文件...
rmdir /S /Q "%TEMP_DIR%"
echo [OK] 清理完成
echo.

echo ========================================
echo   [OK] 安装包构建完成！
echo ========================================
echo.
echo   输出文件: %OUTPUT_FILE%
echo.
echo   用户解压后运行 install.bat 即可安装
echo.
echo ========================================

pause
