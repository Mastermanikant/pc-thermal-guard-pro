"""
Developer, Ecosystem & Offline License Activation View
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import os
import platform
import psutil
import customtkinter as ctk
import webbrowser
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, BG_COLOR, FRAME_BG, BORDER_COLOR, TEXT_COLOR, DYNAMIC_GRAY
from src.core.machine_id import get_machine_hardware_id, copy_machine_id_to_clipboard
from src.core.licensing import LicenseManager
from src.core.logger import get_log_file_path

class AboutAndLicenseView(ctk.CTkScrollableFrame):
    def __init__(self, parent, toast_callback=None, **kwargs):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color=BG_COLOR,
            corner_radius=0,
            scrollbar_button_color=("#cccccc", "#333333"),
            scrollbar_button_hover_color=NEON_CYAN,
            **kwargs
        )
        self.toast = toast_callback
        self.license_mgr = LicenseManager.get_instance()
        self.hwid = get_machine_hardware_id()
        self._build_ui()

    def _build_ui(self):
        # ── Heading ──
        lbl_title = ctk.CTkLabel(
            self,
            text="🔑 License Activation & 👨‍💻 Support Center",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_COLOR
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 8))

        # ── Card 1 (RANK 1 / TOP PRIORITY): 30-Day Beta Trial & Pro Activation ──
        card_license = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        card_license.pack(fill="x", padx=15, pady=6)

        lic_hdr = ctk.CTkFrame(card_license, fg_color="transparent")
        lic_hdr.pack(fill="x", padx=18, pady=(14, 4))

        lbl_lic_title = ctk.CTkLabel(
            lic_hdr,
            text="⭐ License Status & 1-Click 30-Day Beta Activation:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        )
        lbl_lic_title.pack(side="left")

        status_text = f"{self.license_mgr.get_license_tier_name()}"
        self.lbl_tier = ctk.CTkLabel(
            lic_hdr,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#003311" if self.license_mgr.is_pro_active() else "#3b2005",
            text_color=NEON_GREEN if self.license_mgr.is_pro_active() else "#f59e0b",
            corner_radius=6,
            padx=8,
            pady=3
        )
        self.lbl_tier.pack(side="right")

        ctk.CTkLabel(
            card_license,
            text="Get started immediately with 100% free offline community beta access for 30 days, or activate your permanent Pro Lifetime Key:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left",
            wraplength=660
        ).pack(anchor="w", padx=18, pady=(4, 10))

        # Web Key Generation CTA Row (Direct Web Link with pre-filled Device ID)
        row_quick_beta = ctk.CTkFrame(card_license, fg_color=BG_COLOR, corner_radius=8, border_width=1, border_color=BORDER_COLOR)
        row_quick_beta.pack(fill="x", padx=18, pady=(0, 10))

        beta_inner = ctk.CTkFrame(row_quick_beta, fg_color="transparent")
        beta_inner.pack(fill="x", padx=12, pady=10)

        beta_text_box = ctk.CTkFrame(beta_inner, fg_color="transparent")
        beta_text_box.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            beta_text_box,
            text="🌐 Generate 30-Day Free Key on Website (Zero Information Required)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NEON_CYAN,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            beta_text_box,
            text="Click below: Opens portal with your Device ID pre-filled. Click 'Generate' to auto-copy key, then paste it here.",
            font=ctk.CTkFont(size=10),
            text_color=DYNAMIC_GRAY,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        btn_auto_beta = ctk.CTkButton(
            beta_inner,
            text="🔑 Get Free 30-Day Key Online ↗",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=NEON_MAGENTA,
            hover_color="#c00060",
            text_color="white",
            corner_radius=6,
            height=34,
            command=self._open_web_key_generator
        )
        btn_auto_beta.pack(side="right", padx=(10, 0))

        # Manual Key Entry Row
        row_lic = ctk.CTkFrame(card_license, fg_color="transparent")
        row_lic.pack(fill="x", padx=18, pady=(4, 14))

        self.entry_key = ctk.CTkEntry(
            row_lic,
            placeholder_text="Enter your Pro or Beta License Key (e.g. FB-PRO-XXXX-XXXX)",
            height=36,
            corner_radius=6,
            fg_color=BG_COLOR,
            border_color=BORDER_COLOR
        )
        self.entry_key.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_activate = ctk.CTkButton(
            row_lic,
            text="⚡ Activate Key",
            width=130,
            height=36,
            corner_radius=6,
            fg_color="#059669",
            hover_color="#047857",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_activate_license
        )
        btn_activate.pack(side="right")

        # ── Card 2 (RANK 2): Unique PC Hardware ID (Device ID) ──
        card_hwid = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        card_hwid.pack(fill="x", padx=15, pady=6)

        lbl_hwid_title = ctk.CTkLabel(
            card_hwid,
            text="🖥️ Unique Device Hardware ID (Machine Fingerprint):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=NEON_CYAN
        )
        lbl_hwid_title.pack(anchor="w", padx=18, pady=(12, 4))

        row_hwid = ctk.CTkFrame(card_hwid, fg_color="transparent")
        row_hwid.pack(fill="x", padx=18, pady=(2, 6))

        self.lbl_hwid_val = ctk.CTkLabel(
            row_hwid,
            text=self.hwid,
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.lbl_hwid_val.pack(side="left", padx=(0, 15))

        btn_copy_hwid = ctk.CTkButton(
            row_hwid,
            text="📋 Copy Device ID",
            width=130,
            height=30,
            corner_radius=6,
            fg_color=NEON_CYAN,
            hover_color="#00b0ff",
            text_color="black",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_copy_hwid
        )
        btn_copy_hwid.pack(side="left")

        ctk.CTkLabel(
            card_hwid,
            text="• 100% offline hardware identification locked to CPU & Motherboard. Never transmitted anywhere without your permission.",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=DYNAMIC_GRAY
        ).pack(anchor="w", padx=18, pady=(0, 10))

        # ── Card 3 (RANK 3): Community Feedback & 50% Lifetime Pro Discount ──
        card_discount = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        card_discount.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            card_discount,
            text="🎁 Community Feedback & 50% Lifetime Pro Discount:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(12, 4))

        disc_desc = (
            "We value honest user feedback over fake ratings. Share 1-2 quick suggestions or feature requests on our official portal "
            "and receive a 50% discount coupon locked to this PC's Device ID."
        )
        ctk.CTkLabel(
            card_discount,
            text=disc_desc,
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            justify="left",
            wraplength=660
        ).pack(anchor="w", padx=18, pady=(0, 10))

        btn_claim_disc = ctk.CTkButton(
            card_discount,
            text="🌐 Share 2-Min Feedback & Claim Discount ↗",
            height=32,
            corner_radius=6,
            fg_color=BG_COLOR,
            border_width=1,
            border_color=BORDER_COLOR,
            hover_color="#003344",
            text_color=NEON_CYAN,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._open_discount_portal
        )
        btn_claim_disc.pack(padx=18, pady=(0, 12), fill="x")

        # ── Card 4 (RANK 4): Diagnostics Logs & Developer Support ──
        card_logs = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        card_logs.pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            card_logs,
            text="🛠️ Diagnostic Logs & Developer Support:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", padx=18, pady=(12, 4))

        ctk.CTkLabel(
            card_logs,
            text="If you experience any sensor errors or unexpected behavior, you can easily open your local log files or copy system debug info to share with our support desk:",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY,
            wraplength=660,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(0, 10))

        row_log_btns = ctk.CTkFrame(card_logs, fg_color="transparent")
        row_log_btns.pack(fill="x", padx=18, pady=(0, 14))

        btn_open_logs = ctk.CTkButton(
            row_log_btns,
            text="📂 Open Logs Folder",
            height=32,
            corner_radius=6,
            fg_color=BG_COLOR,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            hover_color="#003344",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_open_logs_folder
        )
        btn_open_logs.pack(side="left", padx=(0, 8))

        btn_copy_debug = ctk.CTkButton(
            row_log_btns,
            text="📋 Copy Debug System Info",
            height=32,
            corner_radius=6,
            fg_color=BG_COLOR,
            border_width=1,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            hover_color="#003344",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_copy_debug_info
        )
        btn_copy_debug.pack(side="left")

        # ── Card 5 (RANK 5): Founder Credibility & Official Links ──
        card_founder = ctk.CTkFrame(self, fg_color=FRAME_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        card_founder.pack(fill="x", padx=15, pady=(6, 20))

        lbl_dev_head = ctk.CTkLabel(
            card_founder,
            text="👨‍💻 Founder & System Architect:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        )
        lbl_dev_head.pack(anchor="w", padx=18, pady=(12, 2))

        lbl_founder_name = ctk.CTkLabel(
            card_founder,
            text="Master Manikant Yadav (मास्टर मणिकान्त यादव)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=NEON_CYAN
        )
        lbl_founder_name.pack(anchor="w", padx=18, pady=1)

        lbl_desk = ctk.CTkLabel(
            card_founder,
            text="Official Desk: connect@mastermanikant.com  |  FrankBase Ecosystem",
            font=ctk.CTkFont(size=11),
            text_color=DYNAMIC_GRAY
        )
        lbl_desk.pack(anchor="w", padx=18, pady=(1, 8))

        row_links = ctk.CTkFrame(card_founder, fg_color="transparent")
        row_links.pack(fill="x", padx=18, pady=(2, 14))

        ctk.CTkButton(
            row_links,
            text="🌐 MasterManikant.com",
            height=32,
            corner_radius=6,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            hover_color="#003344",
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=11),
            command=lambda: webbrowser.open("https://mastermanikant.com")
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            row_links,
            text="🛍️ FrankBase Digital Store",
            height=32,
            corner_radius=6,
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            hover_color="#003344",
            border_width=1,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=11),
            command=lambda: webbrowser.open("https://store.frankbase.com")
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _open_web_key_generator(self):
        """Opens official web portal with Device ID automatically passed in URL."""
        url = f"https://store.frankbase.com/pc-thermal-guard-pro-trial?device_id={self.hwid}"
        try:
            webbrowser.open(url)
        except Exception:
            pass
        if self.toast:
            self.toast("🌐 Opening key generator with your Device ID...")

    def _on_copy_hwid(self):
        copy_machine_id_to_clipboard()
        if self.toast:
            self.toast("📋 Device ID copied to clipboard!")

    def _open_discount_portal(self):
        url = self.license_mgr.get_feedback_discount_url()
        try:
            webbrowser.open(url)
        except Exception:
            pass
        if self.toast:
            self.toast("🌐 Opening Feedback page with Device ID...")

    def _on_activate_license(self):
        key = self.entry_key.get().strip()
        success, msg = self.license_mgr.activate_license(key)
        if success:
            self.lbl_tier.configure(
                text=f"{self.license_mgr.get_license_tier_name()}",
                text_color=NEON_GREEN,
                fg_color="#003311"
            )
            if self.toast:
                self.toast("🎉 License Activated Successfully!")
        else:
            if self.toast:
                self.toast(f"❌ {msg}")

    def _on_open_logs_folder(self):
        log_file = get_log_file_path()
        log_dir = os.path.dirname(log_file)
        if os.path.exists(log_dir):
            try:
                os.startfile(log_dir)
                if self.toast:
                    self.toast(f"📂 Opened Logs folder: {log_dir}")
            except Exception as e:
                if self.toast:
                    self.toast(f"⚠️ Error opening folder: {e}")
        else:
            if self.toast:
                self.toast("Log folder not found yet.")

    def _on_copy_debug_info(self):
        cpu_name = platform.processor() or "Unknown CPU"
        os_ver = f"{platform.system()} {platform.release()} (Build {platform.version()})"
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        log_file = get_log_file_path()

        debug_text = (
            f"=== PC Thermal Guard Pro Debug Info ===\n"
            f"Device ID: {self.hwid}\n"
            f"License Status: {self.license_mgr.get_license_tier_name()}\n"
            f"OS: {os_ver}\n"
            f"CPU: {cpu_name} ({psutil.cpu_count(logical=True)} Cores)\n"
            f"RAM: {ram_gb} GB\n"
            f"Log File: {log_file}\n"
            f"App Version: 1.0.0 Beta\n"
            f"Support Desk: connect@mastermanikant.com\n"
            f"========================================"
        )

        try:
            import pyperclip
            pyperclip.copy(debug_text)
        except Exception:
            try:
                import subprocess
                p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                p.communicate(input=debug_text.encode('utf-8'))
            except Exception:
                pass

        if self.toast:
            self.toast("📋 Debug System Info copied to clipboard!")