Мой код mihr_ezan:

Структура кода:

mihr_ezan/
│
├── main.py
│
├── logic/
│   └── time_handler.py
│
├── ui/
│   ├── portrait_clock.py
│   └── landscape_clock.py
│
└── fonts/
    └── DSEG7Classic-Bold.ttf

----------------------

logic/time_handler.py
```
from datetime import datetime

class TimeHandler:
    @staticmethod
    def get_formatted_time(is_colon_visible=True):
        """
        Получает текущее время и форматирует его.
        
        :param is_colon_visible: Флаг видимости двоеточия
        :return: Отформатированная строка времени
        """
        return datetime.now().strftime("%H:%M").replace(":", ":" if is_colon_visible else " ")
```

ui/portrait_clock.py
```
from kivy.uix.label import Label
from kivy.core.window import Window
from logic.time_handler import TimeHandler

class PortraitClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "fonts/DSEG7Classic-Bold.ttf"
        self.color = (0, 1, 0, 1)
        self.is_colon_visible = True
        
        # Базовые настройки
        self.size_hint = (1, None)
        self.halign = 'center'
        
        # Инициализация
        self.setup_portrait_style()
    
    def setup_portrait_style(self):
        """Настройка стиля для портретной ориентации"""
        font_size = Window.width / 3.5
        self.font_size = font_size
        self.valign = 'top'
        self.text_size = (Window.width, None)
        
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
```
ui/landscape_clock.py
```
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
```
main.py
```
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from ui.portrait_clock import PortraitClockLabel
from ui.landscape_clock import LandscapeClockLabel

class MihrEzanApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock_label = None
        
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Использование FloatLayout для гибкого размещения
        self.layout = FloatLayout()
        
        # Определение initial orientation
        self.check_and_set_orientation()
        
        # Привязка события изменения размера
        Window.bind(on_resize=self.check_and_set_orientation)
        
        # Запуск обновления времени
        Clock.schedule_interval(self.update_time, 0.5)
        
        return self.layout
    
    def check_and_set_orientation(self, *args):
        """Выбор виджета в зависимости от ориентации экрана"""
        # Удаляем предыдущий виджет, если он существует
        if self.clock_label:
            self.layout.remove_widget(self.clock_label)
        
        # Определяем ориентацию
        aspect_ratio = Window.width / Window.height
        
        if aspect_ratio > 1:  # Альбомная ориентация
            self.clock_label = LandscapeClockLabel()
        else:  # Портретная ориентация
            self.clock_label = PortraitClockLabel()
        
        # Добавляем новый виджет
        self.layout.add_widget(self.clock_label)
    
    def update_time(self, dt):
        """Обновление времени и переключение видимости двоеточия"""
        if self.clock_label:
            self.clock_label.toggle_colon_visibility()

if __name__ == "__main__":
    MihrEzanApp().run()
```


