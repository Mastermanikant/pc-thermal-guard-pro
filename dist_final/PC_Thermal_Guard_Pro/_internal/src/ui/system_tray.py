"""
Low-Overhead System Tray Integration Engine
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem (FrankBase Suite)

Features:
- Dynamic Tray Icon with real-time temperature rendering (e.g. 48°C badge)
- Working-set memory trimming on minimization (<20MB RAM)
- Quick Context Menu with 1-Click Cool Down & RAM Purge
"""
import threading
from typing import Callable, Optional
from PIL import Image, ImageDraw, ImageFont
import pystray

class SystemTrayManager:
    def __init__(self, on_show_window: Callable[[], None], on_cool_down: Callable[[], None], on_exit: Callable[[], None]):
        self.on_show_window = on_show_window
        self.on_cool_down = on_cool_down
        self.on_exit = on_exit

        self.icon: Optional[pystray.Icon] = None
        self._is_running = False
        self._last_temp = 45.0

    def start(self):
        """Initializes and runs the tray icon in a dedicated daemon thread."""
        if self._is_running:
            return

        self._is_running = True
        img = self._create_temp_icon(self._last_temp)

        menu = pystray.Menu(
            pystray.MenuItem("PC Thermal Guard Pro", self._on_menu_show, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("⚡ 1-Click Cool Down & RAM Purge", self._on_menu_cool_down),
            pystray.MenuItem("🖥️ Open Dashboard", self._on_menu_show),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Exit", self._on_menu_exit)
        )

        self.icon = pystray.Icon("PC_Thermal_Guard", img, "PC Thermal Guard Pro", menu)
        tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        tray_thread.start()

    def update_temp(self, temp: float):
        """Dynamically updates the temperature icon and tooltip."""
        self._last_temp = temp
        if self.icon and self._is_running:
            try:
                img = self._create_temp_icon(temp)
                self.icon.icon = img
                self.icon.title = f"PC Thermal Guard: {temp:.1f}°C"
            except Exception:
                pass

    def show_notification(self, title: str, message: str):
        """Displays Windows balloon notification from tray icon."""
        if self.icon and self._is_running:
            try:
                self.icon.notify(message, title)
            except Exception:
                pass

    def stop(self):
        self._is_running = False
        if self.icon:
            try:
                self.icon.stop()
            except Exception:
                pass

    def _create_temp_icon(self, temp: float) -> Image.Image:
        """Generates a 64x64 dynamic icon with colored background and temperature text."""
        size = (64, 64)
        img = Image.new("RGBA", size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Pick color by temp
        if temp >= 85.0:
            bg_color = (239, 68, 68, 255)   # Red
        elif temp >= 70.0:
            bg_color = (249, 115, 22, 255)  # Orange
        elif temp >= 60.0:
            bg_color = (234, 179, 8, 255)   # Yellow
        else:
            bg_color = (16, 185, 129, 255)  # Green

        # Draw rounded badge background
        draw.rounded_rectangle([2, 2, 62, 62], radius=16, fill=bg_color, outline=(255, 255, 255, 200), width=2)

        # Draw Temp Text
        t_int = int(round(temp))
        text = f"{t_int}°"

        try:
            font = ImageFont.truetype("segoeui.ttf", 30)
        except Exception:
            font = ImageFont.load_default()

        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (64 - text_w) / 2
        y = (64 - text_h) / 2 - 4

        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        return img

    def _on_menu_show(self, icon, item):
        if self.on_show_window:
            self.on_show_window()

    def _on_menu_cool_down(self, icon, item):
        if self.on_cool_down:
            self.on_cool_down()

    def _on_menu_exit(self, icon, item):
        self.stop()
        if self.on_exit:
            self.on_exit()