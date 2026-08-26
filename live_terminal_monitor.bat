@echo off
title PC Thermal Guard Pro - Live Terminal Monitor & Stream Logger
color 0B
cls

echo ==============================================================================
echo        PC THERMAL GUARD PRO - LIVE HARDWARE & CULPRIT MONITOR
echo        Master Manikant Yadav Ecosystem (FrankBase System Suite)
echo ==============================================================================
echo.
echo Starting live hardware telemetry streaming and continuous logging...
echo Logs will be written to: D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro\logs\live_thermal_stream.log
echo.
timeout /t 2 /nobreak >nul

cd /d "D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro"
python src\cli_live_monitor.py

echo.
echo ==============================================================================
echo Live Monitoring Session Terminated.
echo You can view the log file at:
echo D:\02_Desktop_and_Mobile_Apps\PC_Thermal_Guard_Pro\logs\live_thermal_stream.log
echo ==============================================================================
echo.
pause