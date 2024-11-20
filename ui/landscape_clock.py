# ui/landscape_clock.py
from kivy.core.window import Window
from ui.base_clock import BaseClockLabel
from logic.time_handler import TimeHandler

class LandscapeClockLabel(BaseClockLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_colon_visible = True
        
    def setup_style(self):
        """Настройка стиля для альбомной ориентации"""
        super().setup_style()
        # Специфичные настройки для альбомного режима
        self.valign = 'middle'  # Возвращаем центрирование по вертикали
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Центрируем виджет
        
    def toggle_colon_visibility(self):
        """Переключение видимости двоеточия"""
        self.is_colon_visible = not self.is_colon_visible
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
