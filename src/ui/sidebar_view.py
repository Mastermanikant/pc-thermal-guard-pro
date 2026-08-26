"""
Left Sidebar Component (100% Matched with FrankBase Smart File Organizer Sidebar - Screenshots 2 & 3)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk
import webbrowser
import psutil
import threading
from typing import Callable
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, SIDEBAR_BG, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.ui.custom_dialog import show_custom_dialog

class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate_callback: Callable[[str], None], **kwargs):
        super().__init__(
            parent,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
            width=240,
            **kwargs
        )
        self.on_navigate = on_navigate_callback
        self.current_active_nav = "Dashboard"
        self.nav_buttons = {}

        self.grid_propagate(False)
        self._build_ui()

    def _build_ui(self):
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
            scrollbar_button_color=("#cccccc", "#333333"),
            scrollbar_button_hover_color=NEON_CYAN
        )
        self.sidebar_scroll.pack(fill="both", expand=True)

        # 1. Navigation Buttons (Numbered list matching Smart File Organizer)
        items = [
            ("Dashboard", "1. ⚡ Live Dashboard"),
            ("History", "2. 📈 Visual History"),
            ("Sensors", "3. 🖥️ Sensor Tree"),
            ("Cooling", "4. 🛡️ Smart Cooling"),
            ("License", "5. 🔑 License & Key"),
            ("About", "6. 👨‍💻 Founder & Links"),
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
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = btn

        self._highlight_active_nav()

        # 2. Settings / Cooling Profile Pill
        self.settings_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=10, pady=(6, 4))

        self.mode_var = ctk.StringVar(value="Balanced")
        self.m_btn = ctk.CTkSegmentedButton(
            self.settings_frame,
            values=["Eco", "Balanced", "Turbo"],
            variable=self.mode_var,
            selected_color=NEON_MAGENTA,
            selected_hover_color=NEON_MAGENTA,
            unselected_color=SIDEBAR_BG,
            unselected_hover_color=BORDER_COLOR,
            font=ctk.CTkFont(weight="bold", size=11),
            height=28
        )
        self.m_btn.pack(fill="x")

        # 3. Drives Live Storage Monitor (Dual Progress Bars matching Screenshots 2 & 3)
        self.drives_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        self.drives_frame.pack(fill="x", padx=10, pady=(8, 4))

        # Start drive monitor thread
        self.after(500, lambda: threading.Thread(target=self.update_drives_monitor, daemon=True).start())

        # 4. Drive Space Tip Card (Matching Screenshot 2/3)
        self.tip_card = ctk.CTkFrame(self.sidebar_scroll, fg_color=FRAME_BG, corner_radius=6, border_width=1, border_color=BORDER_COLOR)
        self.tip_card.pack(fill="x", padx=10, pady=(5, 8))

        tip_text = "💡 Tip: Keep at least 15-20% free space\non your C: Drive to prevent PC slowdowns."
        ctk.CTkLabel(self.tip_card, text=tip_text, font=ctk.CTkFont(size=10, slant="italic"), text_color=DYNAMIC_GRAY, justify="center").pack(pady=6, padx=6)

        # 5. Bottom Founder & Credibility Card (Matching Screenshots 2 & 3)
        self.bottom_controls = ctk.CTkFrame(self.sidebar_scroll, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        self.bottom_controls.pack(fill="x", padx=10, pady=(4, 15))

        ctk.CTkLabel(self.bottom_controls, text="Designed & Developed By:", font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY).pack(pady=(8, 0))
        ctk.CTkLabel(self.bottom_controls, text="Master Manikant Yadav", font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_COLOR).pack(pady=(2, 4))

        ctk.CTkButton(
            self.bottom_controls,
            text="MasterManikant.com",
            height=26,
            fg_color="transparent",
            border_width=1,
            border_color=NEON_CYAN,
            text_color=NEON_CYAN,
            hover_color="#003344",
            corner_radius=5,
            font=ctk.CTkFont(size=11),
            cursor="hand2",
            command=lambda: webbrowser.open("https://mastermanikant.com")
        ).pack(pady=(0, 4), padx=14, fill="x")

        privacy_text = "I don't give this app internet access\nso this is 100% privacy first."
        ctk.CTkLabel(self.bottom_controls, text=privacy_text, font=ctk.CTkFont(size=9, slant="italic"), text_color=DYNAMIC_GRAY).pack(pady=(2, 2))

        legal_lbl = ctk.CTkLabel(self.bottom_controls, text="📜 Legal Terms & Privacy Policy", font=ctk.CTkFont(size=10, underline=True), text_color=DYNAMIC_GRAY, cursor="hand2")
        legal_lbl.pack(pady=(0, 8))
        legal_lbl.bind("<Button-1>", lambda e: self._show_legal_modal())

    def _on_btn_clicked(self, key: str):
        self.current_active_nav = key
        self._highlight_active_nav()
        if self.on_navigate:
            self.on_navigate(key)

    def _highlight_active_nav(self):
        for k, btn in self.nav_buttons.items():
            if k == self.current_active_nav:
                # Glowing Neon Cyan Pill with black text (Screenshots 2 & 3)
                btn.configure(
                    fg_color=NEON_CYAN,
                    text_color="black"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_COLOR
                )

    def update_drives_monitor(self):
        try:
            partitions = psutil.disk_partitions()
            drive_data = []
            for p in partitions:
                if p.fstype and "cdrom" not in p.opts:
                    try:
                        usage = psutil.disk_usage(p.mountpoint)
                        used_gb = usage.used / (1024 ** 3)
                        free_gb = usage.free / (1024 ** 3)
                        free_percent = 100.0 - usage.percent
                        drive_name = p.device.replace("\\", "")
                        text = f"💽 {drive_name}  {used_gb:.1f} GB Used / {free_gb:.1f} GB Free\n({free_percent:.1f}% Free)"
                        drive_data.append((usage.percent, text))
                    except PermissionError:
                        pass

            self.after(0, self._render_drives_ui, drive_data)
        except Exception:
            pass

    def _render_drives_ui(self, drive_data):
        for widget in self.drives_frame.winfo_children():
            widget.destroy()

        for percent, text in drive_data:
            if percent >= 90:
                fill_col = "#FF0055"
            elif percent >= 75:
                fill_col = "#FF9900"
            else:
                fill_col = "#00FF66"

            pb = ctk.CTkProgressBar(self.drives_frame, height=10, corner_radius=5, fg_color="#333333", progress_color=fill_col)
            pb.pack(fill="x", padx=6, pady=(6, 2))
            pb.set(percent / 100.0)

            lbl = ctk.CTkLabel(self.drives_frame, text=text, font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT_COLOR, justify="center")
            lbl.pack(pady=(0, 6))

    def _show_legal_modal(self):
        msg = (
            "FrankBase Legal Terms & Privacy Commitment:\n\n"
            "• Zero Telemetry: No files, metrics, or personal data ever leave your PC.\n"
            "• Read-Only WHQL Telemetry: Safe hardware sensor polling without BIOS mods.\n"
            "• Offline RSA Licensing: 100% offline verification.\n\n"
            "Terms URL: mastermanikant.com/legal"
        )
        show_custom_dialog(self.winfo_toplevel(), "Legal Terms & Privacy", msg, icon="📜", link_url="https://mastermanikant.com/legal")

    def refresh_theme(self):
        self.configure(fg_color=SIDEBAR_BG)
        self.sidebar_scroll.configure(fg_color=SIDEBAR_BG)
        self.tip_card.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.bottom_controls.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self._highlight_active_nav()