"""
Rolling Telemetry History & Diagnostic Ledger Engine
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import os
import sqlite3
import time
import json
import collections
from typing import List, Dict, Any, Optional
from src.core.logger import get_logger

logger = get_logger("HistoryManager")

class HistoryManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = HistoryManager()
        return cls._instance

    def __init__(self, db_path: Optional[str] = None):
        _appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
        default_dir = os.path.join(_appdata, "FrankBase", "PCThermalGuardPro")
        os.makedirs(default_dir, exist_ok=True)

        self.config_file = os.path.join(default_dir, "thermal_config.json")
        self.db_path = db_path or os.path.join(default_dir, "thermal_history.db")
        # Tier 1: In-memory 60-minute circular ring buffer (sampled 1Hz = 3600 samples)
        self.ring_buffer = collections.deque(maxlen=3600)
        self._last_disk_flush = time.time()
        self.is_logging_enabled = True

        self._load_config()
        self._init_sqlite_db()
        HistoryManager._instance = self

    def _load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.is_logging_enabled = bool(data.get("history_logging_enabled", True))
        except Exception as e:
            logger.warning(f"Could not load history config: {e}")

    def save_config(self, enabled: bool):
        self.is_logging_enabled = enabled
        try:
            data = {}
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            data["history_logging_enabled"] = enabled
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved history logging config: enabled={enabled}")
        except Exception as e:
            logger.error(f"Error saving history logging config: {e}")

    def _init_sqlite_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA journal_mode = WAL;")
                conn.execute("""
                CREATE TABLE IF NOT EXISTS thermal_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    cpu_temp REAL NOT NULL,
                    cpu_load REAL NOT NULL,
                    gpu_temp REAL NOT NULL,
                    fan_rpm INTEGER NOT NULL,
                    top_culprit TEXT NOT NULL,
                    top_has REAL NOT NULL,
                    diag_status TEXT NOT NULL
                );
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON thermal_logs(timestamp);")
                conn.commit()
            logger.info(f"SQLite DB initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"DB Init Error: {e}")

    def record_sample(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diag_status: str = "OPTIMAL"):
        now = time.time()
        cpu_temp = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp", 24.0)
        cpu_load = telemetry.get("cpu_load", 0.0)
        cpu_power = telemetry.get("cpu_power", 0.0)
        ram_pct = telemetry.get("ram_pct", 0.0)
        gpu_temp = telemetry.get("gpu_temp", 22.0)
        fan_rpm = telemetry.get("fan_rpm", 0)

        top_name = culprits[0]["name"] if culprits else "System"
        top_has = culprits[0]["heat_score"] if culprits else 0.0

        sample = {
            "timestamp": now,
            "time_str": time.strftime("%H:%M:%S", time.localtime(now)),
            "cpu_temp": cpu_temp,
            "cpu_load": cpu_load,
            "cpu_power": cpu_power,
            "ram_pct": ram_pct,
            "gpu_temp": gpu_temp,
            "fan_rpm": fan_rpm,
            "top_culprit": top_name,
            "top_has": top_has,
            "diag_status": diag_status
        }

        # Tier 1: In-memory instant ring buffer append (always kept for live in-session graph)
        self.ring_buffer.append(sample)

        # Tier 2: Flush to SQLite every 60 seconds (ONLY IF LOGGING IS ENABLED)
        if self.is_logging_enabled:
            if (now - self._last_disk_flush >= 60.0) or (cpu_temp >= 80.0 and now - self._last_disk_flush >= 10.0):
                self._flush_to_db(sample)
                self._last_disk_flush = now

    def add_telemetry_point(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diag_status: str = "OPTIMAL"):
        """Alias for record_sample to ensure 100% backward compatibility."""
        self.record_sample(telemetry, culprits, diag_status)

    def _flush_to_db(self, sample: Dict[str, Any]):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO thermal_logs (timestamp, cpu_temp, cpu_load, gpu_temp, fan_rpm, top_culprit, top_has, diag_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        sample["timestamp"],
                        sample["cpu_temp"],
                        sample["cpu_load"],
                        sample["gpu_temp"],
                        sample["fan_rpm"],
                        sample["top_culprit"],
                        sample["top_has"],
                        sample["diag_status"]
                    )
                )
                conn.commit()
            self._enforce_retention_policy()
        except Exception as e:
            logger.error(f"DB Flush Error: {e}")

    def _enforce_retention_policy(self):
        try:
            seven_days_ago = time.time() - (7 * 86400)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM thermal_logs WHERE timestamp < ?;", (seven_days_ago,))
                conn.commit()

            if os.path.exists(self.db_path):
                size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
                if size_mb > 25.0:
                    with sqlite3.connect(self.db_path) as conn:
                        conn.execute("DELETE FROM thermal_logs WHERE id IN (SELECT id FROM thermal_logs ORDER BY timestamp ASC LIMIT 5000);")
                        conn.execute("VACUUM;")
                        conn.commit()
        except Exception:
            pass

    def get_recent_ring_buffer(self) -> List[Dict[str, Any]]:
        return list(self.ring_buffer)

    def get_historical_records(self, limit: int = 100) -> List[Dict[str, Any]]:
        records = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM thermal_logs ORDER BY timestamp DESC LIMIT ?;", (limit,))
                for row in cursor.fetchall():
                    d = dict(row)
                    d["time_str"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d["timestamp"]))
                    records.append(d)
        except Exception as e:
            logger.error(f"DB Read Error: {e}")
        return records

    def get_db_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Alias for HistoryView."""
        return self.get_historical_records(limit=limit)

    def clear_all_history(self) -> bool:
        """Clears all stored historical records from the SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM thermal_logs;")
                conn.execute("VACUUM;")
                conn.commit()
            self.ring_buffer.clear()
            logger.info("History database cleared.")
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return False

    def export_report_json(self, file_path: str) -> bool:
        try:
            records = self.get_historical_records(limit=500)
            data = {
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": len(records),
                "records": records
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Report successfully exported to: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Export Error: {e}")
            return False