"""
Theme and Styling Engine (WCAG 2.1 AA Compliant)
PC Thermal Guard Pro

Supports dynamic Day (Light) and Night (Dark) themes with high-contrast semantic tokens.
"""

THEMES = {
    "dark": {
        "bg_primary": "#0f172a",       # Slate 900
        "bg_secondary": "#1e293b",     # Slate 800
        "card_bg": "#1e293b",          # Slate 800
        "input_bg": "#334155",         # Slate 700
        "bg_card_hover": "#334155",    # Slate 700
        "border_color": "#334155",     # Slate 700
        "text_primary": "#f8fafc",     # Slate 50 (High Contrast)
        "text_secondary": "#94a3b8",   # Slate 400
        "text_muted": "#64748b",       # Slate 500
        "accent_blue": "#38bdf8",      # Sky 400
        "accent_cyan": "#06b6d4",      # Cyan 500
        "accent_amber": "#f59e0b",     # Amber 500
        "status_optimal": "#10b981",   # Emerald 500
        "status_elevated": "#f59e0b",  # Amber 500
        "status_hot": "#f97316",       # Orange 500
        "status_critical": "#ef4444",  # Red 500
        "gauge_bg": "#334155",
        "chart_line": "#38bdf8",
        "chart_grid": "#334155"
    },
    "light": {
        "bg_primary": "#f8fafc",       # Slate 50
        "bg_secondary": "#ffffff",     # White
        "card_bg": "#ffffff",          # White
        "input_bg": "#f1f5f9",         # Slate 100
        "bg_card_hover": "#e2e8f0",    # Slate 200
        "border_color": "#cbd5e1",     # Slate 300
        "text_primary": "#0f172a",     # Slate 900 (High Contrast)
        "text_secondary": "#475569",   # Slate 600
        "text_muted": "#64748b",       # Slate 500
        "accent_blue": "#0284c7",      # Sky 600
        "accent_cyan": "#0891b2",      # Cyan 600
        "accent_amber": "#d97706",     # Amber 600
        "status_optimal": "#059669",   # Emerald 600
        "status_elevated": "#d97706",  # Amber 600
        "status_hot": "#ea580c",       # Orange 600
        "status_critical": "#dc2626",  # Red 600
        "gauge_bg": "#e2e8f0",
        "chart_line": "#0284c7",
        "chart_grid": "#e2e8f0"
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