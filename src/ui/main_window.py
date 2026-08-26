"""
Master Application Window Controller (80-95% Matched with Smart File Organizer UI Architecture)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Design Suite)
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
from src.ui.top_banner_view import TopCollapsibleHeader
from src.ui.sidebar_view import CollapsibleSidebar
from src.ui.bottom_drawer_view import BottomCollapsibleDrawer
from src.ui.dashboard_view import DashboardView
from src.ui.history_view import HistoryView
from src.ui.about_view import AboutAndLicenseView
from src.ui.system_tray import SystemTrayManager

class MainWindow(ctk.CTk):
    def __init__(self, sensor_engine=None, history_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.colors = ThemeManager.get_colors()

        # Window Configuration (High-DPI 1140x760 default)
        self.title("PC Thermal Guard Pro - Hardware Heat & Culprit Diagnostic Suite")
        self.geometry("1140x760")
        self.minsize(880, 640)

        # Set Application Window Icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.configure(fg_color=self.colors["bg_primary"])

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
        # Row 0: Top Collapsible Header & AI Quick-Tools Banner
        # Row 1: Middle Workspace (Col 0: Collapsible Sidebar, Col 1: Center Viewport)
        # Row 2: Bottom Collapsible Telemetry & AI Prompt Drawer
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── 1. Top Collapsible Header (Row 0) ──
        self.top_header = TopCollapsibleHeader(
            self,
            on_toggle_theme_callback=self._on_toggle_theme,
            on_minimize_tray_callback=self.minimize_to_tray,
            on_toast_callback=self.show_toast
        )
        self.top_header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # ── 2. Left Collapsible Sidebar (Row 1, Column 0) ──
        self.sidebar = CollapsibleSidebar(
            self,
            on_navigate_callback=self._switch_view
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        # ── 3. Center Dynamic Viewport (Row 1, Column 1) ──
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=6, pady=4)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Instantiate Sub-Views
        self.view_dashboard = DashboardView(
            self.content_container,
            on_toast=lambda title, msg: self.show_toast(f"⚡ {title}: {msg}"),
            on_cool_down_callback=self._on_master_cool_down_trigger
        )
        self.view_history = HistoryView(self.content_container, self.history_mgr)
        self.view_about = AboutAndLicenseView(
            self.content_container,
            toast_callback=self.show_toast
        )

        self.views = {
            "Dashboard": self.view_dashboard,
            "History": self.view_history,
            "Sensors": self.view_dashboard,
            "Cooling": self.view_dashboard,
            "License": self.view_about,
            "About": self.view_about
        }

        # Show initial dashboard view
        self._switch_view("Dashboard")

        # ── 4. Bottom Collapsible Telemetry & Prompt Drawer (Row 2) ──
        self.bottom_drawer = BottomCollapsibleDrawer(
            self,
            on_cool_down_callback=self._on_master_cool_down_trigger,
            on_toast_callback=self.show_toast
        )
        self.bottom_drawer.grid(row=2, column=0, columnspan=2, sticky="ew")

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
        self.colors = ThemeManager.get_colors()

        # Update Master Window & Components
        self.configure(fg_color=self.colors["bg_primary"])
        self.top_header.refresh_theme()
        self.sidebar.refresh_theme()
        self.bottom_drawer.refresh_theme()

        if hasattr(self.view_dashboard, "apply_theme"):
            self.view_dashboard.apply_theme()
        if hasattr(self.view_history, "refresh_theme"):
            self.view_history.refresh_theme()

        self.show_toast(f"🎨 Switched to {'Night' if new_theme == 'dark' else 'Day'} Mode (WCAG 2.1 AA)")

    def _on_master_cool_down_trigger(self):
        """Executes Smart Foreground-Safe 1-Click Cool Down."""
        culprits = HeatAttributionEngine.get_top_heat_culprits(limit=4)
        result = ThermalReliefEngine.one_click_cool_down(culprits)
        self.show_toast(result.get("message", "Cool Down Triggered"))

    def show_toast(self, message: str, duration_sec: float = 3.5):
        """Non-blocking floating toast notification (Glassmorphic style)."""
        toast = ctk.CTkFrame(
            self,
            fg_color=self.colors["toast_bg"],
            corner_radius=8,
            border_width=1,
            border_color=self.colors["border_active"]
        )
        lbl = ctk.CTkLabel(
            toast,
            text=message,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        )
        lbl.pack(padx=16, pady=8)
        toast.place(relx=0.5, rely=0.07, anchor="center")

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
        cpu_t = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 45.0
        status_name = diagnostics.get("status", "OPTIMAL")

        # Update Top Header live temperature chip
        self.top_header.update_live_temp(cpu_t, status_name)

        # Update Sidebar RAM progress bar
        self.sidebar.update_resource_bars()

        # Update Bottom Drawer streaming line
        self.bottom_drawer.append_telemetry_line(telemetry, culprits)

        # Update Active Center Views
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