"""
Left Sidebar Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import customtkinter as ctk
import webbrowser
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, SIDEBAR_BG, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.ui.custom_dialog import show_custom_dialog

class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate_callback: Callable[[str], None], **kwargs):
        super().__init__(
            parent,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
            width=230,
            **kwargs
        )
        self.on_navigate = on_navigate_callback
        self.current_active_nav = "Dashboard"
        self.nav_buttons = {}

        self.grid_propagate(False)
        self._build_ui()

    def _build_ui(self):
        # 1. Fixed Bottom Founder & Credibility Card (Always at bottom of sidebar)
        self.bottom_controls = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        self.bottom_controls.pack(side="bottom", fill="x", padx=10, pady=(6, 12))

        ctk.CTkLabel(self.bottom_controls, text="Designed & Developed By:", font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY).pack(pady=(6, 0))
        ctk.CTkLabel(self.bottom_controls, text="Master Manikant Yadav", font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT_COLOR).pack(pady=(1, 3))

        ctk.CTkButton(
            self.bottom_controls,
            text="🌐 MasterManikant.com",
            height=26,
            fg_color="transparent",
            border_width=1,
            border_color=NEON_CYAN,
            text_color=NEON_CYAN,
            hover_color="#003344",
            corner_radius=6,
            font=ctk.CTkFont(size=10, weight="bold"),
            cursor="hand2",
            command=lambda: webbrowser.open("https://mastermanikant.com")
        ).pack(pady=(2, 4), padx=10, fill="x")

        privacy_text = "100% Local & Privacy-First Architecture"
        ctk.CTkLabel(self.bottom_controls, text=privacy_text, font=ctk.CTkFont(size=8, slant="italic"), text_color=DYNAMIC_GRAY).pack(pady=(0, 2))

        legal_lbl = ctk.CTkLabel(self.bottom_controls, text="📜 Legal Terms & Privacy Policy", font=ctk.CTkFont(size=9, underline=True), text_color=DYNAMIC_GRAY, cursor="hand2")
        legal_lbl.pack(pady=(0, 6))
        legal_lbl.bind("<Button-1>", lambda e: self._show_legal_modal())

        # 2. Scrollable Navigation Area (Takes all remaining vertical space)
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
            scrollbar_button_color=("#cccccc", "#333333"),
            scrollbar_button_hover_color=NEON_CYAN
        )
        self.sidebar_scroll.pack(side="top", fill="both", expand=True)

        # Navigation Buttons (Clean, focused 4 distinct tabs)
        items = [
            ("Dashboard", "1. ⚡ Live Dashboard"),
            ("History", "2. 📈 Visual History"),
            ("Cooling", "3. ⚙️ Settings & Cooling"),
            ("License", "4. 🔑 License & Support"),
        ]

        for key, label in items:
            btn = ctk.CTkButton(
                self.sidebar_scroll,
                text=label,
                corner_radius=8,
                height=40,
                border_spacing=10,
                fg_color="transparent",
                text_color=TEXT_COLOR,
                hover_color=BORDER_COLOR,
                anchor="w",
                font=ctk.CTkFont(weight="bold", size=13),
                command=lambda k=key: self._on_btn_clicked(k)
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[key] = btn

        self._highlight_active_nav()

        # Thermal Protection Status Pill Card
        self.status_card = ctk.CTkFrame(self.sidebar_scroll, fg_color=FRAME_BG, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        self.status_card.pack(fill="x", padx=10, pady=(15, 8))

        ctk.CTkLabel(
            self.status_card,
            text="🟢 Auto-Guard Active",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#10b981"
        ).pack(anchor="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            self.status_card,
            text="Foreground work is 100% protected.\nLow overhead <0.3% CPU usage.",
            font=ctk.CTkFont(size=10),
            text_color=DYNAMIC_GRAY,
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 8))

    def _on_btn_clicked(self, key: str):
        self.current_active_nav = key
        self._highlight_active_nav()
        if self.on_navigate:
            self.on_navigate(key)

    def _highlight_active_nav(self):
        for k, btn in self.nav_buttons.items():
            if k == self.current_active_nav:
                btn.configure(
                    fg_color=NEON_CYAN,
                    text_color="black"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_COLOR
                )

    def _show_legal_modal(self):
        msg = (
            "FrankBase Legal Terms & Privacy Commitment:\n\n"
            "• Zero Telemetry: No hardware metrics, logs, or personal data ever leave your PC.\n"
            "• Read-Only Sensors: Safe hardware polling without BIOS alterations.\n"
            "• Machine ID Licensing: 100% offline verification on this machine.\n\n"
            "Official Website: mastermanikant.com"
        )
        show_custom_dialog(self.winfo_toplevel(), "Legal Terms & Privacy", msg, icon="📜", link_url="https://mastermanikant.com/privacy")

    def refresh_theme(self):
        self.configure(fg_color=SIDEBAR_BG)
        self.sidebar_scroll.configure(fg_color=SIDEBAR_BG)
        self.status_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.bottom_controls.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self._highlight_active_nav()