"""
History & Multi-Metric Live Vertical Level Meter View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import tkinter as tk
import customtkinter as ctk
import time
import os
from typing import Dict, Any, List, Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_GREEN, NEON_MAGENTA
from src.core.history_manager import HistoryManager

class HistoryView(ctk.CTkFrame):
    def __init__(self, master, history_manager: HistoryManager, on_toast: Callable[[str, str], None] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.history_manager = history_manager
        self.on_toast = on_toast
        self._last_chart_draw = 0.0
        
        self._build_ui()

    def _build_ui(self):
        # ── 1. Top Section: Live Real-Time Multi-Sensor Vertical Meter Board ──
        self.meter_card = ctk.CTkFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        self.meter_card.pack(fill="x", padx=10, pady=(4, 8))

        meter_hdr = ctk.CTkFrame(self.meter_card, fg_color="transparent")
        meter_hdr.pack(fill="x", padx=15, pady=(10, 4))

        self.lbl_meter_title = ctk.CTkLabel(
            meter_hdr,
            text="📊 Live Real-Time Multi-Sensor Level Meters",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.lbl_meter_title.pack(side="left")

        self.lbl_meter_sub = ctk.CTkLabel(
            meter_hdr,
            text="0-100 Dynamic Scale (Real-Time Live Gauge)",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color=ThemeManager.get("text_muted")
        )
        self.lbl_meter_sub.pack(side="right")

        # Canvas for Drawing Live Dynamic Vertical Level Meters
        self.meter_canvas = tk.Canvas(
            self.meter_card,
            height=190,
            bg=ThemeManager.get("bg_card"),
            highlightthickness=0
        )
        self.meter_canvas.pack(fill="both", expand=True, padx=12, pady=(2, 10))

        # ── 2. Bottom Section: 7-Day Rolling SQLite Telemetry Ledger ──
        self.log_header = ctk.CTkFrame(self, fg_color="transparent")
        self.log_header.pack(fill="x", padx=10, pady=(4, 4))

        self.log_title = ctk.CTkLabel(
            self.log_header,
            text="📋 Rolling 7-Day Telemetry Incident Ledger (SQLite WAL)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.log_title.pack(side="left")

        # Action Buttons
        self.actions_frame = ctk.CTkFrame(self.log_header, fg_color="transparent")
        self.actions_frame.pack(side="right")

        self.btn_export_json = ctk.CTkButton(
            self.actions_frame,
            text="💾 Export JSON",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color="#0284c7",
            text_color=ThemeManager.get("text_primary"),
            width=95,
            height=26,
            corner_radius=6,
            command=self._on_export_json
        )
        self.btn_export_json.pack(side="left", padx=4)

        self.btn_refresh_log = ctk.CTkButton(
            self.actions_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color="#0284c7",
            text_color=ThemeManager.get("text_primary"),
            width=75,
            height=26,
            corner_radius=6,
            command=self.refresh_log_table
        )
        self.btn_refresh_log.pack(side="left", padx=4)

        # Scrollable Log Table
        self.log_table_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border"),
            height=160
        )
        self.log_table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.refresh_log_table()
        self.update_chart(force=True)

    def update_live_chart(self):
        """Alias for real-time live meter updates."""
        self.update_chart()

    def update_chart(self, force: bool = False):
        """Renders 5 dynamic live vertical level meters on 0-100 scale."""
        now = time.time()
        if not force and (now - self._last_chart_draw < 0.6):
            return
        self._last_chart_draw = now

        samples = self.history_manager.get_recent_ring_buffer()
        canvas = self.meter_canvas
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w < 50 or h < 50:
            return

        canvas.delete("all")
        bg_card = ThemeManager.get("bg_card")
        grid_col = ThemeManager.get("border")
        txt_muted = ThemeManager.get("text_muted")
        txt_pri = ThemeManager.get("text_primary")
        canvas.configure(bg=bg_card)

        # Extract latest readings
        c_temp = 24.0
        g_temp = 22.0
        c_load = 0.0
        r_pct = 0.0
        bat_pct = 100.0
        power_plugged = True

        if samples:
            latest = samples[-1]
            c_temp = float(latest.get("cpu_temp", 24.0))
            g_temp = float(latest.get("gpu_temp", 22.0))
            c_load = float(latest.get("cpu_load", 0.0))
            r_pct = float(latest.get("ram_pct", 0.0))
            bat_pct = float(latest.get("battery_pct") if latest.get("battery_pct") is not None else 100.0)
            power_plugged = latest.get("power_plugged", True)

        # Helper scale calculation (Y position from value 0 to 100)
        y_top = 30
        y_bottom = h - 35
        usable_h = y_bottom - y_top

        def val_to_y(val):
            ratio = max(0.0, min(1.0, val / 100.0))
            return y_bottom - (ratio * usable_h)

        # 1. Draw 0 to 100 Scale Guidelines on Left Axis
        scale_steps = [(100, "100"), (75, "75"), (50, "50"), (25, "25"), (0, "0")]
        for step_val, label_text in scale_steps:
            y_pos = val_to_y(step_val)
            dash_pattern = (4, 4) if step_val == 75 else (1, 4)
            line_color = "#f97316" if step_val == 75 else grid_col
            canvas.create_line(46, y_pos, w - 20, y_pos, fill=line_color, dash=dash_pattern, width=1)
            canvas.create_text(24, y_pos, text=label_text, fill=line_color, font=("Segoe UI", 9, "bold" if step_val == 75 else "normal"))

        # Baseline axis
        canvas.create_line(46, y_bottom, w - 20, y_bottom, fill=grid_col, width=1.5)

        # 2. Define 5 Channels: (Label, Value, DisplayStr, Color)
        # CPU Temp Color
        if c_temp >= 80.0:
            c_temp_col = "#ef4444"
        elif c_temp >= 70.0:
            c_temp_col = "#f97316"
        elif c_temp >= 55.0:
            c_temp_col = "#eab308"
        else:
            c_temp_col = "#00e5ff"

        # GPU Temp Color
        if g_temp >= 75.0:
            g_temp_col = "#ef4444"
        elif g_temp >= 60.0:
            g_temp_col = "#f97316"
        else:
            g_temp_col = "#10b981"

        # CPU Load Color
        if c_load >= 70.0:
            c_load_col = "#ef4444"
        elif c_load >= 40.0:
            c_load_col = "#eab308"
        else:
            c_load_col = "#10b981"

        # RAM Color
        if r_pct >= 85.0:
            ram_col = "#ef4444"
        elif r_pct >= 70.0:
            ram_col = "#a855f7"
        else:
            ram_col = "#00e5ff"

        # Power/Bat Color
        bat_str = f"{bat_pct:.0f}%" + (" (AC)" if power_plugged else " (Bat)")
        bat_col = "#38bdf8" if power_plugged else ("#10b981" if bat_pct > 30 else "#ef4444")

        channels = [
            ("🔥 CPU Temp", c_temp, f"{c_temp:.1f}°C", c_temp_col),
            ("🎮 GPU Temp", g_temp, f"{g_temp:.1f}°C", g_temp_col),
            ("⚡ CPU Load", c_load, f"{c_load:.0f}%", c_load_col),
            ("💾 RAM Used", r_pct, f"{r_pct:.0f}%", ram_col),
            ("🔋 Power / Bat", bat_pct, bat_str, bat_col)
        ]

        # 3. Draw Vertical Towers
        start_x = 75
        usable_w = (w - 30) - start_x
        col_spacing = usable_w / len(channels)
        bar_w = min(42, max(22, col_spacing * 0.45))

        for idx, (lbl, val, val_str, col) in enumerate(channels):
            center_x = start_x + (idx * col_spacing) + (col_spacing / 2)
            x0 = center_x - (bar_w / 2)
            x1 = center_x + (bar_w / 2)
            y_val = val_to_y(val)

            # Draw background slot track
            canvas.create_rectangle(x0, y_top, x1, y_bottom, fill="#1e293b", outline=grid_col, width=1)

            # Draw dynamic filled level bar
            if y_val < y_bottom:
                canvas.create_rectangle(x0 + 1, y_val, x1 - 1, y_bottom - 1, fill=col, outline="", width=0)
                # Highlight glow cap on top
                canvas.create_line(x0, y_val, x1, y_val, fill="#ffffff", width=2)

            # Live changing value text right on top of bar
            text_y = max(14, y_val - 10)
            canvas.create_text(center_x, text_y, text=val_str, fill=col, font=("Segoe UI", 10, "bold"))

            # Label text below bar
            canvas.create_text(center_x, y_bottom + 16, text=lbl, fill=txt_pri, font=("Segoe UI", 9, "bold"))

    def refresh_log_table(self):
        """Refreshes the SQLite telemetry table."""
        for widget in self.log_table_frame.winfo_children():
            widget.destroy()

        # Table Header
        header = ctk.CTkFrame(self.log_table_frame, fg_color=ThemeManager.get("bg_card_hover"), corner_radius=6)
        header.pack(fill="x", padx=4, pady=(2, 4))

        cols = [("Time", 135), ("CPU Temp", 85), ("CPU Load", 85), ("GPU Temp", 85), ("Cooling / Fan", 95), ("Top Culprit", 140), ("Diagnosis", 90)]
        for name, width in cols:
            lbl = ctk.CTkLabel(header, text=name, font=ctk.CTkFont(size=11, weight="bold"), text_color=ThemeManager.get("text_muted"), width=width, anchor="w")
            lbl.pack(side="left", padx=5, pady=4)

        records = self.history_manager.get_db_history(limit=50)
        if not records:
            empty_lbl = ctk.CTkLabel(self.log_table_frame, text="No historical logs recorded yet. Telemetry writes every 60s.", font=ctk.CTkFont(size=12), text_color=ThemeManager.get("text_muted"))
            empty_lbl.pack(pady=20)
            return

        for idx, r in enumerate(records):
            row = ctk.CTkFrame(self.log_table_frame, fg_color="transparent" if idx % 2 == 0 else ThemeManager.get("bg_card_hover"), corner_radius=4)
            row.pack(fill="x", padx=4, pady=1)

            t_str = r.get("time_str", "")
            cpu_t = f"{r.get('cpu_temp', 0):.1f}°C"
            cpu_l = f"{r.get('cpu_load', 0):.1f}%"
            gpu_t = f"{r.get('gpu_temp', 0):.1f}°C"
            fan_num = r.get('fan_rpm', 0)
            fan_str = f"{fan_num} RPM" if fan_num > 0 else "Auto (EC)"
            culprit = f"{r.get('top_culprit', '')} ({r.get('top_has', 0):.0f}%)"
            diag = r.get("diag_status", "OPTIMAL")

            raw_cpu_temp = float(r.get("cpu_temp") or 0.0)
            if raw_cpu_temp < 72.0 and "HEAVY" in diag:
                diag = "OPTIMAL"

            if diag == "OPTIMAL":
                diag_color = "#10b981"
            elif "HEAVY" in diag:
                diag_color = "#eab308"
            elif "ELEVATED" in diag:
                diag_color = "#f97316"
            elif "OVERHEAT" in diag or "CRITICAL" in diag:
                diag_color = "#ef4444"
            else:
                diag_color = "#00e5ff"

            vals = [
                (t_str, 135, ThemeManager.get("text_secondary")),
                (cpu_t, 85, ThemeManager.get("text_primary")),
                (cpu_l, 85, ThemeManager.get("text_secondary")),
                (gpu_t, 85, ThemeManager.get("text_secondary")),
                (fan_str, 95, ThemeManager.get("text_secondary")),
                (culprit, 140, ThemeManager.get("text_primary")),
                (diag, 110, diag_color)
            ]

            for val, width, col in vals:
                lbl = ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=11), text_color=col, width=width, anchor="w")
                lbl.pack(side="left", padx=5, pady=3)

    def _on_export_json(self):
        from tkinter import filedialog
        desktop = os.path.expanduser("~/Desktop")
        export_path = filedialog.asksaveasfilename(
            title="Save Thermal Diagnostic Report",
            initialdir=desktop,
            initialfile="Thermal_Diagnostic_Report.json",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if export_path:
            success = self.history_manager.export_report_json(export_path)
            if success and self.on_toast:
                self.on_toast("Export Successful", f"Report saved to:\n{export_path}")

    def apply_theme(self):
        bg_card = ThemeManager.get("bg_card")
        border = ThemeManager.get("border")
        txt_p = ThemeManager.get("text_primary")

        self.meter_card.configure(fg_color=bg_card, border_color=border)
        self.log_table_frame.configure(fg_color=bg_card, border_color=border)
        self.lbl_meter_title.configure(text_color=txt_p)
        self.log_title.configure(text_color=txt_p)
        self.btn_export_json.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.btn_refresh_log.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.update_chart(force=True)
        self.refresh_log_table()