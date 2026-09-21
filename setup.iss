[Setup]
AppName=Jarvis AI Mouse
AppVersion=1.0
DefaultDirName={autopf}\Jarvis AI Mouse
DefaultGroupName=Jarvis AI Mouse
OutputDir=C:\Users\user\JARVIS_AI_handtracking\Output
OutputBaseFilename=Jarvis_AI_Mouse_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startupicon"; Description: "Run Jarvis automatically when Windows starts"; GroupDescription: "Startup Options"

[Files]
Source: "C:\Users\user\JARVIS_AI_handtracking\dist\Jarvis_AI_Mouse\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Jarvis AI Mouse"; Filename: "{app}\Jarvis_AI_Mouse.exe"
Name: "{autodesktop}\Jarvis AI Mouse"; Filename: "{app}\Jarvis_AI_Mouse.exe"; Tasks: desktopicon
Name: "{userstartup}\Jarvis AI Mouse"; Filename: "{app}\Jarvis_AI_Mouse.exe"; Tasks: startupicon

[Run]
Filename: "{app}\Jarvis_AI_Mouse.exe"; Description: "{cm:LaunchProgram,Jarvis AI Mouse}"; Flags: nowait postinstall skipifsilent