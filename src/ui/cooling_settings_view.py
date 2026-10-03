"""
Smart Cooling & Thermal Relief Settings View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import customtkinter as ctk
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.thermal_relief import ThermalReliefEngine
from src.core.history_manager import HistoryManager

class CoolingSettingsView(ctk.CTkScrollableFrame):
    def __init__(self, master, on_toast: Callable[[str], None] = None, **kwargs):
        super().__init__(
            master,
            fg_color=BG_COLOR,
            corner_radius=0,
            scrollbar_button_color=("#cccccc", "#333333"),
            scrollbar_button_hover_color=NEON_CYAN,
            **kwargs
        )
        self.toast = on_toast
        self.history_mgr = HistoryManager.get_instance()
        self._build_ui()

    def _build_ui(self):
        # ── 1. Header Card ──
        hdr_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        hdr_card.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hdr_card,
            text="🛡️ Smart Cooling & Thermal Relief Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            hdr_card,
            text="Customize your exact target cooling thresholds, auto-restore timers, and telemetry logging preferences.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=15, pady=(0, 12))

        # ── 2. Target Temperature Threshold Setting ──
        temp_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        temp_card.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            temp_card,
            text="🎯 Target Cool-Down Temperature Threshold (°C):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(12, 2))

        ctk.CTkLabel(
            temp_card,
            text="When Cool Down is active, background tasks remain throttled until CPU drops below this temperature:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=15, pady=(0, 8))

        current_temp_str = f"{int(ThermalReliefEngine.restore_target_temp)}°C"
        self.temp_var = ctk.StringVar(value=current_temp_str if current_temp_str in ["45°C", "50°C", "55°C", "60°C", "65°C"] else "55°C")

        self.seg_temp = ctk.CTkSegmentedButton(
            temp_card,
            values=["45°C", "50°C", "55°C", "60°C", "65°C"],
            variable=self.temp_var,
            height=34,
            corner_radius=6,
            fg_color=BG_COLOR,
            selected_color=NEON_CYAN,
            selected_hover_color=NEON_CYAN,
            unselected_color=FRAME_BG,
            unselected_hover_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_temp_changed
        )
        self.seg_temp.pack(fill="x", padx=15, pady=(0, 8))

        self.lbl_temp_hint = ctk.CTkLabel(
            temp_card,
            text=f"💡 Current Selection: {self.temp_var.get()} : Recommended for balanced thermal longevity and smooth multitasking.",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=NEON_GREEN
        )
        self.lbl_temp_hint.pack(anchor="w", padx=15, pady=(0, 12))

        # ── 3. Auto-Restore Timeout Setting ──
        timeout_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        timeout_card.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            timeout_card,
            text="⏱️ Maximum Throttling Timeout (Auto-Restore Safety Timer):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(12, 2))

        ctk.CTkLabel(
            timeout_card,
            text="Background tasks are guaranteed to restore back to normal priority after this duration, even in warm rooms:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=15, pady=(0, 8))

        current_timeout_str = f"{ThermalReliefEngine.restore_timeout_sec}s"
        self.timeout_var = ctk.StringVar(value=current_timeout_str if current_timeout_str in ["30s", "45s", "60s", "90s"] else "45s")

        self.seg_timeout = ctk.CTkSegmentedButton(
            timeout_card,
            values=["30s", "45s", "60s", "90s"],
            variable=self.timeout_var,
            height=34,
            corner_radius=6,
            fg_color=BG_COLOR,
            selected_color=NEON_MAGENTA,
            selected_hover_color=NEON_MAGENTA,
            unselected_color=FRAME_BG,
            unselected_hover_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_timeout_changed
        )
        self.seg_timeout.pack(fill="x", padx=15, pady=(0, 12))

        # ── 4. Telemetry History Logging Toggle Card ──
        log_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        log_card.pack(fill="x", padx=15, pady=6)

        log_hdr = ctk.CTkFrame(log_card, fg_color="transparent")
        log_hdr.pack(fill="x", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            log_hdr,
            text="💾 Background History Recording (Save to Local SQLite DB):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        is_logging = self.history_mgr.is_logging_enabled
        self.sw_log_var = ctk.StringVar(value="ON" if is_logging else "OFF")
        self.sw_logging = ctk.CTkSwitch(
            log_hdr,
            text="ON" if is_logging else "OFF",
            font=ctk.CTkFont(size=12, weight="bold"),
            variable=self.sw_log_var,
            onvalue="ON",
            offvalue="OFF",
            progress_color=NEON_GREEN,
            command=self._on_logging_toggled
        )
        self.sw_logging.pack(side="right")

        self.lbl_log_desc = ctk.CTkLabel(
            log_card,
            text="• ON: Saves 60-second telemetry snapshots for the 7-day Visual History tab.\n• OFF (Ultra-Lean): Zero disk writes. App runs 100% in RAM with zero background disk activity.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left"
        )
        self.lbl_log_desc.pack(anchor="w", padx=15, pady=(2, 8))

        btn_clear_history = ctk.CTkButton(
            log_card,
            text="🗑️ Clear Saved History Database",
            height=28,
            corner_radius=6,
            fg_color="#333333",
            hover_color="#550000",
            text_color="#ff8888",
            font=ctk.CTkFont(size=11),
            command=self._on_clear_history_clicked
        )
        btn_clear_history.pack(anchor="w", padx=15, pady=(0, 12))

        # ── 5. Real Safety & Process Guardrails ──
        guard_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        guard_card.pack(fill="x", padx=15, pady=(6, 15))

        guard_hdr = ctk.CTkFrame(guard_card, fg_color="transparent")
        guard_hdr.pack(fill="x", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            guard_hdr,
            text="🔒 3-Tier Thermal Safety & Memory Protection Pillars",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=NEON_CYAN
        ).pack(side="left")

        ctk.CTkLabel(
            guard_hdr,
            text="🛡️ 100% ENFORCED",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#003311",
            text_color=NEON_GREEN,
            corner_radius=4,
            padx=6,
            pady=2
        ).pack(side="right")

        pillars = [
            ("1. Active Window Immunity", "The app currently focused by the user is never throttled, guaranteeing zero disruption during gaming or typing."),
            ("2. Windows Working-Set Memory Flush", "Reclaims stale RAM pages via psapi.EmptyWorkingSet, reducing memory bus heat and unneeded load."),
            ("3. Kernel & System Process Protection", "Core Windows system processes (PID <= 4, csrss.exe, dwm.exe) are strictly protected from modification.")
        ]

        for title, desc in pillars:
            p_box = ctk.CTkFrame(guard_card, fg_color=BG_COLOR, corner_radius=6)
            p_box.pack(fill="x", padx=15, pady=4)
            ctk.CTkLabel(p_box, text=f"✅ {title}", font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=10, pady=(6, 1))
            ctk.CTkLabel(p_box, text=desc, font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY).pack(anchor="w", padx=10, pady=(0, 6))

    def _on_temp_changed(self, value: str):
        val = float(value.replace("°C", ""))
        ThermalReliefEngine.save_config(target_temp=val)
        self.lbl_temp_hint.configure(text=f"💡 Current Selection: {val:.0f}°C : Setting saved to persistent disk configuration.")
        if self.toast:
            self.toast(f"💾 Target Cool-Down threshold set to {val:.0f}°C")

    def _on_timeout_changed(self, value: str):
        val = int(value.replace("s", ""))
        ThermalReliefEngine.save_config(timeout_sec=val)
        if self.toast:
            self.toast(f"💾 Auto-restore safety timeout set to {val} seconds")

    def _on_logging_toggled(self):
        is_on = self.sw_log_var.get() == "ON"
        self.sw_logging.configure(text="ON" if is_on else "OFF")
        self.history_mgr.save_config(is_on)
        if self.toast:
            if is_on:
                self.toast("💾 History Logging Enabled: 60s snapshots will be saved to SQLite.")
            else:
                self.toast("⚡ Ultra-Lean Mode: History disk recording turned OFF (Pure RAM mode).")

    def _on_clear_history_clicked(self):
        success = self.history_mgr.clear_all_history()
        if self.toast:
            if success:
                self.toast("🗑️ All historical telemetry logs have been cleared.")
            else:
                self.toast("⚠️ Could not clear history database.")

    def refresh_theme(self):
        self.configure(fg_color=BG_COLOR)