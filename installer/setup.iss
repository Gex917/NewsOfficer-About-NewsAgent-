; NewsOfficer 安装脚本 - Inno Setup
; 下载 Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "NewsOfficer"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "NewsOfficer Team"
#define MyAppURL "https://github.com/newsagent"
#define MyAppExeName "NewsOfficer.exe"

[Setup]
; 注: AppId 的值用于唯一标识此应用程序
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; 安装程序图标
; SetupIconFile=..\assets\icon.ico
; 卸载程序图标
; UninstallIconFile=..\assets\icon.ico
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=NewsOfficer_Setup
; 压缩选项
Compression=lzma2/ultra64
SolidCompression=yes
; 界面选项
WizardStyle=modern
; 需要管理员权限
PrivilegesRequired=admin
; 支持 Windows 10/11
MinVersion=10.0
; 架构
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 主程序
Source: "..\dist\NewsOfficer.exe"; DestDir: "{app}"; Flags: ignoreversion
; 配置文件
Source: "..\dist\config.py"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist uninsneveruninstall
; 报告目录
Source: "..\dist\reports\*"; DestDir: "{app}\reports"; Flags: ignoreversion createallsubdirs recursesubdirs
; README
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\reports"
Name: "{app}\logs"

[Icons]
; 开始菜单
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; 桌面快捷方式
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; 快速启动
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安装完成后运行
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 卸载时删除日志
Type: filesandordirs; Name: "{app}\logs"
; 注意: 不删除配置文件和报告，保留用户数据
