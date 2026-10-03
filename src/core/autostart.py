"""
Windows Startup & Registry Integration Engine
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import os
import sys
import winreg
from src.core.logger import get_logger

logger = get_logger("AutoStart")

REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "PCThermalGuardPro"

def is_autostart_enabled() -> bool:
    """Checks if the application is registered in Windows Startup."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        logger.warning(f"Error checking autostart registry: {e}")
        return False

def set_autostart(enabled: bool) -> bool:
    """Enables or disables silent background launch at Windows Startup."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                if getattr(sys, "frozen", False):
                    exe_path = sys.executable
                else:
                    exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "main.py"))
                    exe_path = f'"{sys.executable}" "{exe_path}"'

                cmd = f'{exe_path} --minimized'
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
                logger.info("Windows Startup enabled (Silent Tray Mode).")
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                    logger.info("Windows Startup disabled.")
                except FileNotFoundError:
                    pass
            return True
    except Exception as e:
        logger.error(f"Error setting autostart registry: {e}")
        return False
