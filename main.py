# main.py
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from ui.portrait_clock import PortraitClockLayout, PortraitClockLabel
from ui.landscape_clock import LandscapeClockLabel

class ClockApp(App):
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
        if hasattr(self, 'clock_widget'):
            self.layout.remove_widget(self.clock_widget)
        
        # Определяем ориентацию
        aspect_ratio = Window.width / Window.height
        
        if aspect_ratio > 1:  # Альбомная ориентация
            self.clock_widget = LandscapeClockLabel()
        else:  # Портретная ориентация
            self.clock_widget = PortraitClockLayout()
        
        # Добавляем новый виджет
        self.layout.add_widget(self.clock_widget)
    
    def update_time(self, dt):
        """Обновление времени и переключение видимости двоеточия"""
        if hasattr(self, 'clock_widget'):
            if isinstance(self.clock_widget, PortraitClockLayout):
                self.clock_widget.clock_label.toggle_colon_visibility()
            else:
                self.clock_widget.toggle_colon_visibility()

if __name__ == "__main__":
    ClockApp().run()
