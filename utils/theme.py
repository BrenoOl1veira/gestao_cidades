THEMES = {
    "claro": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "button_bg": "#E0E0E0",
        "button_fg": "#000000",
    },
    "escuro": {
        "bg": "#2E2E2E",
        "fg": "#FFFFFF",
        "button_bg": "#4D4D4D",
        "button_fg": "#FFFFFF",
    }
}

class ThemeManager:
    def __init__(self):
        self.current_theme = "claro"
        self.theme = THEMES[self.current_theme]

    def set_theme(self, theme_name):
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.theme = THEMES[theme_name]
        else:
            raise ValueError(f"Tema {theme_name} não encontrado.")

    def get(self, key):
        return self.theme.get(key, None)
