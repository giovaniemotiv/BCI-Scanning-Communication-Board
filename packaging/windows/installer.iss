; Inno Setup script for the EMOTIV BCI Communication Board.
;
; Compiled by the build workflow after PyInstaller has produced
; dist\EMOTIV BCI Board\. To build locally, from the repository root:
;
;     pyinstaller packaging/BCIScanningBoard.spec --noconfirm
;     iscc packaging\windows\installer.iss
;
; Produces installer\EMOTIV-BCI-Board-Setup-<version>.exe. The installer is
; unsigned, so SmartScreen shows a warning on first run.

#define AppName "EMOTIV BCI Board"
#define AppVersion "1.0.0"
#define AppPublisher "EMOTIV"
#define AppExeName "EMOTIV BCI Board.exe"

[Setup]
AppId={{9C1D4E7A-3F62-4A18-9B6D-2E5C7A0B4F31}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
; Per-user install by default, so no UAC prompt and no admin account needed —
; the people setting this up for a patient often do not have one.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\..\installer
OutputBaseFilename=EMOTIV-BCI-Board-Setup-{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; PyQt6 ships 64-bit only, so refuse to install where it cannot run.
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; The whole PyInstaller COLLECT folder, Qt plugins and all.
Source: "..\..\dist\{#AppName}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; PyInstaller writes nothing here, but Qt and Python leave __pycache__ behind;
; without this the install directory survives an uninstall.
Type: filesandordirs; Name: "{app}"
