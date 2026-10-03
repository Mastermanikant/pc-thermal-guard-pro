"""
Dashboard View Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import time
import customtkinter as ctk
from typing import Dict, Any, List, Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.thermal_relief import ThermalReliefEngine, purge_all_background_ram
from src.core.hardware_sensor import restart_as_admin, is_admin

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
        self.culprit_rows = []
        self.is_elevated = is_admin()
        self.cooling_mode_var = ctk.StringVar(value="⚡ Balanced (Recommended)")

        self._build_ui()

    def _build_ui(self):
        # ── 1. Top Section: 3 High-Precision Live Metric Cards ──
        self.stats_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.stats_card.pack(fill="x", padx=10, pady=(10, 8))

        stats_hdr = ctk.CTkFrame(self.stats_card, fg_color="transparent")
        stats_hdr.pack(fill="x", padx=15, pady=(10, 6))

        ctk.CTkLabel(
            stats_hdr,
            text="📊 Live System Hardware Telemetry",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        if not self.is_elevated:
            self.btn_admin_badge = ctk.CTkButton(
                stats_hdr,
                text="🛡️ Run as Admin (Direct Sensors)",
                height=26,
                corner_radius=6,
                fg_color="#880e4f",
                hover_color=NEON_MAGENTA,
                text_color="white",
                font=ctk.CTkFont(size=10, weight="bold"),
                command=self._on_elevate_admin
            )
            self.btn_admin_badge.pack(side="right")
        else:
            self.btn_admin_badge = ctk.CTkLabel(
                stats_hdr,
                text="⚡ Direct Silicon Sensors Active",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=NEON_GREEN
            )
            self.btn_admin_badge.pack(side="right")

        # 3 Primary Telemetry Cards Grid
        self.gauges_frame = ctk.CTkFrame(self.stats_card, fg_color="transparent")
        self.gauges_frame.pack(fill="x", padx=15, pady=(0, 12))
        self.gauges_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="metric")

        self.card_cpu = self._create_metric_card(self.gauges_frame, 0, "CPU TEMPERATURE", "24.0°C", "Peak: 26.0°C", NEON_GREEN)
        self.card_gpu = self._create_metric_card(self.gauges_frame, 1, "GPU TEMPERATURE", "22.0°C", "Load: 0%", NEON_CYAN)
        self.card_ram = self._create_metric_card(self.gauges_frame, 2, "SYSTEM RAM USAGE", "0.0 GB (0%)", "Total: 16.0 GB", NEON_CYAN)

        # <!-- ================= Section: Diagnostic & Adaptive Relief ================= -->
        self.hero_diag = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.hero_diag.pack(fill="x", padx=10, pady=8)

        diag_hdr = ctk.CTkFrame(self.hero_diag, fg_color="transparent")
        diag_hdr.pack(fill="x", padx=15, pady=(12, 4))

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

        self.lbl_diag_desc = ctk.CTkLabel(
            self.hero_diag,
            text="CPU temperature is normal. Background process load is light and active multitasking is smooth.",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_COLOR,
            wraplength=720,
            justify="left",
            anchor="w"
        )
        self.lbl_diag_desc.pack(fill="x", padx=15, pady=(2, 10))

        # <!-- ================= Section: 1-Click Action Buttons ================= -->
        btn_box = ctk.CTkFrame(self.hero_diag, fg_color="transparent")
        btn_box.pack(fill="x", padx=15, pady=(0, 14))

        self.btn_master_cool = ctk.CTkButton(
            btn_box,
            text="❄️ Smart Cool Down (Auto-Adaptive Relief)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            corner_radius=8,
            height=38,
            command=self._on_master_cool_down
        )
        self.btn_master_cool.pack(side="left", padx=(0, 10), fill="x", expand=True)

        self.btn_quick_ram = ctk.CTkButton(
            btn_box,
            text="🧹 Free Unused RAM",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NEON_CYAN,
            hover_color="#00b0ff",
            text_color="black",
            corner_radius=8,
            height=38,
            command=self._on_quick_ram_flush
        )
        self.btn_quick_ram.pack(side="left", fill="x", expand=True)

        # ── 3. Bottom Section: Top Background CPU Consumers ──
        self.culprits_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.culprits_card.pack(fill="x", padx=10, pady=(0, 15))

        culprits_hdr = ctk.CTkFrame(self.culprits_card, fg_color="transparent")
        culprits_hdr.pack(fill="x", padx=15, pady=(12, 6))

        ctk.CTkLabel(
            culprits_hdr,
            text="🔥 Top Background CPU Consumers",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        ctk.CTkLabel(
            culprits_hdr,
            text="Active window is always protected",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color=DYNAMIC_GRAY
        ).pack(side="right")

        self.rows_container = ctk.CTkFrame(self.culprits_card, fg_color="transparent")
        self.rows_container.pack(fill="x", padx=12, pady=(0, 12))

        # Pre-build 4 Clean Culprit Rows
        for i in range(4):
            row = self._create_culprit_row(self.rows_container, i)
            self.culprit_rows.append(row)

    def _create_metric_card(self, parent, col, title, value, sub, color):
        card = ctk.CTkFrame(parent, fg_color=BG_COLOR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        card.grid(row=0, column=col, padx=4, pady=2, sticky="nsew")

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color=DYNAMIC_GRAY)
        lbl_t.pack(anchor="w", padx=12, pady=(8, 2))

        lbl_v = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"), text_color=color)
        lbl_v.pack(anchor="w", padx=12, pady=(0, 2))

        lbl_s = ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY)
        lbl_s.pack(anchor="w", padx=12, pady=(0, 8))

        return {"frame": card, "title": lbl_t, "val": lbl_v, "sub": lbl_s, "base_color": color}

    def _create_culprit_row(self, parent, index):
        frame = ctk.CTkFrame(parent, fg_color=BG_COLOR if index % 2 == 0 else "transparent", corner_radius=6)
        frame.pack(fill="x", pady=2)

        lbl_rank = ctk.CTkLabel(frame, text=f"#{index+1}", width=28, font=ctk.CTkFont(weight="bold", size=11), text_color=DYNAMIC_GRAY)
        lbl_rank.pack(side="left", padx=(8, 2))

        info_box = ctk.CTkFrame(frame, fg_color="transparent", width=160)
        info_box.pack(side="left", padx=4)
        info_box.pack_propagate(False)

        lbl_name = ctk.CTkLabel(info_box, text="System Process", font=ctk.CTkFont(weight="bold", size=12), text_color=TEXT_COLOR, anchor="w")
        lbl_name.pack(fill="x")
        lbl_desc = ctk.CTkLabel(info_box, text="Idle", font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY, anchor="w")
        lbl_desc.pack(fill="x")

        lbl_stats = ctk.CTkLabel(frame, text="CPU: 0.0% | 0 MB", width=120, font=ctk.CTkFont(size=11), text_color=TEXT_COLOR)
        lbl_stats.pack(side="left", padx=4)

        prog = ctk.CTkProgressBar(frame, height=8, corner_radius=4, fg_color="#333333", progress_color=NEON_GREEN)
        prog.pack(side="left", fill="x", expand=True, padx=6)
        prog.set(0.02)

        btn_slow = ctk.CTkButton(
            frame,
            text="Slow Down",
            width=70,
            height=26,
            corner_radius=5,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            hover_color=NEON_CYAN,
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda idx=index: self._on_slow_down_process(idx)
        )
        btn_slow.pack(side="right", padx=(4, 8))

        return {
            "frame": frame,
            "rank": lbl_rank,
            "name": lbl_name,
            "desc": lbl_desc,
            "stats": lbl_stats,
            "progress": prog,
            "btn_slow": btn_slow,
            "pid": None
        }

    def _on_elevate_admin(self):
        restart_as_admin()

    def _on_quick_ram_flush(self):
        freed = purge_all_background_ram(self.top_culprits_cache)
        if self.on_toast:
            self.on_toast("🧹 Free Unused RAM", f"Reclaimed ~{freed:.0f} MB memory from background processes.")

    def _on_master_cool_down(self):
        # <!-- ================= Auto-Adaptive Smart Cooling Logic ================= -->
        temp = getattr(self, "_last_cpu_temp", 45.0)
        if temp >= 75.0:
            mode_key = "deep"
            mode_desc = f"Deep Emergency Cooling ({temp:.1f}°C High Temp)"
        elif temp >= 60.0:
            mode_key = "balanced"
            mode_desc = f"Balanced Relief ({temp:.1f}°C Warm State)"
        else:
            mode_key = "soft"
            mode_desc = f"Soft Calming & Memory Sweep ({temp:.1f}°C Safe State)"

        res = ThermalReliefEngine.apply_cooling_mode(mode_key, self.top_culprits_cache)
        if self.on_toast:
            self.on_toast(f"❄️ {mode_desc}", res["message"])

    def _on_slow_down_process(self, index: int):
        if index < len(self.top_culprits_cache):
            item = self.top_culprits_cache[index]
            pid = item.get("pid")
            if pid:
                res = ThermalReliefEngine.throttle_process(pid)
                if self.on_toast:
                    self.on_toast("Process Slow Down", res["message"])

    def update_telemetry(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]], diagnostics: Dict[str, Any]):
        self.top_culprits_cache = culprits

        # 1. Update Metric Cards
        cpu_t = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 24.0
        self._last_cpu_temp = cpu_t
        max_t = telemetry.get("cpu_temp_max", cpu_t)
        cpu_pwr = telemetry.get("cpu_power", 0.0)
        gpu_t = telemetry.get("gpu_temp", 22.0)
        gpu_l = telemetry.get("gpu_load", 0.0)
        is_adm = telemetry.get("is_admin", False)

        self.card_cpu["val"].configure(text=f"{cpu_t:.1f}°C")
        self.card_cpu["sub"].configure(text=f"Peak: {max_t:.1f}°C | Power: {cpu_pwr:.1f}W")

        if cpu_t >= 80.0:
            self.card_cpu["val"].configure(text_color="#FF0055")
        elif cpu_t >= 65.0:
            self.card_cpu["val"].configure(text_color="#FFA500")
        else:
            self.card_cpu["val"].configure(text_color=NEON_GREEN)

        self.card_gpu["val"].configure(text=f"{gpu_t:.1f}°C")
        self.card_gpu["sub"].configure(text=f"Load: {gpu_l:.0f}%")

        ram_u = telemetry.get("ram_used_gb", 0.0)
        ram_t = telemetry.get("ram_total_gb", 16.0)
        ram_p = telemetry.get("ram_pct", 0)

        self.card_ram["val"].configure(text=f"{ram_u:.1f} GB ({ram_p:.0f}%)")
        self.card_ram["sub"].configure(text=f"Total: {ram_t:.0f} GB Physical Memory")

        # 2. Update Diagnostic Status
        status = diagnostics.get("status", "OPTIMAL")
        headline = diagnostics.get("headline", "System Cool & Healthy")
        badge_col = diagnostics.get("badge_color", NEON_GREEN)

        self.badge_status.configure(text=status, fg_color=badge_col)
        self.lbl_diag_title.configure(text=headline)
        self.lbl_diag_desc.configure(text=diagnostics.get("explanation", "Hardware running at safe temperature."))

        # 3. Update Culprit Rows
        for i, row in enumerate(self.culprit_rows):
            if i < len(culprits):
                c = culprits[i]
                row["frame"].pack(fill="x", pady=2)
                row["name"].configure(text=c.get("name", "Process"))
                row["desc"].configure(text=c.get("description", ""))
                row["stats"].configure(text=f"CPU: {c.get('cpu_percent', 0.0):.1f}% | {c.get('memory_mb', 0):.0f} MB")

                score = c.get("heat_score", 0.0)
                row["progress"].set(min(1.0, max(0.02, score / 100.0)))
                row["progress"].configure(progress_color=c.get("heat_color", NEON_GREEN))
                row["pid"] = c.get("pid")
            else:
                row["frame"].pack_forget()

    def apply_theme(self):
        self.configure(fg_color=BG_COLOR)
        self.stats_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.hero_diag.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.culprits_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.lbl_diag_title.configure(text_color=TEXT_COLOR)
        self.lbl_diag_desc.configure(text_color=TEXT_COLOR)

    def refresh_theme(self):
        self.apply_theme()