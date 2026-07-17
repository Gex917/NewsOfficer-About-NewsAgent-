@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   NewsOfficer 安装程序
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 请以管理员身份运行此脚本
    echo     右键点击 -^> 以管理员身份运行
    pause
    exit /b 1
)

:: 设置安装目录
set "INSTALL_DIR=%ProgramFiles%\NewsOfficer"
set "DESKTOP_DIR=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\NewsOfficer"

echo [*] 安装目录: %INSTALL_DIR%
echo.

:: 创建安装目录
echo [*] 创建安装目录...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\reports" mkdir "%INSTALL_DIR%\reports"
if not exist "%INSTALL_DIR%\logs" mkdir "%INSTALL_DIR%\logs"

:: 复制文件
echo [*] 复制程序文件...
copy /Y "%~dp0dist\NewsOfficer.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo [!] 复制 NewsOfficer.exe 失败
    pause
    exit /b 1
)

:: 复制配置文件（不覆盖已存在的）
if not exist "%INSTALL_DIR%\config.py" (
    copy /Y "%~dp0dist\config.py" "%INSTALL_DIR%\" >nul
    echo [*] 已创建默认配置文件
) else (
    echo [*] 配置文件已存在，跳过
)

:: 复制 README
copy /Y "%~dp0README.md" "%INSTALL_DIR%\" >nul

:: 创建桌面快捷方式
echo [*] 创建桌面快捷方式...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP_DIR%\NewsOfficer.lnk'); $s.TargetPath = '%INSTALL_DIR%\NewsOfficer.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'NewsOfficer - AI 资讯收集助手'; $s.Save()"

:: 创建开始菜单
echo [*] 创建开始菜单...
if not exist "%START_MENU%" mkdir "%START_MENU%"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%START_MENU%\NewsOfficer.lnk'); $s.TargetPath = '%INSTALL_DIR%\NewsOfficer.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'NewsOfficer - AI 资讯收集助手'; $s.Save()"

:: 创建卸载程序
echo [*] 创建卸载程序...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo   NewsOfficer 卸载程序
echo echo ========================================
echo echo.
echo echo [*] 删除程序文件...
echo del /Q "%INSTALL_DIR%\NewsOfficer.exe" 2^>nul
echo del /Q "%INSTALL_DIR%\README.md" 2^>nul
echo rmdir /S /Q "%INSTALL_DIR%\logs" 2^>nul
echo echo [*] 删除快捷方式...
echo del /Q "%DESKTOP_DIR%\NewsOfficer.lnk" 2^>nul
echo rmdir /S /Q "%START_MENU%" 2^>nul
echo echo [*] 保留配置文件和报告...
echo echo [*] 如需完全删除，请手动删除: %INSTALL_DIR%
echo echo.
echo echo [*] 卸载完成！
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

:: 创建开始菜单卸载快捷方式
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%START_MENU%\卸载 NewsOfficer.lnk'); $s.TargetPath = '%INSTALL_DIR%\uninstall.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = '卸载 NewsOfficer'; $s.Save()"

echo.
echo ========================================
echo   [OK] 安装完成！
echo ========================================
echo.
echo   程序位置: %INSTALL_DIR%\NewsOfficer.exe
echo   桌面快捷方式: 已创建
echo   开始菜单: 已创建
echo.
echo   首次运行请配置 API Key
echo.
echo ========================================

:: 询问是否立即运行
set /p RUN="是否立即运行 NewsOfficer? (Y/N): "
if /i "%RUN%"=="Y" (
    start "" "%INSTALL_DIR%\NewsOfficer.exe"
)

pause
