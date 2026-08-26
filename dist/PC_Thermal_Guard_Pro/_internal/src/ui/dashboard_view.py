"""
Dashboard View Component
PC Thermal Guard Pro

Displays:
- Real-time Thermal Gauges (CPU, GPU, Fan, Power)
- System Thermal Health & Plain-Language Diagnostics
- Top Heat Culprits with Heat Attribution Score (HAS %) & 1-Click Relief
"""
import customtkinter as ctk
from typing import Dict, Any, List, Callable
from src.ui.theme import ThemeManager
from src.core.thermal_relief import ThermalReliefEngine

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_toast: Callable[[str, str], None] = None, on_cool_down_callback: Callable[[], None] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_toast = on_toast
        self.on_cool_down_callback = on_cool_down_callback
        self.top_culprits_cache: List[Dict[str, Any]] = []
        
        self._build_ui()

    def _build_ui(self):
        # 1. Top Section: Thermal Gauge Grid
        self.gauges_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.gauges_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.gauges_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="gauge")

        # CPU Temp Gauge Card
        self.card_cpu = self._create_metric_card(
            self.gauges_frame, 0, "CPU TEMPERATURE", "45.0°C", "Peak: 48.0°C", "#10b981"
        )
        # GPU Temp Gauge Card
        self.card_gpu = self._create_metric_card(
            self.gauges_frame, 1, "GPU TEMPERATURE", "42.0°C", "Load: 0%", "#38bdf8"
        )
        # Fan Speed Gauge Card
        self.card_fan = self._create_metric_card(
            self.gauges_frame, 2, "COOLING FAN", "1200 RPM", "Auto Speed", "#38bdf8"
        )
        # CPU Power Gauge Card
        self.card_power = self._create_metric_card(
            self.gauges_frame, 3, "CPU POWER & CLOCK", "15.0 W", "2400 MHz", "#94a3b8"
        )

        # 2. Middle Section: Plain-Language Diagnostic Hero Card
        self.hero_diag_frame = ctk.CTkFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        self.hero_diag_frame.pack(fill="x", padx=10, pady=5)

        self.diag_header_frame = ctk.CTkFrame(self.hero_diag_frame, fg_color="transparent")
        self.diag_header_frame.pack(fill="x", padx=15, pady=(12, 4))

        self.diag_badge = ctk.CTkLabel(
            self.diag_header_frame,
            text="OPTIMAL",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#10b981",
            text_color="#ffffff",
            corner_radius=6,
            padx=8,
            pady=2
        )
        self.diag_badge.pack(side="left")

        self.diag_title = ctk.CTkLabel(
            self.diag_header_frame,
            text="✅ System Cool & Healthy",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.diag_title.pack(side="left", padx=10)

        # Master 1-Click Cool Down Button
        self.btn_cool_down = ctk.CTkButton(
            self.diag_header_frame,
            text="⚡ 1-Click Cool Down",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            text_color="#ffffff",
            corner_radius=8,
            height=30,
            command=self._on_master_cool_down
        )
        self.btn_cool_down.pack(side="right")

        self.diag_explanation = ctk.CTkLabel(
            self.hero_diag_frame,
            text="CPU temperature is at a safe 45°C. Cooling system is running smoothly with low background load.",
            font=ctk.CTkFont(size=13),
            text_color=ThemeManager.get("text_secondary"),
            wraplength=650,
            justify="left"
        )
        self.diag_explanation.pack(fill="x", padx=15, pady=(2, 4), anchor="w")

        self.diag_recommendation = ctk.CTkLabel(
            self.hero_diag_frame,
            text="💡 Recommendation: No action required. Thermal Guard is actively monitoring in low-overhead mode.",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=ThemeManager.get("text_muted"),
            wraplength=650,
            justify="left"
        )
        self.diag_recommendation.pack(fill="x", padx=15, pady=(0, 12), anchor="w")

        # 3. Bottom Section: Top Heat Culprits List
        self.culprits_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.culprits_header_frame.pack(fill="x", padx=10, pady=(15, 6))

        self.culprits_title = ctk.CTkLabel(
            self.culprits_header_frame,
            text="🔥 Top Heat Culprit Applications (Real-Time Attribution)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ThemeManager.get("text_primary")
        )
        self.culprits_title.pack(side="left")

        self.culprits_sub = ctk.CTkLabel(
            self.culprits_header_frame,
            text="Ranks running apps by their direct thermal contribution (HAS %)",
            font=ctk.CTkFont(size=11),
            text_color=ThemeManager.get("text_muted")
        )
        self.culprits_sub.pack(side="right")

        self.culprits_container = ctk.CTkFrame(
            self,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=12,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        self.culprits_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.culprit_rows = []
        for i in range(5):
            row = self._create_culprit_row(self.culprits_container, i)
            self.culprit_rows.append(row)

    def _create_metric_card(self, parent, col, title, value, subtext, val_color):
        card = ctk.CTkFrame(
            parent,
            fg_color=ThemeManager.get("bg_card"),
            corner_radius=10,
            border_width=1,
            border_color=ThemeManager.get("border")
        )
        card.grid(row=0, column=col, padx=5, pady=0, sticky="nsew")

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ThemeManager.get("text_muted")
        )
        lbl_title.pack(padx=10, pady=(8, 0), anchor="w")

        lbl_val = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=val_color
        )
        lbl_val.pack(padx=10, pady=(0, 0), anchor="w")

        lbl_sub = ctk.CTkLabel(
            card,
            text=subtext,
            font=ctk.CTkFont(size=11),
            text_color=ThemeManager.get("text_secondary")
        )
        lbl_sub.pack(padx=10, pady=(0, 8), anchor="w")

        return {
            "frame": card,
            "title": lbl_title,
            "value": lbl_val,
            "sub": lbl_sub
        }

    def _create_culprit_row(self, parent, index):
        row_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent" if index % 2 == 0 else ThemeManager.get("bg_card_hover"),
            corner_radius=6
        )
        row_frame.pack(fill="x", padx=10, pady=4)

        # Process Rank & Name
        lbl_rank = ctk.CTkLabel(
            row_frame,
            text=f"#{index + 1}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ThemeManager.get("text_muted"),
            width=24
        )
        lbl_rank.pack(side="left", padx=(6, 4))

        info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        info_frame.pack(side="left", padx=4, fill="y")

        lbl_name = ctk.CTkLabel(
            info_frame,
            text="System Process",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ThemeManager.get("text_primary"),
            anchor="w",
            width=180
        )
        lbl_name.pack(anchor="w")

        lbl_desc = ctk.CTkLabel(
            info_frame,
            text="System Task",
            font=ctk.CTkFont(size=10),
            text_color=ThemeManager.get("text_muted"),
            anchor="w",
            width=180
        )
        lbl_desc.pack(anchor="w")

        # CPU & Memory
        lbl_stats = ctk.CTkLabel(
            row_frame,
            text="CPU: 0.0% | 0 MB",
            font=ctk.CTkFont(size=11),
            text_color=ThemeManager.get("text_secondary"),
            width=130
        )
        lbl_stats.pack(side="left", padx=6)

        # Progress Bar for Heat Attribution Score
        bar_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        bar_frame.pack(side="left", fill="x", expand=True, padx=8)

        bar_label = ctk.CTkLabel(
            bar_frame,
            text="HAS: 0.0%",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ThemeManager.get("text_muted"),
            width=65,
            anchor="w"
        )
        bar_label.pack(side="left", padx=(0, 4))

        progress = ctk.CTkProgressBar(
            bar_frame,
            height=10,
            corner_radius=5,
            fg_color=ThemeManager.get("gauge_bg"),
            progress_color="#10b981"
        )
        progress.set(0.1)
        progress.pack(side="left", fill="x", expand=True)

        # 1-Click Relieve Button
        btn_relieve = ctk.CTkButton(
            row_frame,
            text="Relieve",
            font=ctk.CTkFont(size=11),
            fg_color=ThemeManager.get("bg_card_hover"),
            hover_color=ThemeManager.get("accent"),
            text_color=ThemeManager.get("text_primary"),
            width=65,
            height=26,
            corner_radius=6,
            command=lambda idx=index: self._on_relieve_process(idx)
        )
        btn_relieve.pack(side="right", padx=(4, 6))

        return {
            "frame": row_frame,
            "rank": lbl_rank,
            "name": lbl_name,
            "desc": lbl_desc,
            "stats": lbl_stats,
            "has_label": bar_label,
            "progress": progress,
            "btn_relieve": btn_relieve,
            "pid": None
        }

    def update_telemetry(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diag: Dict[str, Any]):
        self.top_culprits_cache = culprits

        # 1. Update Gauge Cards
        cpu_t = telemetry.get("cpu_temp", 45.0)
        cpu_max = telemetry.get("cpu_temp_max", cpu_t)
        cpu_load = telemetry.get("cpu_load", 0.0)
        cpu_pow = telemetry.get("cpu_power", 15.0)
        cpu_freq = telemetry.get("cpu_freq_mhz", 2400.0)

        gpu_t = telemetry.get("gpu_temp", 42.0)
        gpu_load = telemetry.get("gpu_load", 0.0)
        fan_rpm = telemetry.get("fan_rpm", 1200)

        # Color-coded CPU Temp
        if cpu_t >= 85.0:
            cpu_color = ThemeManager.get("danger")
        elif cpu_t >= 70.0:
            cpu_color = ThemeManager.get("caution")
        elif cpu_t >= 60.0:
            cpu_color = ThemeManager.get("warning")
        else:
            cpu_color = ThemeManager.get("success")

        self.card_cpu["value"].configure(text=f"{cpu_t:.1f}°C", text_color=cpu_color)
        self.card_cpu["sub"].configure(text=f"Peak: {cpu_max:.1f}°C | Load: {cpu_load:.1f}%")

        self.card_gpu["value"].configure(text=f"{gpu_t:.1f}°C")
        self.card_gpu["sub"].configure(text=f"Load: {gpu_load:.1f}%")

        self.card_fan["value"].configure(text=f"{fan_rpm} RPM")
        self.card_fan["sub"].configure(text="Auto Speed" if fan_rpm > 0 else "OFF / 0 RPM")

        self.card_power["value"].configure(text=f"{cpu_pow:.1f} W")
        self.card_power["sub"].configure(text=f"{int(cpu_freq)} MHz")

        # 2. Update Diagnostic Hero Card
        status = diag.get("status", "OPTIMAL")
        badge_col = diag.get("badge_color", "#10b981")
        headline = diag.get("headline", "System Cool")
        explanation = diag.get("explanation", "")
        recommendation = diag.get("recommendation", "")

        self.diag_badge.configure(text=status, fg_color=badge_col)
        self.diag_title.configure(text=headline)
        self.diag_explanation.configure(text=explanation)
        self.diag_recommendation.configure(text=f"💡 Recommendation: {recommendation}")

        # 3. Update Top Culprits
        for i, row in enumerate(self.culprit_rows):
            if i < len(culprits):
                c = culprits[i]
                row["frame"].pack(fill="x", padx=10, pady=3)
                row["name"].configure(text=c.get("name", "Process"))
                row["desc"].configure(text=c.get("description", ""))
                row["stats"].configure(text=f"CPU: {c.get('cpu_percent', 0.0):.1f}% | {c.get('memory_mb', 0):.0f} MB")
                
                score = c.get("heat_score", 0.0)
                row["has_label"].configure(text=f"HAS: {score:.1f}%")
                row["progress"].set(min(1.0, max(0.02, score / 100.0)))
                row["progress"].configure(progress_color=c.get("heat_color", "#10b981"))
                row["pid"] = c.get("pid")
            else:
                row["frame"].pack_forget()

    def _on_relieve_process(self, index: int):
        if index < len(self.top_culprits_cache):
            item = self.top_culprits_cache[index]
            pid = item.get("pid")
            if pid:
                res = ThermalReliefEngine.throttle_process(pid)
                if self.on_toast:
                    self.on_toast("Thermal Relief", res["message"])

    def _on_master_cool_down(self):
        res = ThermalReliefEngine.one_click_cool_down(self.top_culprits_cache)
        if self.on_toast:
            self.on_toast("1-Click Cool Down", res["message"])

    def apply_theme(self):
        bg_card = ThemeManager.get("bg_card")
        border = ThemeManager.get("border")
        txt_p = ThemeManager.get("text_primary")
        txt_s = ThemeManager.get("text_secondary")
        txt_m = ThemeManager.get("text_muted")

        self.hero_diag_frame.configure(fg_color=bg_card, border_color=border)
        self.culprits_container.configure(fg_color=bg_card, border_color=border)
        self.diag_title.configure(text_color=txt_p)
        self.diag_explanation.configure(text_color=txt_s)
        self.diag_recommendation.configure(text_color=txt_m)
        self.culprits_title.configure(text_color=txt_p)
        self.culprits_sub.configure(text_color=txt_m)

        for card in [self.card_cpu, self.card_gpu, self.card_fan, self.card_power]:
            card["frame"].configure(fg_color=bg_card, border_color=border)
            card["title"].configure(text_color=txt_m)
            card["sub"].configure(text_color=txt_s)

        for i, row in enumerate(self.culprit_rows):
            row["frame"].configure(fg_color="transparent" if i % 2 == 0 else ThemeManager.get("bg_card_hover"))
            row["rank"].configure(text_color=txt_m)
            row["name"].configure(text_color=txt_p)
            row["desc"].configure(text_color=txt_m)
            row["stats"].configure(text_color=txt_s)
            row["progress"].configure(fg_color=ThemeManager.get("gauge_bg"))
            row["btn_relieve"].configure(
                fg_color=ThemeManager.get("bg_card_hover"),
                text_color=txt_p
            )