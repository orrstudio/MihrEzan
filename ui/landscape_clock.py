from kivy.uix.label import Label
from kivy.core.window import Window
from logic.time_handler import TimeHandler

class LandscapeClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "fonts/DSEG7Classic-Bold.ttf"
        self.color = (0, 1, 0, 1)
        self.is_colon_visible = True
        
        # Базовые настройки
        self.size_hint = (1, None)
        self.halign = 'center'
        
        # Инициализация
        self.setup_landscape_style()
    
    def setup_landscape_style(self):
        """Настройка стиля для альбомной ориентации"""
        font_size = Window.width / 4
        self.font_size = font_size
        self.valign = 'middle'
        self.text_size = (Window.width, Window.height)
        
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        
        # Обновление текстуры для корректного расчета размеров
        self.texture_update()
        self.height = self.texture_size[1]
        
        # Центрирование по горизонтали
        self.pos_hint = {'center_x': 0.5, 'top': 1}
    
    def toggle_colon_visibility(self):
        """Переключение видимости двоеточия"""
        self.is_colon_visible = not self.is_colon_visible
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
