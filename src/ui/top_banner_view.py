"""
Top Collapsible Header & AI Quick-Tools Banner (Shrink/Expand)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Design Suite)
"""
import customtkinter as ctk
import webbrowser
from typing import Callable
from src.ui.theme import ThemeManager
from src.core.machine_id import get_machine_hardware_id, copy_machine_id_to_clipboard

class TopCollapsibleHeader(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_toggle_theme_callback: Callable[[], None],
        on_minimize_tray_callback: Callable[[], None],
        on_toast_callback: Callable[[str], None] = None,
        **kwargs
    ):
        self.colors = ThemeManager.get_colors()
        super().__init__(
            parent,
            fg_color=self.colors["card_bg"],
            corner_radius=0,
            border_width=1,
            border_color=self.colors["border_color"],
            **kwargs
        )
        self.on_toggle_theme = on_toggle_theme_callback
        self.on_minimize_tray = on_minimize_tray_callback
        self.toast = on_toast_callback
        self.hwid = get_machine_hardware_id()
        self.is_expanded = False

        self._build_ui()

    def _build_ui(self):
        # ── Primary Top Row (Always Visible) ──
        self.row_main = ctk.CTkFrame(self, fg_color="transparent", height=48)
        self.row_main.pack(fill="x", padx=12, pady=6)

        # 1. Left: Brand & Glowing Flame Shield
        self.lbl_logo = ctk.CTkLabel(
            self.row_main,
            text="⚡ PC THERMAL GUARD PRO",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        self.lbl_logo.pack(side="left", padx=(4, 10))

        # 2. PC Hardware ID ("PC Number") 1-Click Copy Pill
        self.btn_hwid = ctk.CTkButton(
            self.row_main,
            text=f"PC ID: {self.hwid} 📋",
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"],
            hover_color=self.colors["accent_blue"],
            border_width=1,
            border_color=self.colors["border_color"],
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            command=self._on_copy_hwid
        )
        self.btn_hwid.pack(side="left", padx=6)

        # 3. Live Thermal Chip
        self.chip_temp = ctk.CTkLabel(
            self.row_main,
            text="🌡️ 45.0°C | OPTIMAL",
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["status_optimal"],
            font=ctk.CTkFont(size=11, weight="bold"),
            padx=10
        )
        self.chip_temp.pack(side="left", padx=6)

        # 4. Right Controls: Tray, Theme, Expand Tools Button
        self.btn_tray = ctk.CTkButton(
            self.row_main,
            text="📥 Tray",
            width=70,
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_secondary"],
            hover_color=self.colors["accent_blue"],
            font=ctk.CTkFont(size=11),
            command=self.on_minimize_tray
        )
        self.btn_tray.pack(side="right", padx=(4, 4))

        self.btn_theme = ctk.CTkButton(
            self.row_main,
            text="🌙 Night" if ThemeManager.get_current_theme() == "dark" else "☀️ Day",
            width=76,
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"],
            hover_color=self.colors["accent_cyan"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.on_toggle_theme
        )
        self.btn_theme.pack(side="right", padx=4)

        # Top Drawer Toggle (Shrink/Expand Button)
        self.btn_tools_toggle = ctk.CTkButton(
            self.row_main,
            text="▼ AI & Search Tools",
            width=140,
            height=28,
            corner_radius=6,
            fg_color=self.colors["accent_blue"],
            text_color="#ffffff",
            hover_color=self.colors["accent_cyan"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.toggle_expand
        )
        self.btn_tools_toggle.pack(side="right", padx=6)

        # ── Collapsible Expandable Tools Panel (Hidden by Default) ──
        self.panel_expanded = ctk.CTkFrame(
            self,
            fg_color=self.colors["bg_secondary"],
            corner_radius=0,
            border_width=1,
            border_color=self.colors["border_color"]
        )

        # Build 2-Column AI & Search Quick Grid (Matching Smart File Organizer)
        self._build_expanded_tools()

    def _build_expanded_tools(self):
        col_container = ctk.CTkFrame(self.panel_expanded, fg_color="transparent")
        col_container.pack(fill="x", padx=12, pady=10)

        # Left Column: Web Search Engines
        col_left = ctk.CTkFrame(col_container, fg_color=self.colors["card_bg"], corner_radius=8, border_width=1, border_color=self.colors["border_color"])
        col_left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        ctk.CTkLabel(
            col_left,
            text="🔎 Web Research & Diagnostics (6 Engines)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", padx=10, pady=(6, 4))

        google_url = "https://www.google.com/search?q=PC+Thermal+Guard+Pro+MasterManikant+frankbase.com+hardware+cooling"
        google_ai_url = "https://www.google.com/search?q=how+to+reduce+cpu+thermal+throttling+frankbase.com&udm=50"
        bing_url = "https://www.bing.com/search?q=PC+Thermal+Guard+Pro+MasterManikant"
        ddg_url = "https://duckduckgo.com/?q=CPU+overheating+hardware+diagnostics+frankbase"
        brave_url = "https://search.brave.com/search?q=PC+Thermal+Guard+Pro+MasterManikant"
        store_url = "https://store.frankbase.com"

        r1 = ctk.CTkFrame(col_left, fg_color="transparent")
        r1.pack(fill="x", padx=8, pady=2)
        ctk.CTkButton(r1, text="🌐 Google", height=24, fg_color="#bf360c", hover_color="#9c2d0a", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(google_url)).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r1, text="🔮 Google AI", height=24, fg_color="#880e4f", hover_color="#6a0039", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(google_ai_url)).pack(side="left", expand=True, fill="x", padx=2)

        r2 = ctk.CTkFrame(col_left, fg_color="transparent")
        r2.pack(fill="x", padx=8, pady=2)
        ctk.CTkButton(r2, text="🔍 Bing", height=24, fg_color="#006064", hover_color="#00474a", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(bing_url)).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r2, text="🦆 DuckDuckGo", height=24, fg_color="#5d4037", hover_color="#4a2e24", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(ddg_url)).pack(side="left", expand=True, fill="x", padx=2)

        r3 = ctk.CTkFrame(col_left, fg_color="transparent")
        r3.pack(fill="x", padx=8, pady=(2, 8))
        ctk.CTkButton(r3, text="🦁 Brave", height=24, fg_color="#7b341e", hover_color="#5c2613", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(brave_url)).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r3, text="🛍️ FrankBase Store", height=24, fg_color=self.colors["accent_blue"], hover_color=self.colors["accent_cyan"], font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open(store_url)).pack(side="left", expand=True, fill="x", padx=2)

        # Right Column: AI Assistant Launchers
        col_right = ctk.CTkFrame(col_container, fg_color=self.colors["card_bg"], corner_radius=8, border_width=1, border_color=self.colors["border_color"])
        col_right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        ctk.CTkLabel(
            col_right,
            text="🤖 AI Diagnostic Launchers (Instant Query)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_secondary"]
        ).pack(anchor="w", padx=10, pady=(6, 4))

        ar1 = ctk.CTkFrame(col_right, fg_color="transparent")
        ar1.pack(fill="x", padx=8, pady=2)
        ctk.CTkButton(ar1, text="🤖 ChatGPT", height=24, fg_color="#0e8c6d", hover_color="#0a6e55", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://chatgpt.com")).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(ar1, text="✨ Gemini", height=24, fg_color="#1a4fa8", hover_color="#123c85", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://gemini.google.com")).pack(side="left", expand=True, fill="x", padx=2)

        ar2 = ctk.CTkFrame(col_right, fg_color="transparent")
        ar2.pack(fill="x", padx=8, pady=2)
        ctk.CTkButton(ar2, text="🧠 Claude", height=24, fg_color="#7c4a00", hover_color="#5e3800", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://claude.ai")).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(ar2, text="🔍 Perplexity", height=24, fg_color="#0e6b7a", hover_color="#0a5260", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://www.perplexity.ai")).pack(side="left", expand=True, fill="x", padx=2)

        ar3 = ctk.CTkFrame(col_right, fg_color="transparent")
        ar3.pack(fill="x", padx=8, pady=(2, 8))
        ctk.CTkButton(ar3, text="🤝 Copilot", height=24, fg_color="#0050a0", hover_color="#003d7a", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://copilot.microsoft.com")).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(ar3, text="🐋 DeepSeek", height=24, fg_color="#004d5e", hover_color="#003844", font=ctk.CTkFont(size=10, weight="bold"), corner_radius=4, command=lambda: webbrowser.open("https://chat.deepseek.com")).pack(side="left", expand=True, fill="x", padx=2)

    def toggle_expand(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.btn_tools_toggle.configure(text="▲ Hide AI Tools")
            self.panel_expanded.pack(fill="x", padx=0, pady=0)
        else:
            self.btn_tools_toggle.configure(text="▼ AI & Search Tools")
            self.panel_expanded.pack_forget()

    def update_live_temp(self, temp: float, status: str):
        color = self.colors["status_optimal"]
        if temp >= 80.0:
            color = self.colors["status_critical"]
        elif temp >= 65.0:
            color = self.colors["status_elevated"]

        self.chip_temp.configure(
            text=f"🌡️ {temp:.1f}°C | {status.upper()}",
            text_color=color
        )

    def _on_copy_hwid(self):
        copy_machine_id_to_clipboard()
        if self.toast:
            self.toast(f"📋 PC ID ({self.hwid}) copied to clipboard!")

    def refresh_theme(self):
        self.colors = ThemeManager.get_colors()
        self.configure(fg_color=self.colors["card_bg"], border_color=self.colors["border_color"])
        self.row_main.configure(fg_color="transparent")
        self.lbl_logo.configure(text_color=self.colors["accent_cyan"])
        self.btn_hwid.configure(
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border_color"]
        )
        self.chip_temp.configure(fg_color=self.colors["input_bg"])
        self.btn_tray.configure(
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_secondary"]
        )
        self.btn_theme.configure(
            text="🌙 Night" if ThemeManager.get_current_theme() == "dark" else "☀️ Day",
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"]
        )
        self.btn_tools_toggle.configure(
            fg_color=self.colors["accent_blue"],
            hover_color=self.colors["accent_cyan"]
        )
        self.panel_expanded.configure(
            fg_color=self.colors["bg_secondary"],
            border_color=self.colors["border_color"]
        )