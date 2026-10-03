"""
PC Thermal Guard Pro - Entrypoint Bootstrapper
Master Manikant Yadav Ecosystem (FrankBase System Suite)
"""
import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import customtkinter as ctk

# Strictly enforce Dark Mode on startup before any widget initialization
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

from src.core.hardware_sensor import HardwareSensorEngine
from src.core.history_manager import HistoryManager
from src.core.system_cleaner import SafeSystemCleaner
from src.ui.main_window import MainWindow

def main():
    # Enable High-DPI Awareness on Windows
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # Initialize Core Engines
    sensor_engine = HardwareSensorEngine.get_instance()
    history_manager = HistoryManager()

    # Execute silent startup hygiene sweep (Cleans stale temp & RAM working set)
    SafeSystemCleaner.execute_startup_hygiene_sweep()

    # Launch GUI Controller
    app = MainWindow(sensor_engine=sensor_engine, history_manager=history_manager)
    if "--minimized" in sys.argv or "--tray" in sys.argv:
        app.after(100, app.minimize_to_tray)
    app.mainloop()

if __name__ == "__main__":
    main()