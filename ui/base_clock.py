from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
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
            try:
                # Проверяем текущий размер для анимации
                current_size = self.font_size if self.font_size else width/4
                
                # Начальный размер
                font_size = width/4
                self.font_size = font_size
                self.text_size = (width, None)  # Разрешаем тексту расти по высоте для проверки переноса
                self.size = (width, height)  # Устанавливаем размер виджета равным размеру окна
                self.texture_update()
                
                # Плавно уменьшаем пока текст не поместится в одну строку
                safety_counter = 0
                while (self.texture_size[0] > width or 
                       self.texture_size[1] > height or 
                       '\n' in self._lines or 
                       safety_counter > 50):
                    font_size *= 0.98  # Очень плавное уменьшение
                    self.font_size = font_size
                    self.texture_update()
                    safety_counter += 1
                
                # Анимация с overshoot эффектом только если изменение существенное
                if abs(font_size - current_size) > 1:
                    self.font_size = current_size
                    overshoot = current_size + (font_size - current_size) * 1.2
                    anim1 = Animation(font_size=overshoot, duration=0.15)
                    anim2 = Animation(font_size=font_size, duration=0.1)
                    anim1.bind(on_complete=lambda *args: anim2.start(self))
                    anim1.start(self)
                
                return font_size
            except Exception as e:
                print(f"Ошибка при расчете размера шрифта: {e}")
                return self.font_size or width/4
        else:  # Портретная ориентация - оставляем как было
            font_size = min(width / 3.5, height / 3.5)
            self.font_size = font_size
            return font_size
    
    def setup_style(self):
        """Базовая настройка стиля"""
        self.size_hint = (1, 1)
        self.text_size = (Window.width, Window.height)
        self.padding = [0, 0, 0, 0]
        self.spacing = 0
        
        self.font_size = self.calculate_font_size()
        self.halign = 'center'
        self.valign = 'top'  # Прижимаем к верху
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        self.texture_update()
        
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
