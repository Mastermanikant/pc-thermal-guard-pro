"""
Global Structured Logging Framework
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

_appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
LOG_DIR = os.path.join(_appdata, "FrankBase", "PCThermalGuardPro", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "thermal_guard.log")

# Setup logger
logger = logging.getLogger("PCThermalGuardPro")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # 1. Console Handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # 2. Rotating File Handler (Max 5MB, 3 backups)
    try:
        f_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)
        logger.info(f"Logging initialized. Log file: {LOG_FILE}")
    except Exception as e:
        logger.warning(f"Could not initialize rotating file logger: {e}")

def get_logger(name: str = "PCThermalGuardPro") -> logging.Logger:
    return logging.getLogger(name)

def get_log_file_path() -> str:
    return LOG_FILE