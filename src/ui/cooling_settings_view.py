"""
Smart Cooling & Thermal Relief Settings View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import time
import threading
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
        self._countdown_active = False
        self._build_ui()

    def _build_ui(self):
        # ── 1. Top Header Card ──
        hdr_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        hdr_card.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hdr_card,
            text="🛡️ Smart Cooling & Thermal Relief Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            hdr_card,
            text="Fine-tune your hardware cooling limits, auto-restore timers, and launch dedicated high-performance sessions.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=18, pady=(0, 14))

        # ── 2. Advance Game & Studio Launchpad Card (Clean Slate Mode) ──
        launch_card = ctk.CTkFrame(self, fg_color="#181a2e", corner_radius=10, border_width=1, border_color=NEON_CYAN)
        launch_card.pack(fill="x", padx=15, pady=8)

        launch_hdr = ctk.CTkFrame(launch_card, fg_color="transparent")
        launch_hdr.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            launch_hdr,
            text="🚀 Advance Game & Studio Launchpad (Clean Slate Mode)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=NEON_CYAN
        ).pack(side="left")

        ctk.CTkLabel(
            launch_hdr,
            text="⚡ ZERO BLOAT",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#003344",
            text_color=NEON_CYAN,
            corner_radius=4,
            padx=6,
            pady=2
        ).pack(side="right")

        ctk.CTkLabel(
            launch_card,
            text="Closes non-essential background user applications (browsers, updaters, discord, torrents) and flushes RAM to dedicate 100% CPU & memory power to your upcoming heavy Game or Video Editing suite.",
            font=ctk.CTkFont(size=11),
            text_color="#cbd5e1",
            justify="left",
            wraplength=700
        ).pack(anchor="w", padx=18, pady=(2, 10))

        self.btn_launchpad = ctk.CTkButton(
            launch_card,
            text="🚀 Activate Advance Launchpad (Clean Background & Free RAM)",
            height=38,
            corner_radius=8,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_launchpad_clicked
        )
        self.btn_launchpad.pack(fill="x", padx=18, pady=(0, 14))

        # ── 3. Target Temperature Threshold Setting ──
        temp_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        temp_card.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(
            temp_card,
            text="🎯 Target Cool-Down Temperature Threshold (°C):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(14, 2))

        ctk.CTkLabel(
            temp_card,
            text="When Cool Down is active, background tasks remain throttled until CPU drops below this temperature:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=18, pady=(0, 10))

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
        self.seg_temp.pack(fill="x", padx=18, pady=(0, 8))

        self.lbl_temp_hint = ctk.CTkLabel(
            temp_card,
            text=f"💡 Current Selection: {self.temp_var.get()} : Recommended for balanced thermal longevity and smooth multitasking.",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=NEON_GREEN
        )
        self.lbl_temp_hint.pack(anchor="w", padx=18, pady=(0, 14))

        # ── 4. Auto-Restore Timeout Setting ──
        timeout_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        timeout_card.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(
            timeout_card,
            text="⏱️ Maximum Throttling Timeout (Auto-Restore Safety Timer):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(14, 2))

        ctk.CTkLabel(
            timeout_card,
            text="Background tasks are guaranteed to restore back to normal priority after this duration, even in warm rooms:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=18, pady=(0, 10))

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
        self.seg_timeout.pack(fill="x", padx=18, pady=(0, 14))

        # ── 5. Telemetry History Logging Toggle Card ──
        log_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        log_card.pack(fill="x", padx=15, pady=8)

        log_hdr = ctk.CTkFrame(log_card, fg_color="transparent")
        log_hdr.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            log_hdr,
            text="💾 Background History Recording (SQLite WAL Database):",
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
            text="• ON: Saves 60-second telemetry snapshots for the 7-day Visual History tab.\n• OFF (Ultra-Lean): Zero disk writes. App runs 100% in pure RAM without saving logs.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left"
        )
        self.lbl_log_desc.pack(anchor="w", padx=18, pady=(2, 10))

        btn_clear_history = ctk.CTkButton(
            log_card,
            text="🗑️ Clear Saved History Database",
            height=30,
            corner_radius=6,
            fg_color="#262626",
            hover_color="#550000",
            text_color="#ff8888",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_clear_history_clicked
        )
        btn_clear_history.pack(anchor="w", padx=18, pady=(0, 14))

        # ── 6. 3-Tier Thermal Safety Pillars Card ──
        guard_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        guard_card.pack(fill="x", padx=15, pady=(8, 20))

        guard_hdr = ctk.CTkFrame(guard_card, fg_color="transparent")
        guard_hdr.pack(fill="x", padx=18, pady=(14, 4))

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
            p_box.pack(fill="x", padx=18, pady=4)
            ctk.CTkLabel(p_box, text=f"✅ {title}", font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", padx=12, pady=(6, 1))
            ctk.CTkLabel(p_box, text=desc, font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY).pack(anchor="w", padx=12, pady=(0, 6))

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

    def _on_launchpad_clicked(self):
        """Opens a transparent 5-second countdown dialog before executing clean slate."""
        top = ctk.CTkToplevel(self)
        top.title("Advance Launchpad Activation")
        top.geometry("480x250")
        top.resizable(False, False)
        top.configure(fg_color="#0f172a")
        top.grab_set()

        # Center dialog
        top.update_idletasks()
        x = (top.winfo_screenwidth() - 480) // 2
        y = (top.winfo_screenheight() - 250) // 2
        top.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            top,
            text="🚀 Advance Game/Studio Launchpad",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=NEON_CYAN
        ).pack(pady=(16, 6))

        ctk.CTkLabel(
            top,
            text="Warning: This will gracefully close background browsers, updaters,\nand user apps to free 100% CPU & RAM for your game/editor.",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
            justify="center"
        ).pack(pady=(0, 10))

        lbl_timer = ctk.CTkLabel(
            top,
            text="Starting in: 5s",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NEON_MAGENTA
        )
        lbl_timer.pack(pady=(0, 14))

        btn_box = ctk.CTkFrame(top, fg_color="transparent")
        btn_box.pack(fill="x", padx=30, pady=(0, 10))

        canceled = {"val": False}

        def _cancel():
            canceled["val"] = True
            top.destroy()
            if self.toast:
                self.toast("Advance Launchpad canceled.")

        def _execute():
            canceled["val"] = True
            top.destroy()
            res = ThermalReliefEngine.execute_advance_clean_slate()
            if self.toast:
                self.toast(res["message"])

        btn_cancel = ctk.CTkButton(
            btn_box,
            text="Cancel",
            width=100,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            text_color="white",
            command=_cancel
        )
        btn_cancel.pack(side="left", expand=True, padx=4)

        btn_now = ctk.CTkButton(
            btn_box,
            text="⚡ Activate Now",
            width=140,
            height=34,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            font=ctk.CTkFont(weight="bold"),
            command=_execute
        )
        btn_now.pack(side="right", expand=True, padx=4)

        def _countdown():
            for remaining in range(5, 0, -1):
                if canceled["val"] or not top.winfo_exists():
                    return
                try:
                    lbl_timer.configure(text=f"Auto-activating in: {remaining}s")
                except Exception:
                    return
                time.sleep(1.0)

            if not canceled["val"] and top.winfo_exists():
                try:
                    top.after(0, _execute)
                except Exception:
                    pass

        threading.Thread(target=_countdown, daemon=True).start()

    def refresh_theme(self):
        self.configure(fg_color=BG_COLOR)