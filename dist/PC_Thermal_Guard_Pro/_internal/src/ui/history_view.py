"""
History & Multi-Metric Visual Telemetry Live Cards View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
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
        self._last_draw_time = 0.0
        
        self._build_ui()

    def _build_ui(self):
        # ── 1. Top Section: 5 Multi-Metric Live Telemetry Cards Strip ──
        self.cards_strip = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_strip.pack(fill="x", padx=10, pady=(6, 12))

        # 5 Clean Metric Cards with generous padding and vibrant progress bars
        self.card_cpu_temp = self._create_mini_metric_card(self.cards_strip, "🔥 CPU TEMP", "0.0°C", "#00e5ff")
        self.card_gpu_temp = self._create_mini_metric_card(self.cards_strip, "🎮 GPU TEMP", "0.0°C", "#10b981")
        self.card_ram_pct = self._create_mini_metric_card(self.cards_strip, "💾 RAM USAGE", "0%", "#a855f7")
        self.card_cpu_load = self._create_mini_metric_card(self.cards_strip, "⚡ CPU LOAD", "0%", "#eab308")
        self.card_power = self._create_mini_metric_card(self.cards_strip, "🔋 POWER / BAT", "100%", "#38bdf8")

        # ── 2. Bottom Section: 7-Day Rolling SQLite Telemetry Ledger ──
        self.log_header = ctk.CTkFrame(self, fg_color="transparent")
        self.log_header.pack(fill="x", padx=10, pady=(4, 6))

        self.log_title = ctk.CTkLabel(
            self.log_header,
            text="📋 Rolling 7-Day Telemetry Incident Ledger (SQLite WAL)",
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
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color="#0284c7",
            text_color=ThemeManager.get("text_primary"),
            width=95,
            height=28,
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
            height=360
        )
        self.log_table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_log_table()
        self.update_live_chart()

    def _create_mini_metric_card(self, parent, title: str, init_val: str, accent_color: str):
        card = ctk.CTkFrame(
            parent,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=10,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        card.pack(side="left", fill="both", expand=True, padx=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_t = ctk.CTkLabel(inner, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color=ThemeManager.get("text_muted"))
        lbl_t.pack(anchor="w")

        lbl_v = ctk.CTkLabel(inner, text=init_val, font=ctk.CTkFont(size=16, weight="bold"), text_color=accent_color)
        lbl_v.pack(anchor="w", pady=(3, 6))

        # Mini Progress Bar
        bar = ctk.CTkProgressBar(inner, height=6, corner_radius=3, progress_color=accent_color, fg_color="#1e293b")
        bar.pack(fill="x")
        bar.set(0.0)

        card.lbl_val = lbl_v
        card.bar = bar
        card.accent_color = accent_color
        return card

    def update_live_chart(self):
        """Updates the 5 live metric progress cards with current telemetry."""
        now = time.time()
        if (now - self._last_draw_time < 0.4):
            return
        self._last_draw_time = now

        samples = self.history_manager.get_recent_ring_buffer()
        if not samples:
            return

        latest = samples[-1]
        c_temp = float(latest.get("cpu_temp", 24.0))
        g_temp = float(latest.get("gpu_temp", 22.0))
        r_pct = float(latest.get("ram_pct", 0.0))
        c_load = float(latest.get("cpu_load", 0.0))
        c_pwr = float(latest.get("cpu_power", 0.0))
        bat_pct = latest.get("battery_pct")
        plugged = latest.get("power_plugged", True)

        self.card_cpu_temp.lbl_val.configure(text=f"{c_temp:.1f}°C")
        self.card_cpu_temp.bar.set(min(1.0, max(0.02, c_temp / 100.0)))

        self.card_gpu_temp.lbl_val.configure(text=f"{g_temp:.1f}°C")
        self.card_gpu_temp.bar.set(min(1.0, max(0.02, g_temp / 100.0)))

        self.card_ram_pct.lbl_val.configure(text=f"{r_pct:.0f}%")
        self.card_ram_pct.bar.set(min(1.0, max(0.02, r_pct / 100.0)))

        self.card_cpu_load.lbl_val.configure(text=f"{c_load:.0f}% ({c_pwr:.1f}W)")
        self.card_cpu_load.bar.set(min(1.0, max(0.02, c_load / 100.0)))

        if bat_pct is not None:
            state_str = "AC Plugged" if plugged else "Battery"
            self.card_power.lbl_val.configure(text=f"{bat_pct:.0f}% ({state_str})")
            self.card_power.bar.set(min(1.0, max(0.02, bat_pct / 100.0)))
        else:
            fan_rpm = latest.get("fan_rpm", 0)
            fan_text = f"{fan_rpm} RPM" if fan_rpm > 0 else "AC Main (0 RPM)"
            self.card_power.lbl_val.configure(text=fan_text)
            self.card_power.bar.set(0.75)

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

        records = self.history_manager.get_db_history(limit=60)
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

        self.log_table_frame.configure(fg_color=bg_card, border_color=border)
        self.log_title.configure(text_color=txt_p)
        self.btn_export_json.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.btn_refresh_log.configure(fg_color=ThemeManager.get("bg_card_hover"), text_color=txt_p)
        self.update_live_chart()
        self.refresh_log_table()