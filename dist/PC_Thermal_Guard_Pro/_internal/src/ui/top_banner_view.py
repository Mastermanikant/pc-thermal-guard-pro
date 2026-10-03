"""
Top Header Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import customtkinter as ctk
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR
from src.core.licensing import LicenseManager

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

        self._build_ui()

    def _build_ui(self):
        self.header_inner = ctk.CTkFrame(self, fg_color="transparent", height=50)
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

        # 3. Right Controls: Theme Switch & System Tray
        self.btn_tray = ctk.CTkButton(
            self.header_inner,
            text="📥 Tray",
            width=70,
            height=30,
            corner_radius=6,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            hover_color=NEON_CYAN,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_minimize_tray
        )
        self.btn_tray.pack(side="right", padx=(6, 0))

        # Day/Night Mode Switch
        self.theme_box = ctk.CTkFrame(self.header_inner, fg_color=BG_COLOR, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        self.theme_box.pack(side="right", padx=6)

        is_dark = ThemeManager.get_current_theme() == "dark"
        self.theme_switch_var = ctk.StringVar(value="Night" if is_dark else "Day")
        self.sw_theme = ctk.CTkSwitch(
            self.theme_box,
            text="🌙 Night Mode" if is_dark else "☀️ Day Mode",
            font=ctk.CTkFont(size=11, weight="bold"),
            variable=self.theme_switch_var,
            onvalue="Night",
            offvalue="Day",
            progress_color=NEON_CYAN,
            command=self._on_theme_switch_clicked
        )
        self.sw_theme.pack(padx=10, pady=4)

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