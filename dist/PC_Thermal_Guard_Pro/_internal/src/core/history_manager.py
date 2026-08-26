"""
Rolling Telemetry History & Diagnostic Ledger Engine
PC Thermal Guard Pro

2-Tier Storage Architecture:
- Tier 1: In-memory circular buffer (deque) for real-time 60-min live visual scrubbing (Zero Disk IO).
- Tier 2: SQLite database (WAL mode) storing 7-day rolling telemetry, auto-capped at 25MB.
"""
import os
import sqlite3
import time
import json
import collections
from typing import List, Dict, Any, Optional

class HistoryManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "thermal_history.db")
        )
        # Tier 1: In-memory 60-minute circular ring buffer (sampled 1Hz = 3600 samples)
        self.ring_buffer = collections.deque(maxlen=3600)
        self._last_disk_flush = time.time()
        self._init_sqlite_db()

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
        except Exception as e:
            print(f"DB Init Error: {e}")

    def record_sample(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diag_status: str):
        now = time.time()
        cpu_temp = telemetry.get("cpu_temp", 45.0)
        cpu_load = telemetry.get("cpu_load", 0.0)
        gpu_temp = telemetry.get("gpu_temp", 42.0)
        fan_rpm = telemetry.get("fan_rpm", 1200)

        top_name = culprits[0]["name"] if culprits else "System"
        top_has = culprits[0]["heat_score"] if culprits else 0.0

        sample = {
            "timestamp": now,
            "time_str": time.strftime("%H:%M:%S", time.localtime(now)),
            "cpu_temp": cpu_temp,
            "cpu_load": cpu_load,
            "gpu_temp": gpu_temp,
            "fan_rpm": fan_rpm,
            "top_culprit": top_name,
            "top_has": top_has,
            "diag_status": diag_status
        }

        # Tier 1: In-memory instant ring buffer append
        self.ring_buffer.append(sample)

        # Tier 2: Flush to SQLite every 60 seconds (or on high overheat event)
        if (now - self._last_disk_flush >= 60.0) or (cpu_temp >= 85.0 and now - self._last_disk_flush >= 10.0):
            self._flush_to_db(sample)
            self._last_disk_flush = now

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
            print(f"DB Flush Error: {e}")

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

    def get_db_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM thermal_logs ORDER BY timestamp DESC LIMIT ?;", (limit,)
                )
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    t_val = r["timestamp"]
                    results.append({
                        "id": r["id"],
                        "timestamp": t_val,
                        "time_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t_val)),
                        "cpu_temp": r["cpu_temp"],
                        "cpu_load": r["cpu_load"],
                        "gpu_temp": r["gpu_temp"],
                        "fan_rpm": r["fan_rpm"],
                        "top_culprit": r["top_culprit"],
                        "top_has": r["top_has"],
                        "diag_status": r["diag_status"]
                    })
                return results
        except Exception:
            return []

    def export_report_json(self, export_file: str) -> bool:
        try:
            records = self.get_db_history(limit=5000)
            data = {
                "tool": "PC Thermal Guard Pro",
                "export_timestamp": time.time(),
                "export_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "record_count": len(records),
                "records": records
            }
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False