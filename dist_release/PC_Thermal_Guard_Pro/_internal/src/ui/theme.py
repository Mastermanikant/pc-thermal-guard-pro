"""
Theme and Styling Engine (100% Matched with FrankBase Smart File Organizer Design System)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""
import customtkinter as ctk

# ── FrankBase Iconic Neon Accents ──
NEON_CYAN = "#00E5FF"
NEON_MAGENTA = "#FF007F"
NEON_GREEN = "#00E676"
TNEON_CYAN = "#00FFFF"

# ── Dynamic Light / Dark Color Tuples (Light, Dark) ──
BG_COLOR = ("#F5F6FA", "#121212")
SIDEBAR_BG = ("#EAECEE", "#1E1E1E")
FRAME_BG = ("#FFFFFF", "#252526")
TEXT_COLOR = ("#2C3E50", "#FFFFFF")
BORDER_COLOR = ("#cbd5e1", "#333333")
DYNAMIC_GRAY = ("#555555", "#a0a0a0")
INPUT_BG = ("#e2e8f0", "#181818")

THEMES = {
    "dark": {
        "bg_primary": "#121212",
        "bg_secondary": "#1E1E1E",
        "card_bg": "#252526",
        "bg_card": "#252526",
        "bg_card_hover": "#2e2e30",
        "sidebar_bg": "#1E1E1E",
        "input_bg": "#181818",
        "border": "#333333",
        "border_color": "#333333",
        "text_primary": "#FFFFFF",
        "text_secondary": "#a0a0a0",
        "text_muted": "#777777",
        "accent_cyan": NEON_CYAN,
        "accent_magenta": NEON_MAGENTA,
        "accent_green": NEON_GREEN,
        "accent_blue": "#00E5FF",
        "accent_amber": "#f59e0b",
        "status_optimal": "#00E676",
        "status_elevated": "#FFA500",
        "status_hot": "#FF6B00",
        "status_critical": "#FF0055",
        "gauge_bg": "#333333",
        "chart_line": NEON_CYAN,
        "chart_grid": "#222222",
        "chart_bg": "#181818"
    },
    "light": {
        "bg_primary": "#F5F6FA",
        "bg_secondary": "#FFFFFF",
        "card_bg": "#FFFFFF",
        "bg_card": "#FFFFFF",
        "bg_card_hover": "#F0F2F5",
        "sidebar_bg": "#EAECEE",
        "input_bg": "#F0F2F5",
        "border": "#cbd5e1",
        "border_color": "#cbd5e1",
        "text_primary": "#2C3E50",
        "text_secondary": "#555555",
        "text_muted": "#777777",
        "accent_cyan": "#00838F",
        "accent_magenta": "#D81B60",
        "accent_green": "#00C853",
        "accent_blue": "#0284C7",
        "accent_amber": "#d97706",
        "status_optimal": "#00C853",
        "status_elevated": "#E67E22",
        "status_hot": "#D35400",
        "status_critical": "#C0392B",
        "gauge_bg": "#E2E8F0",
        "chart_line": "#00838F",
        "chart_grid": "#E2E8F0",
        "chart_bg": "#FFFFFF"
    }
}

class ThemeManager:
    _current_theme = "dark"

    @classmethod
    def get_current_theme(cls) -> str:
        return cls._current_theme

    @classmethod
    def get_theme_mode(cls) -> str:
        return cls._current_theme

    @classmethod
    def set_theme_mode(cls, mode: str):
        if mode in ["dark", "light"]:
            cls._current_theme = mode
            ctk.set_appearance_mode("Dark" if mode == "dark" else "Light")

    @classmethod
    def toggle_theme(cls) -> str:
        cls._current_theme = "light" if cls._current_theme == "dark" else "dark"
        ctk.set_appearance_mode("Dark" if cls._current_theme == "dark" else "Light")
        return cls._current_theme

    @classmethod
    def get_colors(cls) -> dict:
        return THEMES.get(cls._current_theme, THEMES["dark"])

    @classmethod
    def get(cls, key: str) -> str:
        theme_dict = cls.get_colors()
        return theme_dict.get(key, "#ffffff")