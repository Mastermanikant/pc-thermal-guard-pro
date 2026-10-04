"""
History & Multi-Metric Visual Telemetry Bar Chart View
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
        
        self.selected_metric = "cpu_temp"  # Options: 'cpu_temp', 'cpu_load', 'ram_pct', 'battery_pct'
        self._last_chart_draw = 0.0
        
        self._build_ui()

    def _build_ui(self):
        # 1. Top Section: 5 Multi-Metric Live Health Bar Cards
        self.cards_strip = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_strip.pack(fill="x", padx=10, pady=(0, 8))

        # 5 Mini Cards
        self.card_cpu_temp = self._create_mini_metric_card(self.cards_strip, "🔥 CPU TEMP", "0.0°C", "#00e5ff")
        self.card_gpu_temp = self._create_mini_metric_card(self.cards_strip, "🎮 GPU TEMP", "0.0°C", "#10b981")
        self.card_ram_pct = self._create_mini_metric_card(self.cards_strip, "💾 RAM USAGE", "0%", "#a855f7")
        self.card_cpu_load = self._create_mini_metric_card(self.cards_strip, "⚡ CPU LOAD", "0%", "#eab308")
        self.card_power = self._create_mini_metric_card(self.cards_strip, "🔋 POWER / BAT", "100%", "#38bdf8")

        # 2. Middle Section: Historical Bar Chart Header with Metric Selector Tabs
        self.chart_header = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_header.pack(fill="x", padx=10, pady=(4, 6))

        self.chart_title = ctk.CTkLabel(
            self.chart_header,
            text="📊 Historical Telemetry Bar Visualizer (Histogram)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.chart_title.pack(side="left")

        # Metric Selector Pill Buttons
        tabs_box = ctk.CTkFrame(self.chart_header, fg_color="transparent")
        tabs_box.pack(side="right")

        self.btn_tab_temp = self._create_tab_button(tabs_box, "🔥 Temp (°C)", "cpu_temp")
        self.btn_tab_load = self._create_tab_button(tabs_box, "⚡ CPU Load (%)", "cpu_load")
        self.btn_tab_ram = self._create_tab_button(tabs_box, "💾 RAM (%)", "ram_pct")
        self.btn_tab_bat = self._create_tab_button(tabs_box, "🔋 Battery (%)", "battery_pct")

        self._highlight_active_tab()

        # Canvas Container Card for Bar Chart
        self.canvas_card = ctk.CTkFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        self.canvas_card.pack(fill="x", padx=10, pady=(0, 8))

        self.chart_canvas = tk.Canvas(
            self.canvas_card,
            height=150,
            bg=ThemeManager.get("bg_card"),
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="both", expand=True, padx=12, pady=8)

        # 3. Bottom Section: 7-Day Rolling SQLite Telemetry Ledger
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
            height=140
        )
        self.log_table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.refresh_log_table()

    def _create_mini_metric_card(self, parent, title: str, init_val: str, accent_color: str):
        card = ctk.CTkFrame(
            parent,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=10,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        card.pack(side="left", fill="both", expand=True, padx=3)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=8, pady=6)

        lbl_t = ctk.CTkLabel(inner, text=title, font=ctk.CTkFont(size=9, weight="bold"), text_color=ThemeManager.get("text_muted"))
        lbl_t.pack(anchor="w")

        lbl_v = ctk.CTkLabel(inner, text=init_val, font=ctk.CTkFont(size=13, weight="bold"), text_color=accent_color)
        lbl_v.pack(anchor="w", pady=(1, 3))

        # Mini Progress Bar
        bar = ctk.CTkProgressBar(inner, height=4, corner_radius=2, progress_color=accent_color, fg_color="#1e293b")
        bar.pack(fill="x")
        bar.set(0.0)

        card.lbl_val = lbl_v
        card.bar = bar
        card.accent_color = accent_color
        return card

    def _create_tab_button(self, parent, text: str, metric_key: str):
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=ctk.CTkFont(size=10, weight="bold"),
            height=24,
            width=85,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color=ThemeManager.get("border"),
            text_color=ThemeManager.get("text_muted"),
            command=lambda: self._set_active_metric(metric_key)
        )
        btn.pack(side="left", padx=2)
        return btn

    def _set_active_metric(self, metric_key: str):
        self.selected_metric = metric_key
        self._highlight_active_tab()
        self.update_chart(force=True)

    def _highlight_active_tab(self):
        tabs = [
            (self.btn_tab_temp, "cpu_temp"),
            (self.btn_tab_load, "cpu_load"),
            (self.btn_tab_ram, "ram_pct"),
            (self.btn_tab_bat, "battery_pct")
        ]
        for btn, key in tabs:
            if key == self.selected_metric:
                btn.configure(fg_color="#0284c7", text_color="#ffffff", border_color="#00e5ff")
            else:
                btn.configure(fg_color="transparent", text_color=ThemeManager.get("text_muted"), border_color=ThemeManager.get("border"))

    def update_live_chart(self):
        """Alias for real-time live chart updates."""
        self.update_chart()

    def update_chart(self, force: bool = False):
        """Renders dynamic multi-metric vertical bar histogram with color gradients."""
        now = time.time()
        if not force and (now - self._last_chart_draw < 1.0):
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

        # 1. Update Mini Top Cards with Latest Telemetry
        if samples:
            latest = samples[-1]
            c_temp = latest.get("cpu_temp", 0.0)
            g_temp = latest.get("gpu_temp", 0.0)
            r_pct = latest.get("ram_pct", 0.0)
            c_load = latest.get("cpu_load", 0.0)
            c_pwr = latest.get("cpu_power", 0.0)
            bat_pct = latest.get("battery_pct")
            plugged = latest.get("power_plugged", True)

            self.card_cpu_temp.lbl_val.configure(text=f"{c_temp:.1f}°C")
            self.card_cpu_temp.bar.set(min(1.0, c_temp / 100.0))

            self.card_gpu_temp.lbl_val.configure(text=f"{g_temp:.1f}°C")
            self.card_gpu_temp.bar.set(min(1.0, g_temp / 100.0))

            self.card_ram_pct.lbl_val.configure(text=f"{r_pct:.0f}%")
            self.card_ram_pct.bar.set(min(1.0, r_pct / 100.0))

            self.card_cpu_load.lbl_val.configure(text=f"{c_load:.0f}% ({c_pwr:.1f}W)")
            self.card_cpu_load.bar.set(min(1.0, c_load / 100.0))

            if bat_pct is not None:
                state_str = "AC Plugged" if plugged else "Battery Discharging"
                self.card_power.lbl_val.configure(text=f"{bat_pct:.0f}% ({state_str})")
                self.card_power.bar.set(min(1.0, bat_pct / 100.0))
            else:
                fan_rpm = latest.get("fan_rpm", 0)
                fan_text = f"{fan_rpm} RPM" if fan_rpm > 0 else "AC Main (0 RPM)"
                self.card_power.lbl_val.configure(text=fan_text)
                self.card_power.bar.set(0.75)

        # 2. Scale & Guideline Coordinates
        def scale_to_y(val, max_scale=100.0):
            ratio = max(0.0, min(1.0, val / max_scale))
            return h - 22 - (ratio * (h - 40))

        # Max scale based on metric
        max_scale = 100.0
        unit = "%"
        if self.selected_metric == "cpu_temp":
            unit = "°C"
            max_scale = 100.0

        # Grid lines at 100%, 75%, 50%, 25%, 0%
        for pct_val, is_alert in [(100, False), (75, True), (50, False), (25, False), (0, False)]:
            y_pos = scale_to_y(pct_val, max_scale)
            dash_pattern = (4, 4) if is_alert else (1, 4)
            line_color = "#f97316" if is_alert else grid_col
            canvas.create_line(42, y_pos, w - 15, y_pos, fill=line_color, dash=dash_pattern, width=1)
            canvas.create_text(22, y_pos, text=f"{pct_val}{unit}", fill=line_color, font=("Segoe UI", 8))

        # Time Scale Axis
        y_bottom = h - 14
        canvas.create_line(42, y_bottom, w - 15, y_bottom, fill=grid_col, width=1)
        canvas.create_text(48, y_bottom + 8, text="-60m", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 8))
        canvas.create_text((w + 30) // 2, y_bottom + 8, text="-30m", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 8))
        canvas.create_text(w - 25, y_bottom + 8, text="Now", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 8, "bold"))

        if not samples:
            canvas.create_text(w / 2, h / 2, text="Sampling real-time hardware telemetry bars...", fill=ThemeManager.get("text_muted"), font=("Segoe UI", 11))
            return

        # 3. Draw Vertical Bars
        # Display last 35 to 45 samples as dense bars
        n_bars = min(len(samples), 40)
        recent_samples = samples[-n_bars:]

        usable_w = w - 65
        bar_width = max(6, (usable_w / max(1, n_bars)) - 3)

        for idx, s in enumerate(recent_samples):
            # Value extraction
            val = 0.0
            if self.selected_metric == "cpu_temp":
                val = float(s.get("cpu_temp", 24.0))
            elif self.selected_metric == "cpu_load":
                val = float(s.get("cpu_load", 0.0))
            elif self.selected_metric == "ram_pct":
                val = float(s.get("ram_pct", 0.0))
            elif self.selected_metric == "battery_pct":
                val = float(s.get("battery_pct") or 100.0)

            x0 = 46 + (idx * (bar_width + 3))
            x1 = x0 + bar_width
            y0 = scale_to_y(val, max_scale)
            y1 = scale_to_y(0.0, max_scale)

            # Intensity color gradient based on value
            if self.selected_metric == "cpu_temp":
                if val >= 80.0:
                    bar_color = "#ef4444"  # Critical Red
                elif val >= 68.0:
                    bar_color = "#f97316"  # Warm Orange
                elif val >= 55.0:
                    bar_color = "#eab308"  # Moderate Yellow
                else:
                    bar_color = "#00e5ff"  # Optimal Cyan
            else:
                if val >= 85.0:
                    bar_color = "#ef4444"
                elif val >= 70.0:
                    bar_color = "#f97316"
                elif val >= 45.0:
                    bar_color = "#eab308"
                else:
                    bar_color = "#10b981"

            # Draw bar rectangle
            canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline="", width=0)

            # If newest bar, draw glow cap & text value
            if idx == len(recent_samples) - 1:
                canvas.create_rectangle(x0 - 1, y0 - 2, x1 + 1, y0 + 2, fill="#ffffff", outline=bar_color, width=1)
                label_y = max(12, y0 - 10)
                canvas.create_text((x0 + x1) / 2, label_y, text=f"{val:.0f}{unit}", fill=bar_color, font=("Segoe UI", 9, "bold"))

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

            # Scientific Calibration: If CPU is cool (<72°C), it is nominal OPTIMAL
            raw_cpu_temp = float(r.get("cpu_temp") or 0.0)
            if raw_cpu_temp < 72.0 and "HEAVY" in diag:
                diag = "OPTIMAL"

            # Color mapping for scientific statuses
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

            vals = [(t_str, 135, ThemeManager.get("text_secondary")), (cpu_t, 85, ThemeManager.get("text_primary")), (cpu_l, 85, ThemeManager.get("text_secondary")), (gpu_t, 85, ThemeManager.get("text_secondary")), (fan_str, 95, ThemeManager.get("text_secondary")), (culprit, 140, ThemeManager.get("text_primary")), (diag, 110, diag_color)]

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

        self.canvas_card.configure(fg_color=bg_card, border_color=border)
        self.log_table_frame.configure(fg_color=bg_card, border_color=border)
        self.chart_title.configure(text_color=txt_p)
        self.log_title.configure(text_color=txt_p)
        self.btn_export_json.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.btn_refresh_log.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self._highlight_active_tab()
        self.update_chart(force=True)
        self.refresh_log_table()