!include "MUI2.nsh"

!define APP_NAME    "Roleta Russa"
!define APP_VERSION "3.9"
!define APP_EXE     "RoletaRussa.exe"
!define PUBLISHER   "Alex Torres"
!define UNINST_KEY  "Software\Microsoft\Windows\CurrentVersion\Uninstall\RoletaRussa"

Name              "${APP_NAME} ${APP_VERSION}"
OutFile           "RoletaRussa-Setup.exe"
InstallDir        "$PROGRAMFILES\RoletaRussa"
InstallDirRegKey  HKLM "Software\RoletaRussa" "Install_Dir"
RequestExecutionLevel admin

!define MUI_ABORTWARNING
!define MUI_ICON   "img\rr_icon.ico"
!define MUI_UNICON "img\rr_icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "Instalar" SecInstall
    SetOutPath "$INSTDIR"
    File /r "dist\RoletaRussa\*"

    WriteRegStr HKLM "Software\RoletaRussa" "Install_Dir" "$INSTDIR"

    ; Desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0

    ; Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"  "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Desinstalar.lnk"  "$INSTDIR\Desinstalar.exe"

    ; Add/Remove Programs entry
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayName"     "${APP_NAME}"
    WriteRegStr   HKLM "${UNINST_KEY}" "UninstallString" '"$INSTDIR\Desinstalar.exe"'
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayVersion"  "${APP_VERSION}"
    WriteRegStr   HKLM "${UNINST_KEY}" "Publisher"       "${PUBLISHER}"
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify"        1
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair"        1

    WriteUninstaller "$INSTDIR\Desinstalar.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    Delete   "$DESKTOP\${APP_NAME}.lnk"
    RMDir /r "$SMPROGRAMS\${APP_NAME}"
    DeleteRegKey HKLM "${UNINST_KEY}"
    DeleteRegKey HKLM "Software\RoletaRussa"
SectionEnd
