"""
Main Application Window Controller (Split-View with Collapsible Sidebar)
PC Thermal Guard Pro
"""
import os
import time
import threading
import customtkinter as ctk
from src.ui.theme import ThemeManager
from src.core.hardware_sensor import HardwareSensorEngine
from src.core.heat_attribution import HeatAttributionEngine
from src.core.root_cause_diagnostics import RootCauseDiagnostics
from src.core.history_manager import HistoryManager
from src.core.thermal_relief import ThermalReliefEngine
from src.core.machine_id import get_machine_hardware_id, copy_machine_id_to_clipboard
from src.ui.sidebar_view import CollapsibleSidebar
from src.ui.dashboard_view import DashboardView
from src.ui.history_view import HistoryView
from src.ui.about_view import AboutAndLicenseView
from src.ui.system_tray import SystemTrayManager

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.colors = ThemeManager.get_colors()

        # Window Config
        self.title("PC Thermal Guard Pro - Hardware Heat & Culprit Diagnostic Suite")
        self.geometry("1100 EARLY_WIDTHx720")
        self.geometry("1120x740")
        self.minsize(860, 620)

        # Set Window Icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.configure(fg_color=self.colors["bg_primary"])

        # Core Engines
        self.sensor_engine = HardwareSensorEngine.get_instance()
        self.history_mgr = HistoryManager()
        self.tray_mgr = SystemTrayManager(
            on_show_window=self.restore_from_tray,
            on_cool_down=self._on_cool_down_trigger,
            on_exit=self.exit_app
        )

        self.hwid = get_machine_hardware_id()
        self.active_view_key = "Dashboard"
        self.views = {}

        self._build_layout()
        self._start_system_tray()
        self._start_background_telemetry_loop()

        # Intercept Close Event to Minimize to Tray
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def _build_layout(self):
        # Configure Grid Layout (Row 0: Header, Row 1: Split View, Row 2: Status Bar)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Row 0: Top Header Bar ---
        self.header_frame = ctk.CTkFrame(self, height=52, fg_color=self.colors["card_bg"], corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Left: App Brand & Shield
        self.lbl_brand = ctk.CTkLabel(
            self.header_frame,
            text="⚡ PC THERMAL GUARD PRO",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        self.lbl_brand.pack(side="left", padx=16)

        # Center-Left: PC Machine ID ("PC Number") Badge
        self.hwid_btn = ctk.CTkButton(
            self.header_frame,
            text=f"PC ID: {self.hwid} 📋",
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"],
            hover_color=self.colors["accent_blue"],
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            command=self._on_copy_hwid_header
        )
        self.hwid_btn.pack(side="left", padx=10)

        # Right: Tray minimize + Day/Night theme
        self.btn_tray = ctk.CTkButton(
            self.header_frame,
            text="📥 Minimize to Tray",
            width=130,
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_secondary"],
            hover_color=self.colors["accent_blue"],
            font=ctk.CTkFont(size=11),
            command=self.minimize_to_tray
        )
        self.btn_tray.pack(side="right", padx=(6, 16))

        self.btn_theme = ctk.CTkButton(
            self.header_frame,
            text="🌙 Night" if ThemeManager.get_current_theme() == "dark" else "☀️ Day",
            width=80,
            height=28,
            corner_radius=6,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"],
            hover_color=self.colors["accent_cyan"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._on_toggle_theme
        )
        self.btn_theme.pack(side="right", padx=6)

        # --- Row 1, Column 0: Left Collapsible Sidebar ---
        self.sidebar = CollapsibleSidebar(
            self,
            on_navigate_callback=self._switch_view
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        # --- Row 1, Column 1: Right Dynamic Content Container ---
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Instantiate Sub-Views
        self.view_dashboard = DashboardView(
            self.content_container,
            on_cool_down_callback=self._on_cool_down_trigger
        )
        self.view_history = HistoryView(self.content_container, self.history_mgr)
        self.view_about = AboutAndLicenseView(
            self.content_container,
            toast_callback=self.show_toast
        )

        self.views = {
            "Dashboard": self.view_dashboard,
            "History": self.view_history,
            "Sensors": self.view_dashboard,  # Direct sensors telemetry
            "Cooling": self.view_dashboard,  # Cooling focused view
            "License": self.view_about,
            "About": self.view_about
        }

        # Show initial view
        self._switch_view("Dashboard")

        # --- Row 2: Bottom Status Bar ---
        self.status_bar = ctk.CTkFrame(self, height=26, fg_color=self.colors["card_bg"], corner_radius=0)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.lbl_status_engine = ctk.CTkLabel(
            self.status_bar,
            text=f"Engine: {self.sensor_engine.driver_mode} | RAM: <20MB | Polling: 1.0s Async",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        self.lbl_status_engine.pack(side="left", padx=15)

        self.lbl_status_badge = ctk.CTkLabel(
            self.status_bar,
            text="🟢 Telemetry Live (Zero VRAM)",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors["status_optimal"]
        )
        self.lbl_status_badge.pack(side="right", padx=15)

    def _switch_view(self, key: str):
        self.active_view_key = key
        for k, v in self.views.items():
            if v and v.winfo_ismapped():
                v.grid_forget()

        target_view = self.views.get(key, self.view_dashboard)
        if target_view:
            target_view.grid(row=0, column=0, sticky="nsew")

    def _on_copy_hwid_header(self):
        copy_machine_id_to_clipboard()
        self.show_toast(f"📋 PC ID ({self.hwid}) copied to clipboard!")

    def _on_toggle_theme(self):
        new_theme = ThemeManager.toggle_theme()
        self.colors = ThemeManager.get_colors()
        self.configure(fg_color=self.colors["bg_primary"])
        self.header_frame.configure(fg_color=self.colors["card_bg"])
        self.status_bar.configure(fg_color=self.colors["card_bg"])
        self.btn_theme.configure(
            text="🌙 Night" if new_theme == "dark" else "☀️ Day",
            fg_color=self.colors["input_bg"],
            text_color=self.colors["text_primary"]
        )
        self.sidebar.refresh_theme()
        self.view_dashboard.refresh_theme()
        self.view_history.refresh_theme()
        self.show_toast(f"Switched to {'Night' if new_theme == 'dark' else 'Day'} Mode")

    def _on_cool_down_trigger(self):
        """Executes Smart Foreground-Safe 1-Click Cool Down."""
        culprits = HeatAttributionEngine.get_top_heat_culprits(limit=4)
        result = ThermalReliefEngine.one_click_cool_down(culprits)
        self.show_toast(result.get("message", "Cool Down Triggered"))

    def show_toast(self, message: str, duration_sec: float = 3.5):
        """Non-blocking floating toast notification."""
        toast = ctk.CTkFrame(
            self,
            fg_color=self.colors["accent_blue"],
            corner_radius=8,
            border_width=1,
            border_color=self.colors["accent_cyan"]
        )
        lbl = ctk.CTkLabel(
            toast,
            text=message,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        )
        lbl.pack(padx=16, pady=8)
        toast.place(relx=0.5, rely=0.08, anchor="center")

        def _remove():
            time.sleep(duration_sec)
            try:
                toast.destroy()
            except Exception:
                pass

        threading.Thread(target=_remove, daemon=True).start()

    def _start_system_tray(self):
        self.tray_mgr.start()

    def _start_background_telemetry_loop(self):
        def _poll():
            while True:
                time.sleep(1.0)
                try:
                    telemetry = self.sensor_engine.get_telemetry()
                    culprits = HeatAttributionEngine.get_top_heat_culprits(limit=5)
                    diag = RootCauseDiagnostics.diagnose(telemetry, culprits)

                    # Update history ledger
                    self.history_mgr.add_telemetry_point(telemetry, culprits)

                    # Update System Tray Temperature Badge
                    cpu_temp = telemetry.get("cpu_package_temp") or telemetry.get("cpu_max_core_temp") or 45.0
                    self.tray_mgr.update_temp(cpu_temp)

                    # Update Active GUI Views on main thread
                    self.after(0, lambda t=telemetry, c=culprits, d=diag: self._update_gui(t, c, d))
                except Exception:
                    pass

        threading.Thread(target=_poll, daemon=True).start()

    def _update_gui(self, telemetry, culprits, diagnostics):
        if self.view_dashboard.winfo_ismapped():
            self.view_dashboard.update_telemetry(telemetry, culprits, diagnostics)
        if self.view_history.winfo_ismapped():
            self.view_history.update_live_chart()

    def minimize_to_tray(self):
        self.withdraw()
        self.tray_mgr.show_notification(
            "PC Thermal Guard Pro",
            "Running in background. Double-click tray icon to open."
        )

    def restore_from_tray(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def exit_app(self):
        self.tray_mgr.stop()
        self.destroy()
        os._exit(0)