"""
History & Visual Telemetry Timeline View
PC Thermal Guard Pro

Displays:
- Real-time 60-minute visual scrubbing temperature graph
- 7-Day Overheat Event Log Table
- Diagnostic Report Export Actions (JSON / CSV)
"""
import tkinter as tk
import customtkinter as ctk
import time
import os
from typing import Dict, Any, List, Callable
from src.ui.theme import ThemeManager
from src.core.history_manager import HistoryManager

class HistoryView(ctk.CTkFrame):
    def __init__(self, master, history_manager: HistoryManager, on_toast: Callable[[str, str], None] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.history_manager = history_manager
        self.on_toast = on_toast
        
        self._build_ui()

    def _build_ui(self):
        # 1. Top Section: 60-Min Visual Telemetry Chart Header
        self.chart_header = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_header.pack(fill="x", padx=10, pady=(0, 6))

        self._last_chart_draw = 0.0

        self.chart_title = ctk.CTkLabel(
            self.chart_header,
            text="📈 Live 60-Minute Thermal Timeline",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.chart_title.pack(side="left")

        # High-Contrast Colored Legend Badges
        legend_box = ctk.CTkFrame(self.chart_header, fg_color="transparent")
        legend_box.pack(side="right")

        ctk.CTkLabel(legend_box, text="🟦 CPU Temp (°C)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#00e5ff").pack(side="left", padx=4)
        ctk.CTkLabel(legend_box, text="|", font=ctk.CTkFont(size=11), text_color="#555555").pack(side="left", padx=2)
        ctk.CTkLabel(legend_box, text="🟨 CPU Load (%)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#eab308").pack(side="left", padx=4)
        ctk.CTkLabel(legend_box, text="|", font=ctk.CTkFont(size=11), text_color="#555555").pack(side="left", padx=2)
        ctk.CTkLabel(legend_box, text="🟧 70°C Limit", font=ctk.CTkFont(size=10), text_color="#f97316").pack(side="left", padx=4)
        ctk.CTkLabel(legend_box, text="|", font=ctk.CTkFont(size=11), text_color="#555555").pack(side="left", padx=2)
        ctk.CTkLabel(legend_box, text="🟥 85°C Overheat", font=ctk.CTkFont(size=10), text_color="#ef4444").pack(side="left", padx=4)

        # Native Visual Canvas for Chart (High-speed, zero VRAM)
        self.canvas_card = ctk.CTkFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        self.canvas_card.pack(fill="x", padx=10, pady=(0, 10))

        self.chart_canvas = tk.Canvas(
            self.canvas_card,
            height=160,
            bg=ThemeManager.get("bg_card"),
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="both", expand=True, padx=12, pady=10)

        # 2. Bottom Section: 7-Day Overheat Events & Incident Log Table
        self.log_header = ctk.CTkFrame(self, fg_color="transparent")
        self.log_header.pack(fill="x", padx=10, pady=(10, 6))

        self.log_title = ctk.CTkLabel(
            self.log_header,
            text="📋 Rolling 7-Day Hardware Telemetry Ledger (SQLite WAL)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.log_title.pack(side="left")

        # Action Buttons
        self.actions_frame = ctk.CTkFrame(self.log_header, fg_color="transparent")
        self.actions_frame.pack(side="right")

        self.btn_export_json = ctk.CTkButton(
            self.actions_frame,
            text="💾 Export JSON",
            font=ctk.CTkFont(size=11),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color=ThemeManager.get("accent"),
            text_color=ThemeManager.get("text_primary"),
            width=100,
            height=28,
            corner_radius=6,
            command=self._on_export_json
        )
        self.btn_export_json.pack(side="left", padx=4)

        self.btn_refresh_log = ctk.CTkButton(
            self.actions_frame,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=11),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color=ThemeManager.get("accent"),
            text_color=ThemeManager.get("text_primary"),
            width=80,
            height=28,
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
            height=180
        )
        self.log_table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_log_table()

    def update_live_chart(self):
        """Alias for real-time live chart updates."""
        self.update_chart()

    def update_chart(self):
        """Draws real-time temperature curve onto canvas with 1-second rate limiting to prevent UI lockup."""
        now = time.time()
        if now - self._last_chart_draw < 1.0:
            return
        self._last_chart_draw = now

        samples = self.history_manager.get_recent_ring_buffer()
        canvas = self.chart_canvas
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w < 50 or h < 50:
            return

        canvas.delete("all")
        bg_card = ThemeManager.get("bg_card")
        grid_col = ThemeManager.get("border")
        canvas.configure(bg=bg_card)

        # Draw Grid Lines & Thresholds
        # 100°C (top = 10px), 85°C, 70°C, 50°C, 30°C (bottom = h - 20px)
        t_max = 100.0
        t_min = 30.0

        def temp_to_y(temp):
            ratio = max(0.0, min(1.0, (temp - t_min) / (t_max - t_min)))
            return h - 20 - (ratio * (h - 35))

        # Threshold line 85°C (Overheat Alert)
        y85 = temp_to_y(85.0)
        canvas.create_line(40, y85, w - 10, y85, fill="#ef4444", dash=(4, 4), width=1)
        canvas.create_text(25, y85, text="85°C", fill="#ef4444", font=("Segoe UI", 9))

        # Threshold line 70°C (Caution)
        y70 = temp_to_y(70.0)
        canvas.create_line(40, y70, w - 10, y70, fill="#f97316", dash=(2, 4), width=1)
        canvas.create_text(25, y70, text="70°C", fill="#f97316", font=("Segoe UI", 9))

        # Baseline 40°C
        y40 = temp_to_y(40.0)
        canvas.create_line(40, y40, w - 10, y40, fill=grid_col, dash=(1, 5), width=1)
        canvas.create_text(25, y40, text="40°C", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 9))

        if not samples:
            canvas.create_text(w / 2, h / 2, text="Sampling real-time telemetry...", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 11))
            return

        # Take last 60 samples or scale
        n_samples = min(len(samples), 60)
        recent = samples[-n_samples:]
        step_x = (w - 60) / max(1, n_samples - 1)

        # Plot CPU Temp Line
        points_temp = []
        points_load = []

        for idx, s in enumerate(recent):
            x = 45 + (idx * step_x)
            yt = temp_to_y(s.get("cpu_temp", 45.0))
            points_temp.append((x, yt))

            # CPU Load mapped to 0-100%
            load = s.get("cpu_load", 0.0)
            yl = h - 20 - ((load / 100.0) * (h - 35))
            points_load.append((x, yl))

        # Draw CPU Load line (Yellow)
        if len(points_load) > 1:
            flat_load = [coord for pt in points_load for coord in pt]
            canvas.create_line(flat_load, fill="#eab308", width=1, smooth=True)

        # Draw CPU Temp line (Sky Blue)
        if len(points_temp) > 1:
            flat_temp = [coord for pt in points_temp for coord in pt]
            canvas.create_line(flat_temp, fill=ThemeManager.get("chart_line"), width=2, smooth=True)

        # Latest Temp Badge on last point
        last_x, last_y = points_temp[-1]
        last_temp = recent[-1].get("cpu_temp", 45.0)
        canvas.create_oval(last_x - 4, last_y - 4, last_x + 4, last_y + 4, fill=ThemeManager.get("chart_line"), outline="#ffffff")
        canvas.create_text(last_x, last_y - 12, text=f"{last_temp:.1f}°C", fill=ThemeManager.get("text_primary"), font=("Segoe UI", 10, "bold"))

    def refresh_log_table(self):
        """Refreshes the SQLite telemetry table."""
        for widget in self.log_table_frame.winfo_children():
            widget.destroy()

        # Table Header
        header = ctk.CTkFrame(self.log_table_frame, fg_color=ThemeManager.get("bg_card_hover"), corner_radius=6)
        header.pack(fill="x", padx=4, pady=(2, 4))

        cols = [("Time", 140), ("CPU Temp", 90), ("CPU Load", 90), ("GPU Temp", 90), ("Fan RPM", 90), ("Top Culprit", 140), ("Diagnosis", 100)]
        for name, width in cols:
            lbl = ctk.CTkLabel(header, text=name, font=ctk.CTkFont(size=11, weight="bold"), text_color=ThemeManager.get("text_muted"), width=width, anchor="w")
            lbl.pack(side="left", padx=6, pady=4)

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
            fan = f"{r.get('fan_rpm', 0)} RPM"
            culprit = f"{r.get('top_culprit', '')} ({r.get('top_has', 0):.0f}%)"
            diag = r.get("diag_status", "OPTIMAL")

            # Color for status
            diag_color = "#10b981" if diag == "OPTIMAL" else ("#ef4444" if diag == "CRITICAL" else "#f97316")

            vals = [(t_str, 140, ThemeManager.get("text_secondary")), (cpu_t, 90, ThemeManager.get("text_primary")), (cpu_l, 90, ThemeManager.get("text_secondary")), (gpu_t, 90, ThemeManager.get("text_secondary")), (fan, 90, ThemeManager.get("text_secondary")), (culprit, 140, ThemeManager.get("text_primary")), (diag, 100, diag_color)]

            for val, width, col in vals:
                lbl = ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=11), text_color=col, width=width, anchor="w")
                lbl.pack(side="left", padx=6, pady=3)

    def _on_export_json(self):
        export_path = os.path.abspath("D:/02_Desktop_and_Mobile_Apps/PC_Thermal_Guard_Pro/Thermal_Diagnostic_Report.json")
        success = self.history_manager.export_report_json(export_path)
        if success and self.on_toast:
            self.on_toast("Export Successful", f"Report saved to:\n{export_path}")

    def apply_theme(self):
        bg_card = ThemeManager.get("bg_card")
        border = ThemeManager.get("border")
        txt_p = ThemeManager.get("text_primary")

        self.canvas_card.configure(fg_color=bg_card, border_color=border)
        self.log_table_frame.configure(fg_color=bg_card, border_color=border)
        self.chart_title.configure(text_color=txt_p)
        self.log_title.configure(text_color=txt_p)
        self.btn_export_json.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.btn_refresh_log.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.update_chart()
        self.refresh_log_table()