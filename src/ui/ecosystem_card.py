"""
Bottom Ecosystem Banner Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import customtkinter as ctk
import webbrowser
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, FRAME_BG, BORDER_COLOR, DYNAMIC_GRAY, TEXT_COLOR

class EcosystemBannerCard(ctk.CTkFrame):
    def __init__(self, parent, on_toast_callback=None, **kwargs):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color=FRAME_BG,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR,
            **kwargs
        )
        self.toast = on_toast_callback
        self.is_minimized = True

        self._build_ui()

    def _build_ui(self):
        # Header Row: Title on Left, Minimize/Expand Button on Right
        self.header_row = ctk.CTkFrame(self, fg_color="transparent")
        self.header_row.pack(fill="x", padx=15, pady=(6, 6))

        self.lbl_title = ctk.CTkLabel(
            self.header_row,
            text="✽ FrankBase System Utility Suite",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NEON_CYAN
        )
        self.lbl_title.pack(side="left")

        self.btn_toggle_min = ctk.CTkButton(
            self.header_row,
            text="▶ Expand",
            width=80,
            height=22,
            corner_radius=6,
            fg_color="#333333",
            text_color="#ffffff",
            hover_color="#444444",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self.toggle_minimize
        )
        self.btn_toggle_min.pack(side="right")

        # Body Container (Hidden by default because is_minimized=True)
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Row 1: Founder info on Left, "Official Desk" CTA on Right
        row1 = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(2, 4))

        dev_box = ctk.CTkFrame(row1, fg_color="transparent")
        dev_box.pack(side="left", anchor="w")

        ctk.CTkLabel(dev_box, text="Developed by", font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY).pack(anchor="w")
        ctk.CTkLabel(dev_box, text="Master Manikant Yadav", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w", pady=(1, 1))
        ctk.CTkLabel(dev_box, text="Founder @ FrankBase | Precision First Tools", font=ctk.CTkFont(size=11), text_color=NEON_CYAN).pack(anchor="w")

        # Right CTA Box
        cta_box = ctk.CTkFrame(row1, fg_color="transparent")
        cta_box.pack(side="right", anchor="e")

        btn_discuss = ctk.CTkButton(
            cta_box,
            text="🌐 Official Portal",
            height=28,
            corner_radius=6,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: webbrowser.open("https://mastermanikant.com")
        )
        btn_discuss.pack(anchor="e")

        # Bio Paragraph
        bio_text = "Built with a local-first philosophy: Zero telemetry, zero bloat, high precision hardware monitoring."
        ctk.CTkLabel(self.body_frame, text=bio_text, font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY, anchor="w", justify="left").pack(fill="x", pady=(4, 6))

        # Footer Row: Version and Legal
        footer_text = "Version 1.0.0 Beta | © 2026 FrankBase Suite | connect@mastermanikant.com"
        ctk.CTkLabel(self.body_frame, text=footer_text, font=ctk.CTkFont(size=9), text_color=DYNAMIC_GRAY, anchor="w").pack(fill="x", pady=(4, 0))

    def toggle_minimize(self):
        self.is_minimized = not self.is_minimized
        if self.is_minimized:
            self.body_frame.pack_forget()
            self.btn_toggle_min.configure(text="▶ Expand")
        else:
            self.body_frame.pack(fill="x", padx=15, pady=(0, 10))
            self.btn_toggle_min.configure(text="▼ Minimize")

    def refresh_theme(self):
        self.configure(fg_color=FRAME_BG, border_color=BORDER_COLOR)
        self.lbl_title.configure(text_color=NEON_CYAN)