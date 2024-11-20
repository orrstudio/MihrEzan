# main.py
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation

from ui.portrait_clock import PortraitClockLayout
from ui.landscape_clock import LandscapeClockLabel

class ClockApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock_label = None
        self.current_orientation = None
        
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Использование FloatLayout для гибкого размещения
        self.layout = FloatLayout()
        
        # Определение initial orientation
        self.check_and_set_orientation()
        
        # Привязка события изменения размера
        Window.bind(on_resize=self.on_window_resize)
        
        # Запуск обновления времени
        Clock.schedule_interval(self.update_time, 0.5)
        
        return self.layout
    
    def on_window_resize(self, instance, width, height):
        """Обработчик изменения размера окна с задержкой"""
        # Отменяем предыдущий запланированный вызов, если он есть
        if hasattr(self, '_resize_trigger'):
            Clock.unschedule(self._resize_trigger)
        
        # Планируем новый вызов через 0.1 секунды
        self._resize_trigger = Clock.schedule_once(lambda dt: self.check_and_set_orientation(), 0.1)
    
    def check_and_set_orientation(self, *args):
        """Выбор виджета в зависимости от ориентации экрана"""
        # Определяем ориентацию с гистерезисом
        aspect_ratio = Window.width / Window.height
        LANDSCAPE_THRESHOLD = 1.1
        PORTRAIT_THRESHOLD = 0.9
        
        new_orientation = None
        if aspect_ratio > LANDSCAPE_THRESHOLD:
            new_orientation = 'landscape'
        elif aspect_ratio < PORTRAIT_THRESHOLD:
            new_orientation = 'portrait'
        else:
            # В промежуточной зоне сохраняем текущую ориентацию
            return
        
        # Проверяем, нужно ли менять ориентацию
        if new_orientation == self.current_orientation:
            return
            
        self.switch_orientation(new_orientation)
    
    def switch_orientation(self, new_orientation):
        """Плавное переключение между ориентациями"""
        # Создаем новый виджет
        new_widget = LandscapeClockLabel() if new_orientation == 'landscape' else PortraitClockLayout()
        new_widget.opacity = 0
        
        # Добавляем новый виджет
        self.layout.add_widget(new_widget)
        
        # Если есть предыдущий виджет, делаем плавный переход
        if hasattr(self, 'clock_widget'):
            # Анимация затухания старого виджета
            anim_old = Animation(opacity=0, duration=0.15)
            
            def on_complete(*args):
                self.layout.remove_widget(self.clock_widget)
                self.clock_widget = new_widget
            
            anim_old.bind(on_complete=on_complete)
            anim_old.start(self.clock_widget)
        else:
            self.clock_widget = new_widget
        
        # Анимация появления нового виджета
        anim_new = Animation(opacity=1, duration=0.15)
        anim_new.start(new_widget)
        
        # Сохраняем текущую ориентацию
        self.current_orientation = new_orientation
    
    def update_time(self, dt):
        """Обновление времени и переключение видимости двоеточия"""
        if hasattr(self, 'clock_widget'):
            if isinstance(self.clock_widget, PortraitClockLayout):
                self.clock_widget.clock_label.toggle_colon_visibility()
            else:
                self.clock_widget.toggle_colon_visibility()

if __name__ == "__main__":
    ClockApp().run()
