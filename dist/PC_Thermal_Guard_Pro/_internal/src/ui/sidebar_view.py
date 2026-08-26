"""
Collapsible Sidebar Component with Shrink/Expand (240px <-> 60px)
PC Thermal Guard Pro
"""
import customtkinter as ctk
import webbrowser
from typing import Callable
from src.ui.theme import ThemeManager

class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate_callback: Callable[[str], None], **kwargs):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color=self.colors["card_bg"],
            corner_radius=0,
            width=240,
            **kwargs
        )
        self.on_navigate = on_navigate_callback
        self.is_expanded = True
        self.current_active_nav = "Dashboard"
        self.nav_buttons = {}

        self.grid_propagate(False)
        self._build_ui()

    def _build_ui(self):
        # Header / Toggle Row
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=45)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 8))

        # Brand / Toggle Button
        self.btn_toggle = ctk.CTkButton(
            self.header_frame,
            text="☰   MENU",
            width=40,
            height=34,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"],
            hover_color=self.colors["accent_blue"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_shrink_expand
        )
        self.btn_toggle.pack(side="left", fill="x", expand=True)

        # Scrollable Nav Container
        self.nav_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.colors["border_color"],
            scrollbar_button_hover_color=self.colors["accent_cyan"]
        )
        self.nav_container.pack(fill="both", expand=True, padx=6, pady=4)

        # Nav items: (Key, Icon, Full Label)
        items = [
            ("Dashboard", "⚡", "1. ⚡ Live Dashboard"),
            ("History", "📈", "2. 📈 Visual History"),
            ("Sensors", "🖥️", "3. 🖥️ Sensor Tree"),
            ("Cooling", "🛡️", "4. 🛡️ Smart Cooling"),
            ("License", "🔑", "5. 🔑 License & Key"),
            ("About", "👨‍💻", "6. 👨‍💻 Founder & Links"),
        ]

        for key, icon, label in items:
            btn = ctk.CTkButton(
                self.nav_container,
                text=label,
                height=38,
                corner_radius=8,
                anchor="w",
                fg_color="transparent",
                text_color=self.colors["text_secondary"],
                hover_color=self.colors["input_bg"],
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda k=key: self._on_btn_clicked(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = (btn, icon, label)

        self._highlight_active_nav()

        # Bottom Ecosystem Section
        self.bottom_frame = ctk.CTkFrame(self, fg_color=self.colors["input_bg"], corner_radius=8)
        self.bottom_frame.pack(fill="x", padx=10, pady=(8, 12))

        self.lbl_ecosystem = ctk.CTkLabel(
            self.bottom_frame,
            text="🌐 FrankBase Ecosystem",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["accent_blue"]
        )
        self.lbl_ecosystem.pack(pady=(6, 2))

        # Sister Website Link Buttons
        self.btn_store = ctk.CTkButton(
            self.bottom_frame,
            text="🛍️ Store & Products",
            height=26,
            corner_radius=4,
            fg_color="transparent",
            text_color=self.colors["text_primary"],
            hover_color=self.colors["card_bg"],
            font=ctk.CTkFont(size=10),
            command=lambda: webbrowser.open("https://store.frankbase.com")
        )
        self.btn_store.pack(fill="x", padx=6, pady=1)

        self.btn_founder = ctk.CTkButton(
            self.bottom_frame,
            text="👨‍💻 MasterManikant.com",
            height=26,
            corner_radius=4,
            fg_color="transparent",
            text_color=self.colors["text_primary"],
            hover_color=self.colors["card_bg"],
            font=ctk.CTkFont(size=10),
            command=lambda: webbrowser.open("https://mastermanikant.com")
        )
        self.btn_founder.pack(fill="x", padx=6, pady=(1, 6))

    def _on_btn_clicked(self, key: str):
        self.current_active_nav = key
        self._highlight_active_nav()
        if self.on_navigate:
            self.on_navigate(key)

    def _highlight_active_nav(self):
        for k, (btn, icon, label) in self.nav_buttons.items():
            if k == self.current_active_nav:
                btn.configure(
                    fg_color=self.colors["accent_blue"],
                    text_color="#ffffff"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors["text_secondary"]
                )

    def toggle_shrink_expand(self):
        """Toggles sidebar width between 240px (expanded) and 60px (collapsed)."""
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.configure(width=240)
            self.btn_toggle.configure(text="☰   MENU")
            self.bottom_frame.pack(fill="x", padx=10, pady=(8, 12))
            for k, (btn, icon, label) in self.nav_buttons.items():
                btn.configure(text=label, anchor="w", width=220)
        else:
            self.configure(width=62)
            self.btn_toggle.configure(text="☰")
            self.bottom_frame.pack_forget()
            for k, (btn, icon, label) in self.nav_buttons.items():
                btn.configure(text=icon, anchor="center", width=48)

    def refresh_theme(self):
        self.colors = ThemeManager.get_colors()
        self.configure(fg_color=self.colors["card_bg"])
        self.btn_toggle.configure(
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"]
        )
        self.bottom_frame.configure(fg_color=self.colors["input_bg"])
        self.lbl_ecosystem.configure(text_color=self.colors["accent_blue"])
        self._highlight_active_nav()