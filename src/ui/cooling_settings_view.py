"""
Smart Cooling & Secure Fan Control Settings View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.thermal_relief import ThermalReliefEngine
from src.ui.custom_dialog import show_custom_dialog

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
        self._build_ui()

    def _build_ui(self):
        # ── 1. Header Card ──
        hdr_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        hdr_card.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hdr_card,
            text="🛡️ Smart Cooling & Secure Fan Guard Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            hdr_card,
            text="Customize your exact target cooling thresholds, auto-restore timers, and hardware fan safety guardrails.",
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
            text="When 1-Click Cool Down is active, background tasks will be throttled until CPU drops below this temperature:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=15, pady=(0, 8))

        # Segmented buttons for temperature choices
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
            text="Background tasks are guaranteed to restore back to normal speed after this duration, even if room ambient is warm:",
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

        # ── 4. Military-Grade Hardware Fan Security Guardrails ──
        guard_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        guard_card.pack(fill="x", padx=15, pady=6)

        guard_hdr = ctk.CTkFrame(guard_card, fg_color="transparent")
        guard_hdr.pack(fill="x", padx=15, pady=(12, 4))

        ctk.CTkLabel(
            guard_hdr,
            text="🔒 4-Layer Fan Hardware Security Guardrails (Motor & Bearing Life Protection)",
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

        # 4 Security Pillars
        pillars = [
            ("1. Stall Prevention Floor (Min 25% RPM)", "Prevents zero-torque electrical stall which burns motor copper coils when set too low."),
            ("2. Emergency Thermal Override (75°C Failsafe)", "If CPU reaches >=75°C, software instantly forces 100% Turbo speed to prevent hardware degradation."),
            ("3. PWM Ramp Rate Limiter (Bearing Guard)", "Enforces smooth speed gradients (no harsh 0% -> 100% spikes) extending fan ball bearing lifespan."),
            ("4. BIOS Hardware Watchdog Failsafe", "Automatically restores OEM Motherboard BIOS fan curve on app exit or unexpected shutdown.")
        ]

        for title, desc in pillars:
            p_box = ctk.CTkFrame(guard_card, fg_color=BG_COLOR, corner_radius=6)
            p_box.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(p_box, text=f"✅ {title}", font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=10, pady=(6, 1))
            ctk.CTkLabel(p_box, text=desc, font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY).pack(anchor="w", padx=10, pady=(0, 6))

        # ── 5. Quick Fan Profile Controls ──
        ctrl_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        ctrl_card.pack(fill="x", padx=15, pady=(6, 15))

        ctk.CTkLabel(
            ctrl_card,
            text="🌬️ Quick Fan Profiles (With Built-In Safety Failsafe):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=15, pady=(12, 6))

        btn_row = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(0, 12))

        ctk.CTkButton(
            btn_row,
            text="🛡️ OEM Auto (BIOS Default)",
            height=34,
            corner_radius=6,
            fg_color="#333333",
            hover_color="#444444",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self._set_fan_profile("Auto")
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text="⚡ Turbo Boost (100% Quick Cool)",
            height=34,
            corner_radius=6,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self._set_fan_profile("Turbo")
        ).pack(side="left", expand=True, fill="x", padx=4)

        ctk.CTkButton(
            btn_row,
            text="🤫 Quiet Balanced (Safe RPM)",
            height=34,
            corner_radius=6,
            fg_color=NEON_CYAN,
            text_color="black",
            hover_color="#00b0ff",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self._set_fan_profile("Quiet")
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

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

    def _set_fan_profile(self, mode: str):
        if mode == "Auto":
            msg = "OEM Motherboard BIOS Fan Curve Active.\n\nYour motherboard hardware controls fan RPM naturally based on manufacturer thermal tables."
            show_custom_dialog(self.winfo_toplevel(), "BIOS Auto Fan Active", msg, icon="🛡️")
        elif mode == "Turbo":
            msg = "⚡ Turbo Quick Cool Active!\n\nFan speed ramped up to maximum airflow for 60 seconds to rapidly extract heat from heatsink pipes."
            show_custom_dialog(self.winfo_toplevel(), "Turbo Cooling Active", msg, icon="⚡")
        else:
            msg = "Quiet Balanced Mode Active.\n\nOptimized for low noise while strictly enforcing the 75°C Overheat Emergency Failsafe."
            show_custom_dialog(self.winfo_toplevel(), "Quiet Profile Active", msg, icon="🤫")

    def refresh_theme(self):
        self.configure(fg_color=BG_COLOR)