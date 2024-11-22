# main.py
import kivy
kivy.require('2.2.1')

import logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation

from ui.portrait_clock import PortraitClockLayout
from ui.landscape_clock import LandscapeClockLabel

class ClockApp(App):
    # Список доступных цветов
    colors = {
        'lime': (0, 1, 0, 1),
        'aqua': (0, 1, 1, 1),
        'blue': (0, 0, 1, 1),
        'red': (1, 0, 0, 1),
        'yellow': (1, 1, 0, 1),
        'magenta': (1, 0, 1, 1),
        'pink': (1, 0.75, 0.8, 1),
        'grey': (0.7, 0.7, 0.7, 1),
        'white': (1, 1, 1, 1)
    }

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
        """
        Плавное переключение между портретной и ландшафтной ориентациями.
        
        Args:
            new_orientation (str): Новая ориентация ('landscape' или 'portrait')
            
        Реализует:
        1. Создание нового виджета для выбранной ориентации
        2. Передачу текущих настроек цвета
        3. Плавную анимацию перехода между виджетами
        """
        # Создаем новый виджет в соответствии с ориентацией
        new_widget = LandscapeClockLabel() if new_orientation == 'landscape' else PortraitClockLayout()
        new_widget.opacity = 0
        
        # Добавляем новый виджет в layout
        self.layout.add_widget(new_widget)
        
        # Если есть предыдущий виджет, выполняем плавный переход
        if hasattr(self, 'clock_widget'):
            # Передаем цвет от старого виджета к новому
            if hasattr(self.clock_widget, 'clock_label'):
                new_widget.color = self.clock_widget.clock_label.color
            else:
                new_widget.color = self.clock_widget.color
                
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

    def update_color(self, color_name):
        """Обновление цвета часов"""
        try:
            if hasattr(self, 'clock_widget'):
                # Преобразуем название цвета в нижний регистр
                color_key = color_name.lower()
                color_tuple = self.colors.get(color_key, (1, 1, 1, 1))
                
                if isinstance(self.clock_widget, PortraitClockLayout):
                    self.clock_widget.clock_label.color = color_tuple
                else:
                    self.clock_widget.color = color_tuple
        except Exception as e:
            logger.error(f"Error updating color: {e}")

if __name__ == "__main__":
    ClockApp().run()
