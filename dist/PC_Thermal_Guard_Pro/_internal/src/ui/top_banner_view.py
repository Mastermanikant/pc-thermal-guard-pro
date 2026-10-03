"""
Top Header Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import customtkinter as ctk
import webbrowser
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.licensing import LicenseManager
from src.core.machine_id import get_machine_hardware_id
from src.ui.custom_dialog import show_custom_dialog

class TopCollapsibleHeader(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_toggle_theme_callback: Callable[[], None],
        on_minimize_tray_callback: Callable[[], None],
        on_navigate_callback: Callable[[str], None] = None,
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
        self.on_navigate = on_navigate_callback
        self.toast = on_toast_callback
        self.license_mgr = LicenseManager.get_instance()
        self.hwid = get_machine_hardware_id()

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

        # 2. Plan / 30-Day Beta Status Badge
        badge_text = self.license_mgr.get_status_badge_text()
        badge_color = "#059669" if self.license_mgr.is_pro_active() else NEON_MAGENTA

        self.btn_plan_badge = ctk.CTkButton(
            self.header_inner,
            text=badge_text,
            height=30,
            corner_radius=6,
            fg_color=badge_color,
            hover_color="#c00060" if not self.license_mgr.is_pro_active() else "#047857",
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_plan_click
        )
        self.btn_plan_badge.pack(side="left", padx=6)

        # 3. 50% Community Discount Action Button (Opens browser with Device ID)
        self.btn_feedback_discount = ctk.CTkButton(
            self.header_inner,
            text="🎁 Get 50% OFF Pro (Takes ≤2 mins) ↗",
            height=30,
            corner_radius=6,
            fg_color="#1e1b4b",
            hover_color="#312e81",
            text_color=NEON_CYAN,
            border_width=1,
            border_color=NEON_CYAN,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._open_feedback_discount
        )
        self.btn_feedback_discount.pack(side="left", padx=6)

        # 4. Privacy Friendly Badge
        self.btn_privacy = ctk.CTkButton(
            self.header_inner,
            text="🛡️ 100% Offline & Private (Learn more ↗)",
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
        self.btn_privacy.pack(side="left", padx=6)

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

        # Day/Night Mode Switch
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

    def _open_feedback_discount(self):
        url = self.license_mgr.get_feedback_discount_url()
        try:
            webbrowser.open(url)
        except Exception:
            pass
        if self.toast:
            self.toast("🌐 Opening Feedback page with your Device ID...")

    def _show_privacy_modal(self):
        msg = (
            "100% Offline & Privacy Friendly Architecture:\n\n"
            "• Zero Cloud Telemetry: PC Thermal Guard Pro never transmits sensor data or process logs over the internet.\n\n"
            "• Zero Ads & Zero Tracking: 100% local, private background execution.\n\n"
            "• Machine-Bound License: Your Device ID is verified completely offline on your PC.\n\n"
            "Developed by Master Manikant Yadav | FrankBase Ecosystem."
        )
        show_custom_dialog(self.winfo_toplevel(), "Privacy Guarantee", msg, icon="🛡️", link_url="https://mastermanikant.com/privacy")

    def _on_plan_click(self):
        if self.on_navigate:
            self.on_navigate("License")

    def _on_theme_switch_clicked(self):
        self.on_toggle_theme()
        is_dark = ThemeManager.get_current_theme() == "dark"
        self.sw_theme.configure(text="🌙 Night Mode" if is_dark else "☀️ Day Mode")

    def refresh_theme(self):
        is_dark = ThemeManager.get_current_theme() == "dark"
        self.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.lbl_brand_main.configure(text_color=NEON_CYAN)
        self.lbl_brand_sub.configure(text_color=TEXT_COLOR)
        self.theme_box.configure(fg_color=BG_COLOR, border_color=BORDER_COLOR)
        self.sw_theme.configure(text="🌙 Night Mode" if is_dark else "☀️ Day Mode")
        self.btn_plan_badge.configure(
            text=self.license_mgr.get_status_badge_text(),
            fg_color="#059669" if self.license_mgr.is_pro_active() else NEON_MAGENTA
        )