"""
Master Application Window Controller (100% Matched with FrankBase Smart File Organizer Architecture - Screenshots 2 & 3)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import os
import time
import threading
import customtkinter as ctk
from src.ui.theme import ThemeManager, BG_COLOR, FRAME_BG, SIDEBAR_BG, BORDER_COLOR, NEON_CYAN, NEON_MAGENTA, TEXT_COLOR
from src.core.hardware_sensor import HardwareSensorEngine
from src.core.heat_attribution import HeatAttributionEngine
from src.core.root_cause_diagnostics import RootCauseDiagnostics
from src.core.history_manager import HistoryManager
from src.core.thermal_relief import ThermalReliefEngine
from src.core.machine_id import get_machine_hardware_id
from src.ui.top_banner_view import TopCollapsibleHeader
from src.ui.sidebar_view import CollapsibleSidebar
from src.ui.dashboard_view import DashboardView
from src.ui.history_view import HistoryView
from src.ui.cooling_settings_view import CoolingSettingsView
from src.ui.about_view import AboutAndLicenseView
from src.ui.system_tray import SystemTrayManager

class MainWindow(ctk.CTk):
    def __init__(self, sensor_engine=None, history_manager=None, **kwargs):
        super().__init__(**kwargs)

        # Window Configuration (High-DPI 1160x780 matching Smart File Organizer)
        self.title("FrankBase - PC Thermal Guard Pro")
        self.geometry("1160x780")
        self.minsize(920, 680)

        # Set Window Icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.configure(fg_color=BG_COLOR)

        # Core Engines
        self.sensor_engine = sensor_engine or HardwareSensorEngine.get_instance()
        self.history_mgr = history_manager or HistoryManager()
        self.tray_mgr = SystemTrayManager(
            on_show_window=self.restore_from_tray,
            on_cool_down=self._on_master_cool_down_trigger,
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
        # Master Grid Layout:
        # Row 0: Top Header
        # Row 1: Workspace (Col 0: Sidebar, Col 1: Center Viewport)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── 1. Top Header (Row 0, Column 0-1) ──
        self.top_header = TopCollapsibleHeader(
            self,
            on_toggle_theme_callback=self._on_toggle_theme,
            on_minimize_tray_callback=self.minimize_to_tray,
            on_toast_callback=self.show_toast
        )
        self.top_header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # ── 2. Left Sidebar (Row 1, Column 0) ──
        self.sidebar = CollapsibleSidebar(
            self,
            on_navigate_callback=self._switch_view
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        # ── 3. Center Dynamic Viewport (Row 1, Column 1) ──
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Instantiate Views
        self.view_dashboard = DashboardView(
            self.content_container,
            on_toast=lambda title, msg: self.show_toast(f"⚡ {title}: {msg}"),
            on_cool_down_callback=self._on_master_cool_down_trigger
        )
        self.view_history = HistoryView(self.content_container, self.history_mgr)
        self.view_cooling = CoolingSettingsView(
            self.content_container,
            on_toast=self.show_toast
        )
        self.view_about = AboutAndLicenseView(
            self.content_container,
            toast_callback=self.show_toast
        )

        self.views = {
            "Dashboard": self.view_dashboard,
            "History": self.view_history,
            "Sensors": self.view_dashboard,
            "Cooling": self.view_cooling,
            "License": self.view_about,
            "About": self.view_about
        }

        # Show initial dashboard view
        self._switch_view("Dashboard")

    def _switch_view(self, key: str):
        self.active_view_key = key
        for k, v in self.views.items():
            if v and v.winfo_ismapped():
                v.grid_forget()

        target_view = self.views.get(key, self.view_dashboard)
        if target_view:
            target_view.grid(row=0, column=0, sticky="nsew")

    def _on_toggle_theme(self):
        new_theme = ThemeManager.toggle_theme()
        is_dark = new_theme == "dark"

        # Update Master Window & Views
        self.configure(fg_color=BG_COLOR)
        self.top_header.refresh_theme()
        self.sidebar.refresh_theme()

        if hasattr(self.view_dashboard, "apply_theme"):
            self.view_dashboard.apply_theme()
        if hasattr(self.view_history, "refresh_theme"):
            self.view_history.refresh_theme()
        if hasattr(self.view_cooling, "refresh_theme"):
            self.view_cooling.refresh_theme()

        self.show_toast(f"🎨 Switched to {'Night Mode 🌙' if is_dark else 'Day Mode ☀️'}")

    def _on_master_cool_down_trigger(self):
        """Executes Smart Foreground-Safe 1-Click Cool Down."""
        culprits = HeatAttributionEngine.get_top_heat_culprits(limit=4)
        result = ThermalReliefEngine.one_click_cool_down(culprits)
        self.show_toast(result.get("message", "Cool Down Triggered"))

    def show_toast(self, message: str, duration_sec: float = 3.0):
        """Non-blocking floating toast notification (Vibrant Cyan/Magenta border)."""
        toast = ctk.CTkFrame(
            self,
            fg_color="#003344",
            corner_radius=8,
            border_width=1,
            border_color=NEON_CYAN
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
                    cpu_temp = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 45.0
                    self.tray_mgr.update_temp(cpu_temp)

                    # Update Active GUI on main thread
                    self.after(0, lambda t=telemetry, c=culprits, d=diag: self._update_gui(t, c, d))
                except Exception:
                    pass

        threading.Thread(target=_poll, daemon=True).start()

    def _update_gui(self, telemetry, culprits, diagnostics):
        # Update Active Center Views
        if self.view_dashboard.winfo_ismapped():
            self.view_dashboard.update_telemetry(telemetry, culprits, diagnostics)
        if self.view_history.winfo_ismapped():
            self.view_history.update_live_chart()

    def minimize_to_tray(self):
        self.withdraw()
        self.tray_mgr.show_notification(
            "FrankBase PC Thermal Guard Pro",
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