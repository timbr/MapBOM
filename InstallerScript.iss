; -- InstallerScript.iss --
; Installer script for MapBom


[Setup]
AppName=MapBom GUI v0.3.1
AppVerName=MapBom GUI version 0.3.1
DefaultDirName={pf}\MapBom
;DefaultGroupName=MapBom
UninstallDisplayIcon={app}\MapBom.exe
Compression=lzma
SolidCompression=yes
OutputDir=Installer

[Files]
Source: MapBom.exe; DestDir: {app}
Source: MapBom_v0_3_1.lnk; DestDir: {commondesktop}
Source: MapBom_v0_3_1.lnk; DestDir: {commonprograms}
Source: FreemindPortable.bat; DestDir: {app}
Source: mapbom.ico; DestDir: {app}
Source: Data\*; DestDir: {app}\Data\; Flags: recursesubdirs
;Source: \\Sheffield\SPD_Data\Temporary\MapBom\Drawings\*; DestDir: {app}\Drawings\
Source: Readme.txt; DestDir: {app}; Flags: isreadme

[Dirs]
Name: {app}\Drawings\

[UninstallDelete]
Type: files; Name: {app}\BOMmindmap.mm

[Icons]
;Name: {commonprograms}\MapBom_0.2.7; Filename: {app}\MapBom.exe
;Name: {commondesktop}\MapBom_0.2.7; Filename: {app}\MapBom.exe
;
;Note that the shortcuts created don't specify where the program is run, so the Freemind starter won't work...
