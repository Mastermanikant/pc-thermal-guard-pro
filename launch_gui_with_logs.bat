@echo off
title PC Thermal Guard Pro - Desktop GUI Launcher
color 0A
cls

echo ==============================================================================
echo        PC THERMAL GUARD PRO - MODERN DESKTOP GUI LAUNCHER
echo        Master Manikant Yadav Ecosystem (FrankBase System Suite)
echo ==============================================================================
echo.
echo Launching Modern Desktop Interface...
echo Output log: D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro\logs\app_runtime.log
echo.

cd /d "D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro"
python main.py > logs\app_runtime.log 2>&1

echo Application closed.