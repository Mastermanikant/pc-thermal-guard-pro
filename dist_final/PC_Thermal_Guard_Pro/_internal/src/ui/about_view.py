"""
Developer, Ecosystem & Offline License Activation View
PC Thermal Guard Pro
"""
import customtkinter as ctk
import webbrowser
from src.ui.theme import ThemeManager
from src.core.machine_id import get_machine_hardware_id, copy_machine_id_to_clipboard
from src.core.licensing import LicenseManager

class AboutAndLicenseView(ctk.CTkScrollableFrame):
    def __init__(self, parent, toast_callback=None, **kwargs):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color="transparent",
            scrollbar_button_color=self.colors["border_color"],
            **kwargs
        )
        self.toast = toast_callback
        self.license_mgr = LicenseManager.get_instance()
        self._build_ui()

    def _build_ui(self):
        # Top Heading
        lbl_title = ctk.CTkLabel(
            self,
            text="🔑 License Activation & 👨‍💻 Developer Credibility",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 10))

        # --- Card 1: PC Hardware ID ("PC Number") ---
        card_hwid = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=10)
        card_hwid.pack(fill="x", padx=15, pady=8)

        lbl_hwid_title = ctk.CTkLabel(
            card_hwid,
            text="🖥️ Unique PC Machine ID (Your PC Number):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        lbl_hwid_title.pack(anchor="w", padx=15, pady=(12, 4))

        row_hwid = ctk.CTkFrame(card_hwid, fg_color="transparent")
        row_hwid.pack(fill="x", padx=15, pady=(2, 12))

        self.lbl_hwid_val = ctk.CTkLabel(
            row_hwid,
            text=get_machine_hardware_id(),
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.lbl_hwid_val.pack(side="left", padx=(0, 15))

        btn_copy_hwid = ctk.CTkButton(
            row_hwid,
            text="📋 Copy PC ID",
            width=120,
            height=32,
            corner_radius=6,
            fg_color=self.colors["accent_blue"],
            hover_color=self.colors["accent_cyan"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_copy_hwid
        )
        btn_copy_hwid.pack(side="left")

        # --- Card 2: 100% Offline RSA License Activation ---
        card_license = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=10)
        card_license.pack(fill="x", padx=15, pady=8)

        lbl_lic_title = ctk.CTkLabel(
            card_license,
            text="⭐ License Status & Pro Activation (100% Offline Key Validation):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent_blue"]
        )
        lbl_lic_title.pack(anchor="w", padx=15, pady=(12, 4))

        status_text = f"Current Tier: {self.license_mgr.get_license_tier_name()}"
        self.lbl_tier = ctk.CTkLabel(
            card_license,
            text=status_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors["status_optimal"] if self.license_mgr.is_pro_active() else self.colors["accent_amber"]
        )
        self.lbl_tier.pack(anchor="w", padx=15, pady=2)

        row_lic = ctk.CTkFrame(card_license, fg_color="transparent")
        row_lic.pack(fill="x", padx=15, pady=(8, 14))

        self.entry_key = ctk.CTkEntry(
            row_lic,
            placeholder_text="Enter your Pro License Key (e.g. FB-PRO-XXXX-XXXX)",
            height=36,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            border_color=self.colors["border_color"]
        )
        self.entry_key.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_activate = ctk.CTkButton(
            row_lic,
            text="⚡ Activate Pro",
            width=130,
            height=36,
            corner_radius=6,
            fg_color=self.colors["status_optimal"],
            hover_color="#059669",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_activate_license
        )
        btn_activate.pack(side="right")

        # --- Card 3: Founder Credibility & Developer Info ---
        card_founder = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=10)
        card_founder.pack(fill="x", padx=15, pady=8)

        lbl_dev_head = ctk.CTkLabel(
            card_founder,
            text="👨‍💻 Founder & System Architect:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        lbl_dev_head.pack(anchor="w", padx=15, pady=(12, 2))

        lbl_founder_name = ctk.CTkLabel(
            card_founder,
            text="Master Manikant Yadav (मास्टर मणिकान्त यादव)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        lbl_founder_name.pack(anchor="w", padx=15, pady=1)

        lbl_desk = ctk.CTkLabel(
            card_founder,
            text="Official Desk: connect@mastermanikant.com  |  FrankBase Ecosystem",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        lbl_desk.pack(anchor="w", padx=15, pady=(1, 12))

        # --- Card 4: Sister Ecosystem & Product Store Links ---
        card_links = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=10)
        card_links.pack(fill="x", padx=15, pady=(8, 20))

        lbl_links_title = ctk.CTkLabel(
            card_links,
            text="🌐 FrankBase Official Sister Ecosystem Portals:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["accent_blue"]
        )
        lbl_links_title.pack(anchor="w", padx=15, pady=(12, 6))

        grid_links = ctk.CTkFrame(card_links, fg_color="transparent")
        grid_links.pack(fill="x", padx=15, pady=(0, 14))

        links = [
            ("🌐 MasterManikant.com", "https://mastermanikant.com"),
            ("🛍️ FrankBase Digital Store", "https://store.frankbase.com"),
            ("🏢 FrankBase Agency", "https://digital.frankbase.com"),
            ("📚 EnglishVidya Hub", "https://englishvidya.com"),
            ("⭐ Leave Honest Review (Get 20p Bonus)", "https://store.frankbase.com/review"),
            ("🛡️ Anti-Piracy Bounty Program", "https://store.frankbase.com/report-piracy"),
        ]

        for i, (title, url) in enumerate(links):
            r = i // 2
            c = i % 2
            btn = ctk.CTkButton(
                grid_links,
                text=title,
                height=32,
                corner_radius=6,
                fg_color=self.colors["input_bg"],
                text_color=self.colors["text_primary"],
                hover_color=self.colors["accent_blue"],
                font=ctk.CTkFont(size=11),
                command=lambda u=url: webbrowser.open(u)
            )
            btn.grid(row=r, column=c, padx=5, pady=4, sticky="ew")

        grid_links.grid_columnconfigure(0, weight=1)
        grid_links.grid_columnconfigure(1, weight=1)

    def _on_copy_hwid(self):
        copy_machine_id_to_clipboard()
        if self.toast:
            self.toast("📋 PC Hardware ID copied to clipboard!")

    def _on_activate_license(self):
        key = self.entry_key.get().strip()
        success, msg = self.license_mgr.activate_license(key)
        if success:
            self.lbl_tier.configure(
                text=f"Current Tier: {self.license_mgr.get_license_tier_name()}",
                text_color=self.colors["status_optimal"]
            )
            if self.toast:
                self.toast("🎉 Pro Lifetime License Activated Successfully!")
        else:
            if self.toast:
                self.toast(f"❌ {msg}")