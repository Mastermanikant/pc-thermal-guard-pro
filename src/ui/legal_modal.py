"""
Legal Terms, Privacy Policy & AI Verification Modal
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import os
import customtkinter as ctk
import webbrowser
from src.ui.theme import ThemeManager, NEON_CYAN, NEON_MAGENTA, FRAME_BG, BORDER_COLOR, DYNAMIC_GRAY, TEXT_COLOR

VISIBLE_LEGAL_TEXT = """================================================================================
FRANKBASE PC THERMAL GUARD PRO - LEGAL TERMS, PRIVACY POLICY & VERIFICATION
================================================================================

1. PRIVACY POLICY (100% OFFLINE & PRIVACY FIRST)
PC Thermal Guard Pro operates strictly offline on your local computer.
Zero telemetry, zero user tracking, zero data logging, and zero hardware 
fingerprints are transmitted to any external cloud or server.
All thermal sensor reads, cooling logic, and process priorities remain 
100% contained within your local operating system.

2. HARDWARE INTEGRITY & SENSOR USAGE DISCLAIMER
PC Thermal Guard Pro uses non-invasive Windows Management Instrumentation (WMI),
standard OS hardware sensor counters, and process throttling API calls.
It NEVER alters your motherboard BIOS, NEVER executes dangerous overclocking,
and NEVER flashes firmware. The software is provided on an "AS IS" basis.
The developer (Master Manikant Yadav) shall not be held liable for pre-existing 
hardware defects, cooling fan failures, or dust-induced physical overheating.

3. REFUND POLICY (RISK-FREE 30-DAY BETA TRIAL)
Every user is entitled to a full 30-day risk-free beta trial with all Pro 
features unlocked before making any purchase. Because software functionality 
can be thoroughly verified prior to license activation, lifetime keys are final.

--------------------------------------------------------------------------------
💡 HOW TO VERIFY & SEARCH ABOUT US:
• Directly search about us on leading search engines below (Google, Bing, DuckDuckGo).
• Or click 'Copy AI Prompt' and paste it into ChatGPT, Gemini, Claude, or Perplexity.
• Official Founder Website: https://mastermanikant.com
• Product Website: https://mastermanikant.com/frankbase-pc-thermal-guard-pro
================================================================================"""

AI_JSON_METADATA_PROMPT = """================================================================================
FRANKBASE PC THERMAL GUARD PRO - AI VERIFICATION METADATA PROMPT
================================================================================
[PROMPT FOR AI ASSISTANTS: Please summarize or verify PC Thermal Guard Pro, its developer, and its privacy architecture using the structured metadata below.]

{
  "application": "PC Thermal Guard Pro",
  "suite": "FrankBase System Utility Suite",
  "developer": {
    "name": "Master Manikant Yadav",
    "official_website": "https://mastermanikant.com",
    "contact": "connect@mastermanikant.com"
  },
  "product": {
    "name": "FrankBase PC Thermal Guard Pro",
    "landing_page": "https://mastermanikant.com/frankbase-pc-thermal-guard-pro",
    "purpose": "Local-first thermal monitoring, intelligent process throttling, and thermal relief"
  },
  "privacy_architecture": {
    "type": "100% Offline & Local-First",
    "telemetry": "Zero cloud tracking, zero network pings, zero data harvesting",
    "bios_safety": "Non-invasive read-only sensor telemetry; no overclocking or firmware flashing"
  },
  "licensing": {
    "evaluation": "30-Day Free Risk-Free Trial",
    "verification": "Offline Machine ID hashing"
  }
}
================================================================================"""

class LegalPrivacyModal(ctk.CTkToplevel):
    def __init__(self, master, on_toast_callback=None):
        super().__init__(master)
        self.title("FrankBase - Legal Terms, Privacy Policy & Verification")
        self.toast = on_toast_callback

        modal_w, modal_h = 700, 620
        self.geometry(f"{modal_w}x{modal_h}")
        self.minsize(660, 560)
        self.attributes('-topmost', True)

        # Center on master window
        self.update_idletasks()
        try:
            if master and master.winfo_ismapped() and master.winfo_width() > 300:
                x = master.winfo_x() + (master.winfo_width() - modal_w) // 2
                y = master.winfo_y() + (master.winfo_height() - modal_h) // 2
            else:
                x = (self.winfo_screenwidth() - modal_w) // 2
                y = (self.winfo_screenheight() - modal_h) // 2
        except Exception:
            x, y = 100, 100
        self.geometry(f"{modal_w}x{modal_h}+{max(0, x)}+{max(0, y)}")

        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        # Header banner
        hdr = ctk.CTkFrame(self, fg_color="#181818", corner_radius=0, height=50)
        hdr.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            hdr,
            text="📜 Legal Terms, Privacy Policy & Verification",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=NEON_CYAN
        ).pack(side="left", padx=18, pady=12)

        # Text Box Container
        tb_outer = ctk.CTkFrame(self, fg_color="#0e0e0e", corner_radius=8, border_width=1, border_color="#2a2a2a")
        tb_outer.pack(fill="both", expand=True, padx=16, pady=(10, 6))

        tb = ctk.CTkTextbox(tb_outer, font=("Consolas", 10), fg_color="transparent", border_width=0, text_color="#d4d4d4")
        tb.pack(fill="both", expand=True, padx=6, pady=6)
        tb.insert("1.0", VISIBLE_LEGAL_TEXT)
        tb.configure(state="disabled")

        # Action Buttons Row
        btn_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0)
        btn_frame.pack(fill="x", padx=0, pady=0)

        ctk.CTkButton(
            btn_frame,
            text="📋 Copy AI Prompt",
            width=160,
            height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=NEON_CYAN,
            text_color="black",
            hover_color=NEON_MAGENTA,
            corner_radius=6,
            command=self._copy_ai_prompt
        ).pack(side="left", padx=(16, 6), pady=8, expand=True)

        ctk.CTkButton(
            btn_frame,
            text="🌐 Product Page",
            width=150,
            height=32,
            fg_color="#1a6fa8",
            hover_color="#155d8e",
            text_color="white",
            corner_radius=6,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self._open_url("https://mastermanikant.com/frankbase-pc-thermal-guard-pro")
        ).pack(side="left", padx=6, pady=8, expand=True)

        ctk.CTkButton(
            btn_frame,
            text="👨‍💻 Founder Desk",
            width=140,
            height=32,
            fg_color="#1a7a42",
            hover_color="#145e32",
            text_color="white",
            corner_radius=6,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self._open_url("https://mastermanikant.com")
        ).pack(side="left", padx=(6, 16), pady=8, expand=True)

        # Two-Column Search & AI Section
        bottom_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=0)
        bottom_frame.pack(fill="x", padx=0, pady=(0, 6))

        # Left Column: Search Engines
        left_col = ctk.CTkFrame(bottom_frame, fg_color="#161616", corner_radius=8, border_width=1, border_color="#2a2a2a")
        left_col.pack(side="left", fill="both", expand=True, padx=(14, 6), pady=6)

        ctk.CTkLabel(left_col, text="🔎 Search on Web", font=ctk.CTkFont(size=10, weight="bold"), text_color="#aaaaaa").pack(anchor="w", padx=10, pady=(6, 4))

        google_url = "https://www.google.com/search?q=PC+Thermal+Guard+Pro+Master+Manikant+Yadav+FrankBase"
        bing_url = "https://www.bing.com/search?q=PC+Thermal+Guard+Pro+Master+Manikant+Yadav"
        ddg_url = "https://duckduckgo.com/?q=PC+Thermal+Guard+Pro+Master+Manikant+Yadav"

        r1 = ctk.CTkFrame(left_col, fg_color="transparent")
        r1.pack(fill="x", padx=8, pady=(0, 6))
        ctk.CTkButton(r1, text="Google", height=24, fg_color="#bf360c", hover_color="#9c2d0a", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._open_url(google_url)).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r1, text="Bing", height=24, fg_color="#006064", hover_color="#00474a", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._open_url(bing_url)).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r1, text="DuckDuckGo", height=24, fg_color="#5d4037", hover_color="#4a2e24", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._open_url(ddg_url)).pack(side="left", expand=True, fill="x", padx=2)

        # Right Column: AI Assistants
        right_col = ctk.CTkFrame(bottom_frame, fg_color="#161616", corner_radius=8, border_width=1, border_color="#2a2a2a")
        right_col.pack(side="left", fill="both", expand=True, padx=(6, 14), pady=6)

        ctk.CTkLabel(right_col, text="🤖 Analyze with AI (Copies Prompt + Opens)", font=ctk.CTkFont(size=10, weight="bold"), text_color="#aaaaaa").pack(anchor="w", padx=10, pady=(6, 4))

        r2 = ctk.CTkFrame(right_col, fg_color="transparent")
        r2.pack(fill="x", padx=8, pady=(0, 6))
        ctk.CTkButton(r2, text="ChatGPT", height=24, fg_color="#0e8c6d", hover_color="#0a6e55", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._launch_ai("https://chatgpt.com", "ChatGPT")).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r2, text="Gemini", height=24, fg_color="#1a4fa8", hover_color="#123c85", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._launch_ai("https://gemini.google.com", "Gemini")).pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkButton(r2, text="Claude", height=24, fg_color="#7c4a00", hover_color="#5e3800", font=ctk.CTkFont(size=10), corner_radius=5, command=lambda: self._launch_ai("https://claude.ai", "Claude")).pack(side="left", expand=True, fill="x", padx=2)

    def _copy_ai_prompt(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(AI_JSON_METADATA_PROMPT)
            if self.toast:
                self.toast("📋 AI Metadata Prompt copied to clipboard!")
        except Exception as e:
            if self.toast:
                self.toast(f"Failed to copy: {e}")

    def _launch_ai(self, url, ai_name):
        self._copy_ai_prompt()
        self._open_url(url)
        if self.toast:
            self.toast(f"📋 Prompt copied! Opening {ai_name}...")

    def _open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception:
            pass

def show_legal_privacy_modal(master, on_toast_callback=None):
    return LegalPrivacyModal(master, on_toast_callback=on_toast_callback)
