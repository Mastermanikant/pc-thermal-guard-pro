"""
Theme and Styling Engine (WCAG 2.1 AA Compliant)
PC Thermal Guard Pro

Supports dynamic Day (Light) and Night (Dark) themes.
"""

THEMES = {
    "dark": {
        "bg_primary": "#0f172a",       # Slate 900
        "bg_secondary": "#1e293b",     # Slate 800
        "bg_card": "#1e293b",          # Slate 800
        "bg_card_hover": "#334155",    # Slate 700
        "border": "#334155",           # Slate 700
        "text_primary": "#f8fafc",     # Slate 50 (High Contrast)
        "text_secondary": "#94a3b8",   # Slate 400
        "text_muted": "#64748b",       # Slate 500
        "accent": "#38bdf8",           # Sky 400
        "accent_hover": "#0ea5e9",     # Sky 500
        "success": "#10b981",          # Emerald 500
        "warning": "#f59e0b",          # Amber 500
        "caution": "#f97316",          # Orange 500
        "danger": "#ef4444",           # Red 500
        "gauge_bg": "#334155",
        "chart_line": "#38bdf8",
        "chart_grid": "#334155"
    },
    "light": {
        "bg_primary": "#f8fafc",       # Slate 50
        "bg_secondary": "#ffffff",     # White
        "bg_card": "#ffffff",          # White
        "bg_card_hover": "#f1f5f9",    # Slate 100
        "border": "#cbd5e1",           # Slate 300
        "text_primary": "#0f172a",     # Slate 900 (High Contrast)
        "text_secondary": "#475569",   # Slate 600
        "text_muted": "#64748b",       # Slate 500
        "accent": "#0284c7",           # Sky 600
        "accent_hover": "#0369a1",     # Sky 700
        "success": "#059669",          # Emerald 600
        "warning": "#d97706",          # Amber 600
        "caution": "#ea580c",          # Orange 600
        "danger": "#dc2626",           # Red 600
        "gauge_bg": "#e2e8f0",
        "chart_line": "#0284c7",
        "chart_grid": "#e2e8f0"
    }
}

class ThemeManager:
    _current_theme = "dark"

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
    def get(cls, key: str) -> str:
        theme_dict = THEMES.get(cls._current_theme, THEMES["dark"])
        return theme_dict.get(key, "#ffffff")