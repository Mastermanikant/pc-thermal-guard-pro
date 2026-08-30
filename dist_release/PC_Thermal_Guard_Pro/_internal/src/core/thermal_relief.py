"""
Smart 1-Click Thermal Relief & Secure Fan Control Engine
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import os
import json
import time
import threading
from typing import Dict, Any, List, Optional
import psutil

# Configuration File Path
_appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
CONFIG_DIR = os.path.join(_appdata, "FrankBase", "PCThermalGuardPro")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "thermal_config.json")

def get_foreground_process_id() -> Optional[int]:
    try:
        import win32gui
        import win32process
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return pid
    except Exception:
        pass
    return None

class ThermalReliefEngine:
    # Configurable Thresholds (Saved to disk)
    restore_target_temp: float = 55.0      # Target temperature to restore normal priority
    restore_timeout_sec: int = 45          # Maximum time to keep throttled (seconds)
    fan_security_enabled: bool = True       # Enforces 25% stall floor and 75°C emergency override
    emergency_override_temp: float = 75.0  # Temperature that forces 100% fan speed

    # Runtime registry
    _throttled_registry: Dict[int, Dict[str, Any]] = {}
    _watcher_thread: Optional[threading.Thread] = None
    _lock = threading.Lock()

    @classmethod
    def load_config(cls):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls.restore_target_temp = float(data.get("restore_target_temp", 55.0))
                    cls.restore_timeout_sec = int(data.get("restore_timeout_sec", 45))
                    cls.fan_security_enabled = bool(data.get("fan_security_enabled", True))
                    cls.emergency_override_temp = float(data.get("emergency_override_temp", 75.0))
        except Exception:
            pass

    @classmethod
    def save_config(cls, target_temp: float = None, timeout_sec: int = None, fan_sec: bool = None):
        if target_temp is not None:
            cls.restore_target_temp = float(target_temp)
        if timeout_sec is not None:
            cls.restore_timeout_sec = int(timeout_sec)
        if fan_sec is not None:
            cls.fan_security_enabled = bool(fan_sec)

        try:
            data = {
                "restore_target_temp": cls.restore_target_temp,
                "restore_timeout_sec": cls.restore_timeout_sec,
                "fan_security_enabled": cls.fan_security_enabled,
                "emergency_override_temp": cls.emergency_override_temp,
                "updated_at": time.time()
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    @classmethod
    def throttle_process(cls, pid: int, is_auto: bool = False) -> Dict[str, Any]:
        """Throttles a background process to Idle priority while preserving active foreground app."""
        fg_pid = get_foreground_process_id()
        
        # Protect active foreground app
        if fg_pid and pid == fg_pid:
            return {
                "success": False,
                "message": f"Skipped active window process (PID: {pid}). Your current active work was not interrupted.",
                "pid": pid,
                "is_foreground": True
            }

        try:
            p = psutil.Process(pid)
            p_name = p.name()

            # Ignore critical system kernel processes
            if pid <= 4 or p_name.lower() in ["system", "registry", "smss.exe", "csrss.exe"]:
                return {
                    "success": False,
                    "message": f"Cannot throttle protected Windows system process '{p_name}'.",
                    "pid": pid
                }

            with cls._lock:
                orig_nice = None
                try:
                    orig_nice = p.nice()
                except Exception:
                    pass

                # Set to IDLE priority
                if hasattr(psutil, "IDLE_PRIORITY_CLASS"):
                    p.nice(psutil.IDLE_PRIORITY_CLASS)

                # Restrict affinity to single core to drop thermal dissipation
                if hasattr(p, "cpu_affinity"):
                    p.cpu_affinity([0])

                cls._throttled_registry[pid] = {
                    "name": p_name,
                    "original_nice": orig_nice,
                    "throttled_at": time.time()
                }

            # Ensure background auto-restore watcher is running
            cls._ensure_restore_watcher()

            return {
                "success": True,
                "message": f"Successfully throttled '{p_name}' (PID: {pid}) to Idle priority. Heat generation dropped.",
                "pid": pid,
                "name": p_name,
                "is_foreground": False
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {
                "success": False,
                "message": f"Could not throttle PID {pid}: {str(e)}",
                "pid": pid
            }

    @classmethod
    def restore_process(cls, pid: int) -> bool:
        """Restores a process back to normal priority and all CPU cores."""
        with cls._lock:
            info = cls._throttled_registry.pop(pid, None)

        if not info:
            return False

        try:
            p = psutil.Process(pid)
            if hasattr(psutil, "NORMAL_PRIORITY_CLASS"):
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            if hasattr(p, "cpu_affinity"):
                p.cpu_affinity(list(range(psutil.cpu_count() or 4)))
            return True
        except Exception:
            return False

    @classmethod
    def one_click_cool_down(cls, top_culprits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Smart 1-Click Cool Down: Throttles top background culprits while protecting active window."""
        throttled_count = 0
        details = []
        skipped_fg = []

        fg_pid = get_foreground_process_id()

        for item in top_culprits[:4]:
            pid = item.get("pid")
            if pid and pid > 4:
                if fg_pid and pid == fg_pid:
                    skipped_fg.append(item.get("name", "Active App"))
                    continue

                res = cls.throttle_process(pid, is_auto=True)
                if res["success"]:
                    throttled_count += 1
                    details.append(res["name"])

        if throttled_count > 0:
            msg = f"⚡ Smart Cool Down Active: Throttled {throttled_count} background tasks ({', '.join(details)}). Auto-restores when CPU <{cls.restore_target_temp:.0f}°C or {cls.restore_timeout_sec}s."
            if skipped_fg:
                msg += f" (Protected active app: {', '.join(skipped_fg)})"
        else:
            if skipped_fg:
                msg = f"All high CPU load is from your active window ({', '.join(skipped_fg)}). No background tasks needed throttling."
            else:
                msg = "No heavy background tasks currently require throttling."

        return {
            "success": throttled_count > 0,
            "throttled_count": throttled_count,
            "message": msg
        }

    @classmethod
    def _ensure_restore_watcher(cls):
        """Starts the auto-restore daemon thread if not already active."""
        if cls._watcher_thread is not None and cls._watcher_thread.is_alive():
            return

        def _watcher_loop():
            from src.core.hardware_sensor import HardwareSensorEngine
            sensor_engine = HardwareSensorEngine.get_instance()

            while True:
                time.sleep(3.0)
                now = time.time()
                to_restore = []

                # Read live telemetry
                try:
                    telemetry = sensor_engine.get_telemetry()
                    current_temp = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 45.0
                except Exception:
                    current_temp = 50.0

                with cls._lock:
                    if not cls._throttled_registry:
                        break
                    for pid, data in list(cls._throttled_registry.items()):
                        elapsed = now - data["throttled_at"]
                        # Restore condition: Either target temp reached OR timeout exceeded
                        if current_temp <= cls.restore_target_temp or elapsed >= cls.restore_timeout_sec:
                            to_restore.append(pid)

                for pid in to_restore:
                    cls.restore_process(pid)

        cls._watcher_thread = threading.Thread(target=_watcher_loop, daemon=True)
        cls._watcher_thread.start()

# Load saved config on startup
ThermalReliefEngine.load_config()