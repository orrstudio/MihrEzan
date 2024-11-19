from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from ui.portrait_clock import PortraitClockLabel
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
    ClockApp().run()
