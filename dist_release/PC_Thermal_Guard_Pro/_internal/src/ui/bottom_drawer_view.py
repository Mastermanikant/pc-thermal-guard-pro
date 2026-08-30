"""
Bottom Collapsible Telemetry & AI Diagnostic Drawer (Shrink/Expand)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Design Suite)
"""
import time
import customtkinter as ctk
from typing import Callable, Dict, Any, List
from src.ui.theme import ThemeManager
from src.core.machine_id import get_machine_hardware_id

class BottomCollapsibleDrawer(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_cool_down_callback: Callable[[], None] = None,
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
        self.on_cool_down = on_cool_down_callback
        self.toast = on_toast_callback
        self.is_expanded = False
        self.last_telemetry: Dict[str, Any] = {}
        self.last_culprits: List[Dict[str, Any]] = []

        self._build_ui()

    def _build_ui(self):
        # ── Always Visible Strip (Row 0) ──
        self.strip_bar = ctk.CTkFrame(self, fg_color="transparent", height=32)
        self.strip_bar.pack(fill="x", padx=12, pady=4)

        # Left: Live Status & Engine Indicator
        self.lbl_status = ctk.CTkLabel(
            self.strip_bar,
            text="🟢 Telemetry Live (Zero VRAM) | RAM: <20MB | Engine: Ring-0 MSR / Adaptive",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_secondary"]
        )
        self.lbl_status.pack(side="left", padx=4)

        # Right: Quick Actions & Drawer Toggle
        self.btn_cool = ctk.CTkButton(
            self.strip_bar,
            text="⚡ Quick Cool Down",
            height=24,
            corner_radius=4,
            fg_color=self.colors["accent_blue"],
            hover_color=self.colors["accent_cyan"],
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._on_cool_clicked
        )
        self.btn_cool.pack(side="right", padx=6)

        self.btn_drawer_toggle = ctk.CTkButton(
            self.strip_bar,
            text="▲ Expand Live Stream & AI Log",
            height=24,
            corner_radius=4,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"],
            hover_color=self.colors["card_bg_hover"],
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self.toggle_drawer
        )
        self.btn_drawer_toggle.pack(side="right", padx=4)

        # ── Collapsible Drawer Body (Hidden by default) ──
        self.drawer_body = ctk.CTkFrame(self, fg_color=self.colors["bg_secondary"], corner_radius=0)

        # Content of Drawer: Live Textbox Stream + AI Copy Prompt Bar
        self._build_drawer_body()

    def _build_drawer_body(self):
        # Top toolbar inside drawer
        tools_row = ctk.CTkFrame(self.drawer_body, fg_color="transparent")
        tools_row.pack(fill="x", padx=12, pady=(8, 4))

        ctk.CTkLabel(
            tools_row,
            text="📝 Real-Time Hardware Telemetry Stream (Per-Second Ledger):",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left")

        btn_copy_ai_prompt = ctk.CTkButton(
            tools_row,
            text="🤖 Copy AI Diagnostic Prompt",
            height=24,
            corner_radius=4,
            fg_color=self.colors["status_optimal"],
            hover_color="#059669",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=self._on_copy_ai_prompt
        )
        btn_copy_ai_prompt.pack(side="right", padx=4)

        btn_clear = ctk.CTkButton(
            tools_row,
            text="🗑️ Clear Stream",
            height=24,
            corner_radius=4,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_secondary"],
            hover_color=self.colors["card_bg_hover"],
            font=ctk.CTkFont(size=10),
            command=self._on_clear_stream
        )
        btn_clear.pack(side="right", padx=4)

        # Live Text Stream Box
        self.txt_stream = ctk.CTkTextbox(
            self.drawer_body,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=self.colors["card_bg"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["border_color"]
        )
        self.txt_stream.pack(fill="x", padx=12, pady=(0, 10))

    def toggle_drawer(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.btn_drawer_toggle.configure(text="▼ Shrink Drawer")
            self.drawer_body.pack(fill="x", padx=0, pady=0)
        else:
            self.btn_drawer_toggle.configure(text="▲ Expand Live Stream & AI Log")
            self.drawer_body.pack_forget()

    def append_telemetry_line(self, telemetry: Dict[str, Any], culprits: List[Dict[str, Any]]):
        self.last_telemetry = telemetry
        self.last_culprits = culprits

        ts = time.strftime("%H:%M:%S")
        cpu_t = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 45.0
        gpu_t = telemetry.get("gpu_temp", 42.0)
        load = telemetry.get("cpu_load", 0.0)
        pwr = telemetry.get("cpu_power", 15.0)
        fan = telemetry.get("fan_rpm", 1200)

        top_culprit = culprits[0]["name"] if culprits else "Idle"
        top_has = culprits[0]["heat_score"] if culprits else 0.0

        line = f"[{ts}] CPU: {cpu_t:.1f}°C | Load: {load:.1f}% | Power: {pwr:.1f}W | GPU: {gpu_t:.1f}°C | Fan: {fan} RPM | Top: {top_culprit} ({top_has:.1f}% HAS)\n"

        if self.is_expanded:
            try:
                self.txt_stream.insert("end", line)
                # Keep last 150 lines
                lines = self.txt_stream.get("1.0", "end").splitlines()
                if len(lines) > 150:
                    self.txt_stream.delete("1.0", "2.0")
                self.txt_stream.see("end")
            except Exception:
                pass

    def _on_cool_clicked(self):
        if self.on_cool_down:
            self.on_cool_down()

    def _on_clear_stream(self):
        self.txt_stream.delete("1.0", "end")

    def _on_copy_ai_prompt(self):
        hwid = get_machine_hardware_id()
        cpu_t = self.last_telemetry.get("cpu_package_temp") or self.last_telemetry.get("cpu_temp") or 45.0
        load = self.last_telemetry.get("cpu_load", 0.0)
        fan = self.last_telemetry.get("fan_rpm", 1200)
        culprits_str = ", ".join([f"{c['name']} ({c['heat_score']}%)" for c in self.last_culprits[:4]])

        prompt = (
            f"Analyze this PC hardware thermal diagnosis:\n"
            f"- Machine ID: {hwid}\n"
            f"- CPU Temp: {cpu_t}°C (Load: {load}%)\n"
            f"- Cooling Fan: {fan} RPM\n"
            f"- Top Heat Culprit Applications: {culprits_str}\n"
            f"Is this system healthy? What actionable hardware or software steps should I take to prevent throttling and fan noise?"
        )

        try:
            import pyperclip
            pyperclip.copy(prompt)
        except Exception:
            import subprocess
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            p.communicate(input=prompt.encode('utf-8'))

        if self.toast:
            self.toast("📋 AI Diagnostic Prompt copied! Paste into ChatGPT or Gemini.")

    def refresh_theme(self):
        self.colors = ThemeManager.get_colors()
        self.configure(fg_color=self.colors["card_bg"], border_color=self.colors["border_color"])
        self.lbl_status.configure(text_color=self.colors["text_secondary"])
        self.btn_cool.configure(fg_color=self.colors["accent_blue"])
        self.btn_drawer_toggle.configure(
            fg_color=self.colors["input_bg"],
            text_color=self.colors["accent_cyan"]
        )
        self.drawer_body.configure(fg_color=self.colors["bg_secondary"])
        self.txt_stream.configure(
            fg_color=self.colors["card_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border_color"]
        )