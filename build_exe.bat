@echo off
title Building PC Thermal Guard Pro Standalone Executable...
echo =======================================================
echo Compiling PC Thermal Guard Pro with PyInstaller...
echo =======================================================

pyinstaller --noconfirm --onedir --windowed ^
    --name "PC_Thermal_Guard_Pro" ^
    --add-data "lib/LibreHardwareMonitorLib.dll;lib" ^
    --add-data "lib/HidSharp.dll;lib" ^
    --add-data "src;src" ^
    main.py

echo.
echo =======================================================
echo Build Completed Successfully!
echo Executable Location: dist\PC_Thermal_Guard_Pro\PC_Thermal_Guard_Pro.exe
echo =======================================================
pause