; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
; Will be adapted by "python setup.py py2exe"

[Setup]
AppName=Cognitionplay
AppComments="Collection of educational activities"
AppVerName=$AppVerName$
AppVersion=$AppVersion$
AppContact="chris.van.bael@gmail.com"
AppPublisherURL=http://www.schoolsplay.org
AppSupportURL=http://www.schoolsplay.org
AppUpdatesURL=http://www.schoolsplay.org
VersionInfoVersion=$VersionInfoVersion$
VersionInfoDescription="Collection of educational activities"
DefaultDirName={pf}\Cognitionplay
DefaultGroupName=Cognitionplay
AllowNoIcons=yes
InfoBeforeFile=$BaseDir$\dist\share\doc\childsplay_sp\license.txt
OutputDir=$BaseDir$\dist\installer
OutputBaseFilename=$OutputBaseFilename$
;SetupIconFile=$BaseDir$\dist\data\schoolsplay.ico
Compression=lzma
SolidCompression=yes
;VersionInfoVersion=$VersionInfoVersion$
;WizardImageFile=$BaseDir$\dist\data\logo_cp_64x64.bmp
;WizardSmallImageFile=$BaseDir$\dist\data\logo_cp_48x48.bmp
PrivilegesRequired=none

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "indonesian"; MessagesFile: "compiler:Languages\Indonesian.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "swedish"; MessagesFile: "compiler:Languages\Swedish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "$BaseDir$\dist\cognitionplay.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "$BaseDir$\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[INI]
Filename: "{app}\Cognitionplay.url"; Section: "InternetShortcut"; Key: "URL"; String: "http://www.schoolsplay.org"

[Icons]
Name: "{group}\Cognitionplay windowed"; Filename: "{app}\Cognitionplay.exe"; WorkingDir: "{app}"; Comment: "Start Cognitionplay in a window"
Name: "{group}\Cognitionplay fullscreen"; Filename: "{app}\Cognitionplay.exe"; Parameters: "--fullscreen"; WorkingDir: "{app}"; Comment: "Start Cognitionplay fullscreen"
Name: "{group}\Admin App"; Filename: "{app}\Cognitionplay.exe"; Parameters: "--admin-gui"; WorkingDir: "{app}"; Comment: "Administer Cognitionplay settings and results"
Name: "{group}\{cm:ProgramOnTheWeb,cognitionplay}"; Filename: "{app}\Cognitionplay.url"
Name: "{group}\{cm:UninstallProgram,Cognitionplay}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Cognitionplay"; Filename: "{app}\Cognitionplay.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Cognitionplay"; Filename: "{app}\Cognitionplay.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\Cognitionplay.exe"; Description: "{cm:LaunchProgram,Cognitionplay}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\Cognitionplay.url"

