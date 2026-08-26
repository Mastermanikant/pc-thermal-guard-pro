"""
Custom Floating Modal Dialog Component (100% Matched with Smart File Organizer Screenshot 4)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk
import webbrowser
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, FRAME_BG, BORDER_COLOR, DYNAMIC_GRAY, TEXT_COLOR

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message, is_confirm=False, icon="🛡️", link_url=None, link_text=None):
        super().__init__(master)
        self.title(title)
        self.result = False

        if not link_url and "frankbase.com" in message.lower():
            link_url = "https://frankbase.com/pcthermalguard"
            link_text = "🌐 Visit frankbase.com/pcthermalguard ↗"

        dlg_w = 660
        dlg_h = 520 if link_url else 440
        self.geometry(f"{dlg_w}x{dlg_h}")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Center on master
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        try:
            if master and master.winfo_ismapped() and master.winfo_width() > 300:
                x = master.winfo_x() + (master.winfo_width() - dlg_w) // 2
                y = master.winfo_y() + (master.winfo_height() - dlg_h) // 2
            else:
                x = (screen_w - dlg_w) // 2
                y = (screen_h - dlg_h) // 2
        except Exception:
            x = (screen_w - dlg_w) // 2
            y = (screen_h - dlg_h) // 2

        self.geometry(f"{dlg_w}x{dlg_h}+{max(0, x)}+{max(0, y)}")

        # Top Big Icon / Avatar
        ctk.CTkLabel(self, text=icon, font=ctk.CTkFont(size=44)).pack(pady=(16, 2))

        # Message Container
        msg_frame = ctk.CTkFrame(self, fg_color="transparent")
        msg_frame.pack(fill="x", padx=35, pady=(5, 10))

        sections = [s.strip() for s in message.split("\n\n") if s.strip()]
        for idx, sec in enumerate(sections):
            lbl_pady = (0, 8) if idx < len(sections) - 1 else (0, 0)
            ctk.CTkLabel(
                msg_frame,
                text=sec,
                font=ctk.CTkFont(size=12),
                wraplength=dlg_w - 90,
                justify="left" if "•" in sec or "Tip:" in sec else "center",
                anchor="w" if "•" in sec or "Tip:" in sec else "center"
            ).pack(fill="x", pady=lbl_pady)

        # Clickable Website Link Button (Cyan Outline)
        if link_url:
            btn_link_text = link_text or "🌐 Visit frankbase.com/products ↗"
            def on_link_click():
                try:
                    webbrowser.open(link_url)
                except Exception:
                    pass
                self.result = True
                self.destroy()

            btn_link = ctk.CTkButton(
                self,
                text=btn_link_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="transparent",
                border_width=1,
                border_color=NEON_CYAN,
                text_color=NEON_CYAN,
                hover_color="#003344",
                corner_radius=6,
                height=34,
                command=on_link_click
            )
            btn_link.pack(padx=40, pady=(4, 12), fill="x")

        # Bottom Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(5, 15))

        if is_confirm:
            ctk.CTkButton(
                btn_frame,
                text="Yes, Proceed 🚀",
                fg_color=NEON_MAGENTA,
                hover_color="#c00060",
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=140,
                height=38,
                corner_radius=8,
                command=self._on_confirm
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                btn_frame,
                text="Cancel ❌",
                fg_color="transparent",
                border_width=1,
                border_color="#c0392b",
                text_color="#c0392b",
                hover_color="#e74c3c",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=120,
                height=38,
                corner_radius=8,
                command=self._on_cancel
            ).pack(side="left", padx=10)
        else:
            ctk.CTkButton(
                btn_frame,
                text="Awesome! 🚀",
                fg_color=NEON_MAGENTA,
                hover_color="#c00060",
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=160,
                height=38,
                corner_radius=8,
                command=self._on_confirm
            ).pack()

        self.grab_set()

    def _on_confirm(self):
        self.result = True
        self.destroy()

    def _on_cancel(self):
        self.result = False
        self.destroy()

def show_custom_dialog(master, title, message, is_confirm=False, icon="🛡️", link_url=None, link_text=None) -> bool:
    dlg = CustomDialog(master, title, message, is_confirm, icon, link_url, link_text)
    master.wait_window(dlg)
    return getattr(dlg, 'result', False)