"""
Theme and Styling Engine (WCAG 2.1 AA Compliant - Zero Hardcoded Colors)
PC Thermal Guard Pro
Master Manikant Yadav Ecosystem
"""

THEMES = {
    "dark": {
        "bg_primary": "#0a0f1d",       # Deep Obsidian Slate (Main Window BG)
        "bg_secondary": "#111827",     # Dark Gray 900 (Secondary BG)
        "card_bg": "#1e293b",          # Slate 800 (Card & Panel BG)
        "card_bg_hover": "#273549",    # Slate 750 (Card Hover)
        "sidebar_bg": "#0f172a",       # Slate 900 (Sidebar BG)
        "input_bg": "#1e293b",         # Slate 800 (Input / Pill BG)
        "input_border": "#334155",      # Slate 700
        "border_color": "#334155",     # Slate 700 (Border default)
        "border_active": "#38bdf8",    # Sky 400 (Active Glow Border)
        "text_primary": "#f8fafc",     # Slate 50 (15:1 High Contrast Ratio)
        "text_secondary": "#94a3b8",   # Slate 400 (Subtitles)
        "text_muted": "#64748b",       # Slate 500 (Footers/Hints)
        "accent_blue": "#0284c7",      # Sky 600 (Primary Action)
        "accent_cyan": "#06b6d4",      # Cyan 500 (Glow / Highlights)
        "accent_magenta": "#d946ef",   # Fuchsia 500 (Mode Pill)
        "accent_amber": "#f59e0b",     # Amber 500 (Warnings)
        "status_optimal": "#10b981",   # Emerald 500 (Green)
        "status_elevated": "#f59e0b",  # Amber 500 (Orange)
        "status_hot": "#f97316",       # Orange 500
        "status_critical": "#ef4444",  # Red 500
        "gauge_bg": "#334155",         # Slate 700 (Empty Meter Track)
        "chart_line": "#38bdf8",       # Sky 400
        "chart_grid": "#1e293b",       # Grid Lines
        "chart_bg": "#0f172a",         # Canvas Background
        "toast_bg": "#0369a1",         # Deep Sky
        "drawer_bg": "#0f172a"         # Bottom Drawer BG
    },
    "light": {
        "bg_primary": "#f1f5f9",       # Slate 100 (Main Window BG)
        "bg_secondary": "#ffffff",     # White (Secondary BG)
        "card_bg": "#ffffff",          # White (Card & Panel BG)
        "card_bg_hover": "#f8fafc",    # Slate 50 (Card Hover)
        "sidebar_bg": "#ffffff",       # White (Sidebar BG)
        "input_bg": "#e2e8f0",         # Slate 200 (Input / Pill BG)
        "input_border": "#cbd5e1",      # Slate 300
        "border_color": "#cbd5e1",     # Slate 300 (Border default)
        "border_active": "#0284c7",    # Sky 600 (Active Glow Border)
        "text_primary": "#0f172a",     # Slate 900 (15:1 High Contrast Ratio)
        "text_secondary": "#475569",   # Slate 600 (Subtitles)
        "text_muted": "#64748b",       # Slate 500 (Footers/Hints)
        "accent_blue": "#0284c7",      # Sky 600 (Primary Action)
        "accent_cyan": "#0891b2",      # Cyan 600 (Glow / Highlights)
        "accent_magenta": "#c026d3",   # Fuchsia 600 (Mode Pill)
        "accent_amber": "#d97706",     # Amber 600 (Warnings)
        "status_optimal": "#059669",   # Emerald 600 (Green)
        "status_elevated": "#d97706",  # Amber 600 (Orange)
        "status_hot": "#ea580c",       # Orange 600
        "status_critical": "#dc2626",  # Red 600
        "gauge_bg": "#e2e8f0",         # Slate 200 (Empty Meter Track)
        "chart_line": "#0284c7",       # Sky 600
        "chart_grid": "#e2e8f0",       # Grid Lines
        "chart_bg": "#ffffff",         # Canvas Background
        "toast_bg": "#0284c7",         # Sky 600
        "drawer_bg": "#f8fafc"         # Bottom Drawer BG
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

    @classmethod
    def toggle_theme(cls) -> str:
        cls._current_theme = "light" if cls._current_theme == "dark" else "dark"
        return cls._current_theme

    @classmethod
    def get_colors(cls) -> dict:
        return THEMES.get(cls._current_theme, THEMES["dark"])

    @classmethod
    def get(cls, key: str) -> str:
        theme_dict = cls.get_colors()
        return theme_dict.get(key, "#ffffff")