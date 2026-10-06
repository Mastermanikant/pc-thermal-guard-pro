"""
Bottom Ecosystem Banner Component
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import os
import customtkinter as ctk
import webbrowser
from PIL import Image
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, FRAME_BG, BORDER_COLOR, DYNAMIC_GRAY, TEXT_COLOR
from src.ui.legal_modal import show_legal_privacy_modal

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
        # Header Row: Clickable everywhere to Toggle Expand/Minimize
        self.header_row = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.header_row.pack(fill="x", padx=15, pady=(6, 6))
        self.header_row.bind("<Button-1>", lambda e: self.toggle_minimize())

        self.lbl_title = ctk.CTkLabel(
            self.header_row,
            text="✽ Frank Base System Utility Suite",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NEON_CYAN,
            cursor="hand2"
        )
        self.lbl_title.pack(side="left")
        self.lbl_title.bind("<Button-1>", lambda e: self.toggle_minimize())

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
            cursor="hand2",
            command=self.toggle_minimize
        )
        self.btn_toggle_min.pack(side="right")

        # Body Container (Hidden by default because is_minimized=True)
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")

        # Row 1: Developer Avatar + Info on Left, Official CTA Buttons on Right
        row1 = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(2, 4))

        dev_container = ctk.CTkFrame(row1, fg_color="transparent")
        dev_container.pack(side="left", anchor="w")

        # Load developer.webp avatar safely
        try:
            asset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))
            avatar_path = os.path.join(asset_dir, "developer.webp")
            if os.path.exists(avatar_path):
                self.avatar_img = ctk.CTkImage(
                    light_image=Image.open(avatar_path),
                    dark_image=Image.open(avatar_path),
                    size=(52, 52)
                )
                self.lbl_avatar = ctk.CTkLabel(dev_container, image=self.avatar_img, text="")
                self.lbl_avatar.pack(side="left", padx=(0, 10))
        except Exception:
            pass

        dev_box = ctk.CTkFrame(dev_container, fg_color="transparent")
        dev_box.pack(side="left", anchor="w")

        ctk.CTkLabel(dev_box, text="Developed by", font=ctk.CTkFont(size=10), text_color=DYNAMIC_GRAY).pack(anchor="w")
        ctk.CTkLabel(dev_box, text="Master Manikant Yadav", font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_COLOR).pack(anchor="w")
        ctk.CTkLabel(dev_box, text="Founder @ FrankBase | Precision First Tools", font=ctk.CTkFont(size=10), text_color=NEON_CYAN).pack(anchor="w")

        # Right CTA Box with action buttons
        cta_box = ctk.CTkFrame(row1, fg_color="transparent")
        cta_box.pack(side="right", anchor="e")

        ctk.CTkButton(
            cta_box,
            text="🌐 Founder Portal",
            height=28,
            corner_radius=6,
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: webbrowser.open("https://mastermanikant.com")
        ).pack(side="right", padx=(6, 0))

        ctk.CTkButton(
            cta_box,
            text="📜 Legal & Privacy",
            height=28,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color=NEON_CYAN,
            hover_color="#003344",
            text_color=NEON_CYAN,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._open_legal_modal
        ).pack(side="right", padx=0)

        # Bio Paragraph
        bio_text = "Built with a local-first philosophy: Zero telemetry, zero bloat, high precision hardware monitoring."
        ctk.CTkLabel(self.body_frame, text=bio_text, font=ctk.CTkFont(size=11), text_color=DYNAMIC_GRAY, anchor="w", justify="left").pack(fill="x", pady=(4, 6))

        # Direct links row
        links_row = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        links_row.pack(fill="x", pady=(0, 4))

        ctk.CTkButton(
            links_row,
            text="🔗 mastermanikant.com",
            height=24,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=DYNAMIC_GRAY,
            hover_color="#222222",
            corner_radius=5,
            font=ctk.CTkFont(size=10),
            cursor="hand2",
            command=lambda: webbrowser.open("https://mastermanikant.com")
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            links_row,
            text="🔗 frankbase.com/products",
            height=24,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=DYNAMIC_GRAY,
            hover_color="#222222",
            corner_radius=5,
            font=ctk.CTkFont(size=10),
            cursor="hand2",
            command=lambda: webbrowser.open("https://frankbase.com/products")
        ).pack(side="left")

        # Footer Row: Version and Contact
        footer_text = "Version 1.0.0 Beta | © 2026 FrankBase Suite | connect@mastermanikant.com"
        ctk.CTkLabel(self.body_frame, text=footer_text, font=ctk.CTkFont(size=9), text_color=DYNAMIC_GRAY, anchor="w").pack(fill="x", pady=(4, 0))

    def _open_legal_modal(self):
        show_legal_privacy_modal(self.winfo_toplevel(), on_toast_callback=self.toast)

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