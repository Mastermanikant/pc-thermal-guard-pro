"""
Master Application Window Controller
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)
"""
import os
import sys
import time
import queue
import ctypes
import threading
import customtkinter as ctk
from src.ui.theme import ThemeManager, BG_COLOR, FRAME_BG, SIDEBAR_BG, BORDER_COLOR, NEON_CYAN, NEON_MAGENTA, TEXT_COLOR
from src.core.hardware_sensor import HardwareSensorEngine
from src.core.heat_attribution import HeatAttributionEngine
from src.core.root_cause_diagnostics import RootCauseDiagnostics
from src.core.history_manager import HistoryManager
from src.core.thermal_relief import ThermalReliefEngine
from src.core.machine_id import get_machine_hardware_id
from src.core.logger import get_logger
from src.ui.top_banner_view import TopCollapsibleHeader
from src.ui.sidebar_view import CollapsibleSidebar
from src.ui.dashboard_view import DashboardView
from src.ui.history_view import HistoryView
from src.ui.cooling_settings_view import CoolingSettingsView
from src.ui.about_view import AboutAndLicenseView
from src.ui.system_tray import SystemTrayManager

logger = get_logger("MainWindow")

class MainWindow(ctk.CTk):
    def __init__(self, sensor_engine=None, history_manager=None, **kwargs):
        super().__init__(**kwargs)
        logger.info("Initializing PC Thermal Guard Pro MainWindow...")

        # Window Configuration (1160x760)
        self.title("FrankBase - PC Thermal Guard Pro")
        self.geometry("1160x760")
        self.minsize(940, 660)

        # Set Window Icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "app_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                logger.warning(f"Could not load window icon: {e}")

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

        # Thread-safe UI update queue (lean maxsize to prevent backlog starvation)
        self.telemetry_queue = queue.Queue(maxsize=2)
        self._stop_event = threading.Event()

        self._build_layout()
        self._start_system_tray()
        self._start_background_telemetry_loop()

        # Start Tkinter Main Thread Queue Consumer Loop
        self.after(500, self._process_telemetry_queue)

        # Intercept Close Event to Minimize to Tray
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        logger.info("MainWindow initialized and ready!")

    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── 1. Top Header (Row 0, Column 0-1) ──
        self.top_header = TopCollapsibleHeader(
            self,
            on_toggle_theme_callback=self._on_toggle_theme,
            on_minimize_tray_callback=self.minimize_to_tray,
            on_navigate_callback=self._switch_view,
            on_toast_callback=self.show_toast
        )
        self.top_header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # ── 2. Left Sidebar (Row 1, Column 0) ──
        self.sidebar = CollapsibleSidebar(
            self,
            on_navigate_callback=self._switch_view
        )
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        # ── 3. Center Viewport (Row 1, Column 1) ──
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Instantiate Clean Views
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
            "Cooling": self.view_cooling,
            "License": self.view_about
        }

        # Show initial dashboard view
        self._switch_view("Dashboard")

    def _switch_view(self, key: str):
        logger.info(f"Navigating to view: {key}")
        self.active_view_key = key
        for k, v in self.views.items():
            if v and v.winfo_ismapped():
                v.grid_forget()

        target_view = self.views.get(key, self.view_dashboard)
        if target_view:
            target_view.grid(row=0, column=0, sticky="nsew")
        self.sidebar.current_active_nav = key
        self.sidebar._highlight_active_nav()

    def _on_toggle_theme(self):
        new_theme = ThemeManager.toggle_theme()
        is_dark = new_theme == "dark"
        logger.info(f"Toggled theme: {new_theme}")

        self.configure(fg_color=BG_COLOR)
        self.top_header.refresh_theme()
        self.sidebar.refresh_theme()

        if hasattr(self.view_dashboard, "apply_theme"):
            self.view_dashboard.apply_theme()
        if hasattr(self.view_history, "apply_theme"):
            self.view_history.apply_theme()
        if hasattr(self.view_cooling, "refresh_theme"):
            self.view_cooling.refresh_theme()

        self.show_toast(f"🎨 Switched to {'Night Mode 🌙' if is_dark else 'Day Mode ☀️'}")

    def _on_master_cool_down_trigger(self):
        """Executes 1-Click Cool Down & RAM Purge."""
        try:
            logger.info("Executing 1-Click Cool Down & RAM Purge...")
            culprits = HeatAttributionEngine.get_top_heat_culprits(limit=4)
            result = ThermalReliefEngine.one_click_cool_down(culprits)
            msg = result.get("message", "Cool Down & RAM Purge Triggered")
            logger.info(f"Cool Down result: {msg}")
            self.show_toast(msg)
        except Exception as e:
            logger.exception(f"Error during Cool Down: {e}")
            self.show_toast(f"⚠️ Error executing Cool Down: {e}")

    def show_toast(self, message: str, duration_sec: float = 3.5):
        """Non-blocking floating toast notification."""
        try:
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
                    if toast.winfo_exists():
                        toast.destroy()
                except Exception:
                    pass

            threading.Thread(target=_remove, daemon=True).start()
        except Exception as e:
            logger.error(f"Error showing toast: {e}")

    def _start_system_tray(self):
        try:
            self.tray_mgr.start()
            logger.info("System Tray started successfully.")
        except Exception as e:
            logger.error(f"Error starting System Tray: {e}")

    def _start_background_telemetry_loop(self):
        def _poll():
            while not self._stop_event.is_set():
                time.sleep(1.0)
                try:
                    telemetry = self.sensor_engine.get_telemetry()
                    cpu_load = telemetry.get("cpu_load", 0.0)
                    culprits = HeatAttributionEngine.get_top_heat_culprits(total_cpu_load=cpu_load, limit=5)
                    diag = RootCauseDiagnostics.diagnose(telemetry, culprits)

                    # Update history ledger
                    self.history_mgr.add_telemetry_point(telemetry, culprits, diag.get("status", "OPTIMAL"))

                    # Update System Tray Temperature Badge
                    cpu_temp = telemetry.get("cpu_package_temp") or telemetry.get("cpu_temp") or 24.0
                    self.tray_mgr.update_temp(cpu_temp)

                    # Put in thread-safe queue for Main Tkinter thread
                    try:
                        self.telemetry_queue.put_nowait((telemetry, culprits, diag))
                    except queue.Full:
                        pass
                except Exception as e:
                    logger.error(f"Error in background telemetry loop: {e}", exc_info=True)

        t = threading.Thread(target=_poll, daemon=True)
        t.start()
        logger.info("Background telemetry thread started.")

    def _process_telemetry_queue(self):
        """Runs strictly on Tkinter Main Thread."""
        latest_item = None
        while not self.telemetry_queue.empty():
            try:
                latest_item = self.telemetry_queue.get_nowait()
            except queue.Empty:
                break

        if latest_item:
            telemetry, culprits, diag = latest_item
            self._update_gui(telemetry, culprits, diag)

        if not self._stop_event.is_set():
            self.after(500, self._process_telemetry_queue)

    def _update_gui(self, telemetry, culprits, diagnostics):
        try:
            if self.view_dashboard.winfo_ismapped():
                self.view_dashboard.update_telemetry(telemetry, culprits, diagnostics)
            if self.view_history.winfo_ismapped():
                self.view_history.update_live_chart()
        except Exception as e:
            logger.error(f"Error updating GUI widgets: {e}", exc_info=True)

    def minimize_to_tray(self):
        try:
            self.withdraw()
            # Trim working set RAM on minimize to drop footprint <20MB
            try:
                ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
            except Exception:
                pass

            self.tray_mgr.show_notification(
                "FrankBase PC Thermal Guard Pro",
                "Running in background tray mode (<20MB RAM). Double-click tray icon to open."
            )
            logger.info("Minimized to System Tray & RAM Trimmed.")
        except Exception as e:
            logger.error(f"Error minimizing to tray: {e}")

    def restore_from_tray(self):
        self.after(0, self._do_restore_from_tray)

    def _do_restore_from_tray(self):
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            logger.info("Restored from System Tray.")
        except Exception as e:
            logger.error(f"Error restoring from tray: {e}")

    def exit_app(self):
        self.after(0, self._do_exit_app)

    def _do_exit_app(self):
        try:
            logger.info("Exiting PC Thermal Guard Pro...")
            self._stop_event.set()
            self.tray_mgr.stop()
            self.sensor_engine.stop_polling()
            self.destroy()
        except Exception as e:
            logger.error(f"Error during exit: {e}")
        finally:
            os._exit(0)