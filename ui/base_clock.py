from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from logic.time_handler import TimeHandler

class BaseClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "fonts/DSEG7Classic-Bold.ttf"
        self.color = (0, 1, 0, 1)
        self.is_colon_visible = True
        
        # Базовые настройки
        self.size_hint = (1, None)
        self.halign = 'center'
        
        # Инициализация
        self.setup_style()
        Window.bind(on_resize=self.on_window_resize)

    def calculate_font_size(self):
        """Умная адаптация размера шрифта"""
        width = Window.width
        height = Window.height
        aspect_ratio = width / height
        
        if aspect_ratio > 1:  # Альбомная ориентация
            font_size = width / 3.5  # Начальный размер
            self.font_size = font_size
            self.text_size = (width, None)
            self.size = (width, height)
            self.texture_update()
            
            # Сначала уменьшаем, если текст больше окна
            while self.texture_size[0] > width:
                font_size *= 0.99  # Уменьшаем на 1%
                self.font_size = font_size
                self.texture_update()
                
            # Теперь увеличиваем, если текст меньше окна
            while self.texture_size[0] < width:
                font_size *= 1.001  # Увеличиваем на 0.1%
                self.font_size = font_size
                self.texture_update()
                
            return font_size
            
        else:  # Портретная ориентация - не трогаем
            font_size = min(width / 3.5, height / 3.5)
            self.font_size = font_size
            return font_size
                
    def setup_style(self):
        """Базовая настройка стиля"""
        self.size_hint = (1, 1)
        self.text_size = (Window.width, Window.height)
        self.padding = [0, 0, 0, 0]
        self.spacing = 0
        self.halign = 'center'
        self.valign = 'top'  # Прижимаем к верху
        
        # Сначала устанавливаем текст
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        self.texture_update()
        
        # Потом считаем размер шрифта
        self.font_size = self.calculate_font_size()
        
        # Убираем все возможные отступы
        self.bind(size=self._update_text_size)
        self.bind(pos=self._update_text_size)
    
    def _update_text_size(self, *args):
        """Обновляем размер текста при изменении размера или позиции"""
        self.text_size = (Window.width, Window.height)
        self.texture_update()
    
    def toggle_colon_visibility(self):
        """Переключение видимости двоеточия"""
        self.is_colon_visible = not self.is_colon_visible
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        
    def on_window_resize(self, instance, width, height):
        """Обработка изменения размера окна"""
        self.calculate_font_size()
