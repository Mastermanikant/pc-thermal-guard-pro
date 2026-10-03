"""
Smart Cooling, System Junk Cleaner & Startup Settings View
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
from src.core.autostart import is_autostart_enabled, set_autostart
from src.core.system_cleaner import SafeSystemCleaner

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
        # <!-- ================= Section: Top Header Card ================= -->
        hdr_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        hdr_card.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hdr_card,
            text="🛡️ Smart Cooling, System Care & Startup Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            hdr_card,
            text="Configure automated background protection, clean system junk/cache, and launch high-performance sessions.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=18, pady=(0, 14))

        # <!-- ================= Section: Windows Auto-Start Toggle Card ================= -->
        startup_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        startup_card.pack(fill="x", padx=15, pady=8)

        startup_hdr = ctk.CTkFrame(startup_card, fg_color="transparent")
        startup_hdr.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            startup_hdr,
            text="🚀 Run at Windows Startup (Silent Tray Sentinel):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        is_autostart = is_autostart_enabled()
        self.sw_startup_var = ctk.StringVar(value="ON" if is_autostart else "OFF")
        self.sw_startup = ctk.CTkSwitch(
            startup_hdr,
            text="ON" if is_autostart else "OFF",
            font=ctk.CTkFont(size=12, weight="bold"),
            variable=self.sw_startup_var,
            onvalue="ON",
            offvalue="OFF",
            progress_color=NEON_CYAN,
            command=self._on_autostart_toggled
        )
        self.sw_startup.pack(side="right")

        ctk.CTkLabel(
            startup_card,
            text="• Starts silently in the Windows Taskbar Tray (<20MB RAM) on PC boot.\n• Automatically monitors thermals and sweeps stale background cache without opening any popups.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(2, 12))

        # <!-- ================= Section: 1-Click Safe Deep System Cleanup ================= -->
        clean_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        clean_card.pack(fill="x", padx=15, pady=8)

        clean_hdr = ctk.CTkFrame(clean_card, fg_color="transparent")
        clean_hdr.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            clean_hdr,
            text="🧹 1-Click Safe Deep Junk & Cache Cleaner:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        ctk.CTkLabel(
            clean_hdr,
            text="⚡ ZERO RISK",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#003311",
            text_color=NEON_GREEN,
            corner_radius=4,
            padx=6,
            pady=2
        ).pack(side="right")

        ctk.CTkLabel(
            clean_card,
            text="Safely deletes stale temporary files (%TEMP%), Windows error crash dumps, and GPU shader debris. Reclaims 1 to 3 GB disk space and flushes RAM working sets without closing your active work.",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left",
            wraplength=700
        ).pack(anchor="w", padx=18, pady=(2, 10))

        self.btn_deep_clean = ctk.CTkButton(
            clean_card,
            text="🧹 Execute Safe Deep Clean (Clean Temp & Reclaim RAM)",
            height=36,
            corner_radius=8,
            fg_color=NEON_CYAN,
            hover_color="#00b0ff",
            text_color="black",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_execute_deep_clean
        )
        self.btn_deep_clean.pack(fill="x", padx=18, pady=(0, 14))

        # <!-- ================= Section: Advance Game & Studio Launchpad ================= -->
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

        # <!-- ================= Section: Intelligent Auto-Thermostat & Manual Presets ================= -->
        mode_card = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        mode_card.pack(fill="x", padx=15, pady=8)

        mode_hdr = ctk.CTkFrame(mode_card, fg_color="transparent")
        mode_hdr.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            mode_hdr,
            text="🤖 Intelligent Auto-Thermostat & Relief Intensity:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(side="left")

        ctk.CTkLabel(
            mode_hdr,
            text="50°C - 55°C Sweet Spot",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#003311",
            text_color=NEON_GREEN,
            corner_radius=4,
            padx=6,
            pady=2
        ).pack(side="right")

        ctk.CTkLabel(
            mode_card,
            text="Built-in intelligent thermostat maintains silicon within 50°C-55°C optimal silent range automatically. Choose preferred default relief depth:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(2, 10))

        self.mode_var = ctk.StringVar(value="⚡ Balanced (Recommended)")
        self.seg_mode = ctk.CTkSegmentedButton(
            mode_card,
            values=["🌱 Soft", "⚡ Balanced (Recommended)", "❄️ Deep"],
            variable=self.mode_var,
            height=34,
            corner_radius=6,
            fg_color=BG_COLOR,
            selected_color=NEON_CYAN,
            selected_hover_color=NEON_CYAN,
            unselected_color=FRAME_BG,
            unselected_hover_color=BORDER_COLOR,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_mode_preset_changed
        )
        self.seg_mode.pack(fill="x", padx=18, pady=(0, 8))

        self.lbl_mode_hint = ctk.CTkLabel(
            mode_card,
            text="💡 Balanced Mode: Throttles top background spikes while keeping active foreground window 100% fast.",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=NEON_GREEN
        )
        self.lbl_mode_hint.pack(anchor="w", padx=18, pady=(0, 14))

        # <!-- ================= Section: Telemetry History Logging Toggle ================= -->
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

        # <!-- ================= Section: 3-Tier Thermal Safety Pillars ================= -->
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

    def _on_autostart_toggled(self):
        is_on = self.sw_startup_var.get() == "ON"
        self.sw_startup.configure(text="ON" if is_on else "OFF")
        success = set_autostart(is_on)
        if self.toast:
            if success and is_on:
                self.toast("🚀 Windows Startup Enabled: App will run silently in the system tray on boot.")
            elif success and not is_on:
                self.toast("Windows Startup Disabled.")

    def _on_execute_deep_clean(self):
        res = SafeSystemCleaner.execute_deep_clean()
        if self.toast:
            self.toast(res["message"])

    def _on_mode_preset_changed(self, val: str):
        if "Soft" in val:
            hint = "💡 Soft Mode: Cleans background RAM and calms idle updaters. Zero impact on multitasking."
        elif "Deep" in val:
            hint = "💡 Deep Mode: Emergency thermal relief. Calms all background tasks for maximum temperature drop."
        else:
            hint = "💡 Balanced Mode: Throttles top background spikes while keeping active foreground window 100% fast."
        self.lbl_mode_hint.configure(text=hint)
        if self.toast:
            self.toast(f"❄️ Default Cooling Mode set to: {val}")

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