"""
Header Component (100% Matched with FrankBase Smart File Organizer Header - Screenshots 2 & 3)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk
import webbrowser
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.machine_id import get_machine_hardware_id, copy_machine_id_to_clipboard
from src.ui.custom_dialog import show_custom_dialog

class TopCollapsibleHeader(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_toggle_theme_callback: Callable[[], None],
        on_minimize_tray_callback: Callable[[], None],
        on_toast_callback: Callable[[str], None] = None,
        **kwargs
    ):
        super().__init__(
            parent,
            fg_color=FRAME_BG,
            corner_radius=0,
            border_width=1,
            border_color=BORDER_COLOR,
            **kwargs
        )
        self.on_toggle_theme = on_toggle_theme_callback
        self.on_minimize_tray = on_minimize_tray_callback
        self.toast = on_toast_callback
        self.hwid = get_machine_hardware_id()
        self.user_persona_var = ctk.StringVar(value="Normal")

        self._build_ui()

    def _build_ui(self):
        self.header_inner = ctk.CTkFrame(self, fg_color="transparent", height=52)
        self.header_inner.pack(fill="x", padx=15, pady=8)

        # 1. Left Brand: FRANKBASE (Neon Cyan) + PC Thermal Guard Pro (White)
        brand_box = ctk.CTkFrame(self.header_inner, fg_color="transparent")
        brand_box.pack(side="left", padx=(0, 15))

        self.lbl_brand_main = ctk.CTkLabel(
            brand_box,
            text="FRANKBASE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NEON_CYAN
        )
        self.lbl_brand_main.pack(anchor="w")

        self.lbl_brand_sub = ctk.CTkLabel(
            brand_box,
            text="PC Thermal Guard Pro",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.lbl_brand_sub.pack(anchor="w")

        # 2. Plan Badge (Magenta Pill matching Screenshot 2)
        self.btn_plan_badge = ctk.CTkButton(
            self.header_inner,
            text="🛡️ Community Edition - Free",
            height=30,
            corner_radius=6,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_plan_click
        )
        self.btn_plan_badge.pack(side="left", padx=8)

        # 3. Persona Switch (Normal User / Gamer Turbo Mode)
        self.persona_frame = ctk.CTkFrame(self.header_inner, fg_color=BG_COLOR, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        self.persona_frame.pack(side="left", padx=8)

        self.sw_persona = ctk.CTkSwitch(
            self.persona_frame,
            text="👤 Normal User",
            font=ctk.CTkFont(size=11, weight="bold"),
            variable=self.user_persona_var,
            onvalue="Turbo",
            offvalue="Normal",
            progress_color=NEON_CYAN,
            command=self._on_persona_toggled
        )
        self.sw_persona.pack(padx=10, pady=4)

        # 4. Privacy Friendly Badge (Green Pill matching Screenshot 2)
        self.btn_privacy = ctk.CTkButton(
            self.header_inner,
            text="🛡️ 100% Offline & Privacy Friendly (learn more ↗)",
            height=28,
            corner_radius=20,
            fg_color="#003311",
            text_color=NEON_GREEN,
            hover_color="#004419",
            border_width=1,
            border_color=NEON_GREEN,
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._show_privacy_modal
        )
        self.btn_privacy.pack(side="left", padx=8)

        # 5. Right Controls: Theme Switch & System Tray
        self.btn_tray = ctk.CTkButton(
            self.header_inner,
            text="📥 Tray",
            width=65,
            height=28,
            corner_radius=6,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            hover_color=NEON_CYAN,
            font=ctk.CTkFont(size=11),
            command=self.on_minimize_tray
        )
        self.btn_tray.pack(side="right", padx=(4, 0))

        # Day/Night Mode Switch (Matching Screenshot 2/3)
        self.theme_box = ctk.CTkFrame(self.header_inner, fg_color=BG_COLOR, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        self.theme_box.pack(side="right", padx=6)

        self.theme_switch_var = ctk.StringVar(value="Night" if ThemeManager.get_current_theme() == "dark" else "Day")
        self.sw_theme = ctk.CTkSwitch(
            self.theme_box,
            text="🌙 Night Mode" if ThemeManager.get_current_theme() == "dark" else "☀️ Day Mode",
            font=ctk.CTkFont(size=11, weight="bold"),
            variable=self.theme_switch_var,
            onvalue="Night",
            offvalue="Day",
            progress_color=NEON_CYAN,
            command=self._on_theme_switch_clicked
        )
        self.sw_theme.pack(padx=10, pady=4)

    def _on_persona_toggled(self):
        val = self.user_persona_var.get()
        if val == "Turbo":
            self.sw_persona.configure(text="⚡ Power Gamer (Turbo)")
            msg = (
                "Power Gamer Mode Activated!\n\n"
                "• Aggressive Background Heat Throttling Enabled.\n"
                "• Real-time 0.5s ultra-fast sensor polling.\n"
                "• All heavy background tasks will be automatically parked on E-Cores during gaming.\n\n"
                "Need more details? Visit frankbase.com/pcthermalguard"
            )
            show_custom_dialog(self.winfo_toplevel(), "Gamer Turbo Mode Active", msg, icon="⚡", link_url="https://mastermanikant.com")
        else:
            self.sw_persona.configure(text="👤 Normal User")
            msg = (
                "Normal User Mode Activated!\n\n"
                "• Standard Balanced Cooling Profile.\n"
                "• Low-overhead asynchronous telemetry (<18MB RAM).\n"
                "• Protected Active Window: Your active work will never be interrupted.\n\n"
                "System Protection Guaranteed: Windows system kernel remains protected."
            )
            show_custom_dialog(self.winfo_toplevel(), "Normal User Mode Active", msg, icon="👤", link_url="https://mastermanikant.com")

    def _show_privacy_modal(self):
        msg = (
            "100% Offline & Privacy Friendly Architecture!\n\n"
            "• Zero Cloud Telemetry: PC Thermal Guard Pro does not send any hardware telemetry or process logs over the internet.\n\n"
            "• Zero Ads & Zero Tracking: 100% private, local-first engineering.\n\n"
            "• Offline RSA-2048 Licensing: Pro features are verified completely offline on your PC without third-party server pings.\n\n"
            "Developed by Master Manikant Yadav | FrankBase Ecosystem."
        )
        show_custom_dialog(self.winfo_toplevel(), "Privacy Guarantee", msg, icon="🛡️", link_url="https://mastermanikant.com/privacy")

    def _on_plan_click(self):
        msg = (
            "Pro Lifetime License Upgrade!\n\n"
            "• Auto-Sentry Background Silent Cooling.\n"
            "• 30-Day SQLite Deep Historical Heat Ledger.\n"
            "• Exportable Hardware Health Reports (PDF/CSV).\n"
            "• AI Voice Alerts (Edge-TTS).\n\n"
            "Upgrade for only ₹299 INR / $9.99 USD One-Time Lifetime!"
        )
        show_custom_dialog(self.winfo_toplevel(), "Upgrade to Pro", msg, icon="⭐", link_url="https://store.frankbase.com")

    def _on_theme_switch_clicked(self):
        self.on_toggle_theme()
        is_dark = ThemeManager.get_current_theme() == "dark"
        self.sw_theme.configure(text="🌙 Night Mode" if is_dark else "☀️ Day Mode")

    def refresh_theme(self):
        is_dark = ThemeManager.get_current_theme() == "dark"
        self.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.lbl_brand_main.configure(text_color=NEON_CYAN)
        self.lbl_brand_sub.configure(text_color=TEXT_COLOR)
        self.persona_frame.configure(fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.theme_box.configure(fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.sw_theme.configure(text="🌙 Night Mode" if is_dark else "☀️ Day Mode")