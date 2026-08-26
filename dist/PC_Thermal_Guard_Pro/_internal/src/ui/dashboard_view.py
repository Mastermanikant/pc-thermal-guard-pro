"""
Dashboard View Component (100% Matched with FrankBase Smart File Organizer Architecture - Screenshots 2 & 3)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk
from typing import Dict, Any, List, Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.thermal_relief import ThermalReliefEngine
from src.ui.ecosystem_card import EcosystemBannerCard

class DashboardView(ctk.CTkScrollableFrame):
    def __init__(self, master, on_toast: Callable[[str, str], None] = None, on_cool_down_callback: Callable[[], None] = None, **kwargs):
        super().__init__(
            master,
            fg_color=BG_COLOR,
            corner_radius=0,
            scrollbar_button_color=("#cccccc", "#333333"),
            scrollbar_button_hover_color=NEON_CYAN,
            **kwargs
        )
        self.on_toast = on_toast
        self.on_cool_down_callback = on_cool_down_callback
        self.top_culprits_cache: List[Dict[str, Any]] = []
        self.stats_expanded = True
        self.culprit_rows = []

        self._build_ui()

    def _build_ui(self):
        # ── 1. Top Section: Global Thermal Stats & Preview (Expandable Card matching Screenshots 2 & 3) ──
        self.stats_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.stats_card.pack(fill="x", padx=10, pady=(10, 8))

        # Card Header
        stats_hdr = ctk.CTkFrame(self.stats_card, fg_color="transparent")
        stats_hdr.pack(fill="x", padx=15, pady=(10, 6))

        ctk.CTkLabel(
            stats_hdr,
            text="📊 Global Thermal Stats & Live Telemetry",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        self.btn_update_telemetry = ctk.CTkButton(
            stats_hdr,
            text="🔄 Live Active",
            width=100,
            height=26,
            corner_radius=6,
            fg_color=NEON_CYAN,
            text_color="black",
            hover_color=NEON_MAGENTA,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_update_telemetry.pack(side="right", padx=(6, 0))

        self.btn_toggle_stats = ctk.CTkButton(
            stats_hdr,
            text="▼ Minimize",
            width=90,
            height=26,
            corner_radius=6,
            fg_color="#333333",
            text_color="white",
            hover_color="#444444",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.toggle_stats_view
        )
        self.btn_toggle_stats.pack(side="right")

        # Stats Content Container (Collapsible)
        self.stats_content = ctk.CTkFrame(self.stats_card, fg_color="transparent")
        self.stats_content.pack(fill="x", padx=15, pady=(0, 12))

        # 4 Metric Cards Grid
        self.gauges_frame = ctk.CTkFrame(self.stats_content, fg_color="transparent")
        self.gauges_frame.pack(fill="x", pady=(2, 10))
        self.gauges_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="metric")

        self.card_cpu = self._create_metric_card(self.gauges_frame, 0, "CPU TEMPERATURE", "45.0°C", "Peak: 48.0°C", NEON_GREEN)
        self.card_gpu = self._create_metric_card(self.gauges_frame, 1, "GPU TEMPERATURE", "42.0°C", "Load: 0%", NEON_CYAN)
        self.card_fan = self._create_metric_card(self.gauges_frame, 2, "COOLING FAN", "1200 RPM", "Auto Speed", NEON_CYAN)
        self.card_power = self._create_metric_card(self.gauges_frame, 3, "CPU POWER & CLOCK", "15.0 W", "2400 MHz", DYNAMIC_GRAY)

        # ── 2. Diagnostic Hero Card (Matching Screenshot 1 & 2) ──
        self.hero_diag = ctk.CTkFrame(self.stats_content, fg_color=BG_COLOR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.hero_diag.pack(fill="x", pady=(0, 4))

        diag_hdr = ctk.CTkFrame(self.hero_diag, fg_color="transparent")
        diag_hdr.pack(fill="x", padx=12, pady=(10, 4))

        self.badge_status = ctk.CTkLabel(
            diag_hdr,
            text="OPTIMAL",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=NEON_GREEN,
            text_color="black",
            corner_radius=6,
            padx=10,
            pady=3
        )
        self.badge_status.pack(side="left")

        self.lbl_diag_title = ctk.CTkLabel(
            diag_hdr,
            text="✅ System Cool & Healthy",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.lbl_diag_title.pack(side="left", padx=10)

        # Master Magenta 1-Click Cool Down Button (Screenshots 1 & 2)
        self.btn_master_cool = ctk.CTkButton(
            diag_hdr,
            text="⚡ 1-Click Cool Down",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            corner_radius=8,
            height=32,
            command=self._on_master_cool_down
        )
        self.btn_master_cool.pack(side="right")

        self.lbl_diag_desc = ctk.CTkLabel(
            self.hero_diag,
            text="CPU temperature is at a safe 45°C. Cooling system is running smoothly with low background load.",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_COLOR,
            wraplength=700,
            justify="left",
            anchor="w"
        )
        self.lbl_diag_desc.pack(fill="x", padx=15, pady=(2, 2))

        self.lbl_diag_rec = ctk.CTkLabel(
            self.hero_diag,
            text="💡 Recommendation: No action required. Thermal Guard is actively monitoring in low-overhead mode.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color=DYNAMIC_GRAY,
            wraplength=700,
            justify="left",
            anchor="w"
        )
        self.lbl_diag_rec.pack(fill="x", padx=15, pady=(0, 10))

        # ── 3. Middle Section: Top Heat Culprit Applications (Real-Time Attribution) ──
        self.culprits_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.culprits_card.pack(fill="x", padx=10, pady=8)

        culprits_hdr = ctk.CTkFrame(self.culprits_card, fg_color="transparent")
        culprits_hdr.pack(fill="x", padx=15, pady=(12, 6))

        ctk.CTkLabel(
            culprits_hdr,
            text="🔥 Top Heat Culprit Applications (Real-Time Attribution)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        ctk.CTkLabel(
            culprits_hdr,
            text="Ranks running apps by their direct thermal contribution (HAS %)",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color=DYNAMIC_GRAY
        ).pack(side="right")

        self.rows_container = ctk.CTkFrame(self.culprits_card, fg_color="transparent")
        self.rows_container.pack(fill="x", padx=12, pady=(0, 12))

        # Pre-build 5 Culprit Rows
        for i in range(5):
            row = self._create_culprit_row(self.rows_container, i)
            self.culprit_rows.append(row)

        # ── 4. Bottom Section: Ecosystem Banner Card (100% Matched with Screenshots 2 & 3) ──
        self.ecosystem_banner = EcosystemBannerCard(self, on_toast_callback=self.on_toast)
        self.ecosystem_banner.pack(fill="x", padx=10, pady=(8, 15))

    def _create_metric_card(self, parent, col, title, value, sub, color):
        card = ctk.CTkFrame(parent, fg_color=BG_COLOR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        card.grid(row=0, column=col, padx=4, pady=2, sticky="nsew")

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color=DYNAMIC_GRAY)
        lbl_t.pack(anchor="w", padx=10, pady=(8, 2))

        lbl_v = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"), text_color=color)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 2))

        lbl_s = ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY)
        lbl_s.pack(anchor="w", padx=10, pady=(0, 8))

        return {"frame": card, "title": lbl_t, "val": lbl_v, "sub": lbl_s, "base_color": color}

    def _create_culprit_row(self, parent, index):
        frame = ctk.CTkFrame(parent, fg_color=BG_COLOR if index % 2 == 0 else "transparent", corner_radius=6)
        frame.pack(fill="x", pady=2)

        lbl_rank = ctk.CTkLabel(frame, text=f"#{index+1}", width=30, font=ctk.CTkFont(weight="bold", size=12), text_color=DYNAMIC_GRAY)
        lbl_rank.pack(side="left", padx=(8, 4))

        info_box = ctk.CTkFrame(frame, fg_color="transparent", width=170)
        info_box.pack(side="left", padx=4)
        info_box.pack_propagate(False)

        lbl_name = ctk.CTkLabel(info_box, text="System Task", font=ctk.CTkFont(weight="bold", size=12), text_color=TEXT_COLOR, anchor="w")
        lbl_name.pack(fill="x")
        lbl_desc = ctk.CTkLabel(info_box, text="Idle", font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY, anchor="w")
        lbl_desc.pack(fill="x")

        lbl_stats = ctk.CTkLabel(frame, text="CPU: 0.0% | 0 MB", width=130, font=ctk.CTkFont(size=11), text_color=TEXT_COLOR)
        lbl_stats.pack(side="left", padx=6)

        lbl_has = ctk.CTkLabel(frame, text="HAS: 0.0%", width=70, font=ctk.CTkFont(size=11, weight="bold"), text_color=NEON_CYAN)
        lbl_has.pack(side="left", padx=4)

        prog = ctk.CTkProgressBar(frame, height=10, corner_radius=5, fg_color="#333333", progress_color=NEON_GREEN)
        prog.pack(side="left", fill="x", expand=True, padx=8)
        prog.set(0.02)

        btn_relieve = ctk.CTkButton(
            frame,
            text="Relieve",
            width=70,
            height=26,
            corner_radius=5,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            hover_color=NEON_CYAN,
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda idx=index: self._on_relieve_process(idx)
        )
        btn_relieve.pack(side="right", padx=(4, 8))

        return {
            "frame": frame,
            "rank": lbl_rank,
            "name": lbl_name,
            "desc": lbl_desc,
            "stats": lbl_stats,
            "has": lbl_has,
            "progress": prog,
            "btn_relieve": btn_relieve,
            "pid": None
        }

    def toggle_stats_view(self):
        self.stats_expanded = not self.stats_expanded
        if self.stats_expanded:
            self.stats_content.pack(fill="x", padx=15, pady=(0, 12))
            self.btn_toggle_stats.configure(text="▼ Minimize")
        else:
            self.stats_content.pack_forget()
            self.btn_toggle_stats.configure(text="▶ Expand")

    def update_telemetry(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diagnostics: Dict[str, Any]):
        self.top_culprits_cache = culprits

        # 1. Update Metric Cards
        cpu_t = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 45.0
        max_t = telemetry.get("cpu_temp_max", cpu_t)
        cpu_l = telemetry.get("cpu_load", 0.0)
        gpu_t = telemetry.get("gpu_temp", 42.0)
        gpu_l = telemetry.get("gpu_load", 0.0)
        fan_rpm = telemetry.get("fan_rpm", 1200)
        pwr = telemetry.get("cpu_power", 15.0)
        freq = telemetry.get("cpu_freq_mhz", 2400.0)

        self.card_cpu["val"].configure(text=f"{cpu_t:.1f}°C")
        self.card_cpu["sub"].configure(text=f"Peak: {max_t:.1f}°C")

        if cpu_t >= 80.0:
            self.card_cpu["val"].configure(text_color="#FF0055")
        elif cpu_t >= 65.0:
            self.card_cpu["val"].configure(text_color="#FFA500")
        else:
            self.card_cpu["val"].configure(text_color=NEON_GREEN)

        self.card_gpu["val"].configure(text=f"{gpu_t:.1f}°C")
        self.card_gpu["sub"].configure(text=f"Load: {gpu_l:.0f}%")

        self.card_fan["val"].configure(text=f"{fan_rpm} RPM")
        self.card_power["val"].configure(text=f"{pwr:.1f} W")
        self.card_power["sub"].configure(text=f"{freq:.0f} MHz")

        # 2. Update Diagnostic Hero Card
        status = diagnostics.get("status", "OPTIMAL")
        headline = diagnostics.get("headline", "System Cool & Healthy")
        badge_col = diagnostics.get("badge_color", NEON_GREEN)

        self.badge_status.configure(text=status, fg_color=badge_col)
        self.lbl_diag_title.configure(text=headline)
        self.lbl_diag_desc.configure(text=diagnostics.get("explanation", ""))
        self.lbl_diag_rec.configure(text=diagnostics.get("recommendation", ""))

        # 3. Update Culprit Rows
        for i, row in enumerate(self.culprit_rows):
            if i < len(culprits):
                c = culprits[i]
                row["frame"].pack(fill="x", pady=2)
                row["name"].configure(text=c.get("name", "Process"))
                row["desc"].configure(text=c.get("description", ""))
                row["stats"].configure(text=f"CPU: {c.get('cpu_percent', 0.0):.1f}% | {c.get('memory_mb', 0):.0f} MB")

                score = c.get("heat_score", 0.0)
                row["has"].configure(text=f"HAS: {score:.1f}%")
                row["progress"].set(min(1.0, max(0.02, score / 100.0)))
                row["progress"].configure(progress_color=c.get("heat_color", NEON_GREEN))
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
        self.configure(fg_color=BG_COLOR)
        self.stats_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.hero_diag.configure(fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.culprits_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.lbl_diag_title.configure(text_color=TEXT_COLOR)
        self.lbl_diag_desc.configure(text_color=TEXT_COLOR)
        self.lbl_diag_rec.configure(text_color=DYNAMIC_GRAY)
        self.ecosystem_banner.refresh_theme()

    def refresh_theme(self):
        self.apply_theme()