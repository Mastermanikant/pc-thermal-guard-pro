"""
Collapsible Left Sidebar with Drive/RAM Telemetry & Mode Pills
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Design Suite)
"""
import customtkinter as ctk
import webbrowser
import psutil
from typing import Callable
from src.ui.theme import ThemeManager

class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate_callback: Callable[[str], None], **kwargs):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color=self.colors["sidebar_bg"],
            corner_radius=0,
            width=240,
            border_width=1,
            border_color=self.colors["border_color"],
            **kwargs
        )
        self.on_navigate = on_navigate_callback
        self.is_expanded = True
        self.current_active_nav = "Dashboard"
        self.nav_buttons = {}

        self.grid_propagate(False)
        self._build_ui()

    def _build_ui(self):
        # 1. Top Toggle Button
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 6))

        self.btn_toggle = ctk.CTkButton(
            self.header_frame,
            text="☰   NAVIGATION",
            height=32,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"],
            hover_color=self.colors["card_bg_hover"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.toggle_shrink_expand
        )
        self.btn_toggle.pack(fill="x")

        # 2. Scrollable Navigation Section
        self.nav_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=self.colors["border_color"],
            scrollbar_button_hover_color=self.colors["accent_cyan"]
        )
        self.nav_container.pack(fill="both", expand=True, padx=6, pady=2)

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
                height=36,
                corner_radius=6,
                anchor="w",
                fg_color="transparent",
                text_color=self.colors["text_secondary"],
                hover_color=self.colors["input_bg"],
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda k=key: self._on_btn_clicked(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = (btn, icon, label)

        self._highlight_active_nav()

        # 3. Cooling Profile Mode Segmented Pill (Matching Smart File Organizer Move/Copy Mode Pill)
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(fill="x", padx=10, pady=(6, 4))

        self.lbl_profile = ctk.CTkLabel(
            self.mode_frame,
            text="⚡ Cooling Profile:",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["text_secondary"]
        )
        self.lbl_profile.pack(anchor="w", padx=2, pady=1)

        self.profile_var = ctk.StringVar(value="Balanced")
        self.btn_profile_seg = ctk.CTkSegmentedButton(
            self.mode_frame,
            values=["Eco", "Balanced", "Turbo"],
            variable=self.profile_var,
            height=26,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            selected_color=self.colors["accent_blue"],
            selected_hover_color=self.colors["accent_cyan"],
            unselected_color=self.colors["card_bg"],
            unselected_hover_color=self.colors["card_bg_hover"],
            font=ctk.CTkFont(size=10, weight="bold")
        )
        self.btn_profile_seg.pack(fill="x", pady=2)

        # 4. Storage & RAM Live Mini Monitor (Matching Smart File Organizer Drive Monitor)
        self.drives_card = ctk.CTkFrame(self, fg_color=self.colors["input_bg"], corner_radius=6)
        self.drives_card.pack(fill="x", padx=10, pady=4)

        self.lbl_ram = ctk.CTkLabel(
            self.drives_card,
            text="RAM Usage: 0%",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.lbl_ram.pack(anchor="w", padx=8, pady=(4, 1))

        self.bar_ram = ctk.CTkProgressBar(
            self.drives_card,
            height=6,
            corner_radius=3,
            fg_color=self.colors["gauge_bg"],
            progress_color=self.colors["accent_cyan"]
        )
        self.bar_ram.pack(fill="x", padx=8, pady=(0, 6))

        # 5. Smart Tip Card (Matching Smart File Organizer Tip Card)
        self.tip_card = ctk.CTkFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=6,
            border_width=1,
            border_color=self.colors["border_color"]
        )
        self.tip_card.pack(fill="x", padx=10, pady=(4, 10))

        tip_text = "💡 Tip: CPU load >70°C under low load indicates dried thermal paste or dust."
        self.lbl_tip = ctk.CTkLabel(
            self.tip_card,
            text=tip_text,
            font=ctk.CTkFont(size=9, slant="italic"),
            text_color=self.colors["text_muted"],
            wraplength=210,
            justify="left"
        )
        self.lbl_tip.pack(padx=6, pady=6)

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
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.configure(width=240)
            self.btn_toggle.configure(text="☰   NAVIGATION")
            self.mode_frame.pack(fill="x", padx=10, pady=(6, 4))
            self.drives_card.pack(fill="x", padx=10, pady=4)
            self.tip_card.pack(fill="x", padx=10, pady=(4, 10))
            for k, (btn, icon, label) in self.nav_buttons.items():
                btn.configure(text=label, anchor="w", width=220)
        else:
            self.configure(width=62)
            self.btn_toggle.configure(text="☰")
            self.mode_frame.pack_forget()
            self.drives_card.pack_forget()
            self.tip_card.pack_forget()
            for k, (btn, icon, label) in self.nav_buttons.items():
                btn.configure(text=icon, anchor="center", width=48)

    def update_resource_bars(self):
        try:
            ram_pct = psutil.virtual_memory().percent
            if self.is_expanded:
                self.lbl_ram.configure(text=f"RAM Usage: {ram_pct:.1f}%")
                self.bar_ram.set(ram_pct / 100.0)
        except Exception:
            pass

    def refresh_theme(self):
        self.colors = ThemeManager.get_colors()
        self.configure(fg_color=self.colors["sidebar_bg"], border_color=self.colors["border_color"])
        self.btn_toggle.configure(
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"]
        )
        self.lbl_profile.configure(text_color=self.colors["text_secondary"])
        self.btn_profile_seg.configure(
            fg_color=self.colors["input_bg"],
            selected_color=self.colors["accent_blue"],
            unselected_color=self.colors["card_bg"]
        )
        self.drives_card.configure(fg_color=self.colors["input_bg"])
        self.lbl_ram.configure(text_color=self.colors["text_primary"])
        self.bar_ram.configure(
            fg_color=self.colors["gauge_bg"],
            progress_color=self.colors["accent_cyan"]
        )
        self.tip_card.configure(
            fg_color=self.colors["card_bg"],
            border_color=self.colors["border_color"]
        )
        self.lbl_tip.configure(text_color=self.colors["text_muted"])
        self._highlight_active_nav()