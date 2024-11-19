from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime

class ClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "fonts/DSEG7Classic-Bold.ttf"
        self.color = (0, 1, 0, 1)
        self.is_colon_visible = True
        
        # Базовые настройки
        self.size_hint = (1, None)
        self.halign = 'center'
        
        # Инициализация
        self.text = self.get_time()
        Clock.schedule_interval(self.update_time, 0.5)
        Window.bind(on_resize=self.on_window_resize)
        
        # Первоначальная установка размера
        self.resize_font()
    
    def get_time(self):
        return datetime.now().strftime("%H:%M").replace(":", ":" if self.is_colon_visible else " ")
    
    def update_time(self, dt):
        self.is_colon_visible = not self.is_colon_visible
        self.text = self.get_time()
    
    def on_window_resize(self, instance, width, height):
        self.resize_font()
    
    def resize_font(self):
        # Расчет размера шрифта на основе соотношения сторон
        aspect_ratio = Window.width / Window.height
        
        if aspect_ratio > 1:  # Ландшафтная ориентация
            # Адаптация под ширину экрана с учетом соотношения сторон
            font_size = Window.width / 4  # Уменьшаем делитель для лучшей адаптации
            self.font_size = font_size
            self.valign = 'middle'
            self.text_size = (Window.width, Window.height)
        else:  # Портретная ориентация
            font_size = Window.width / 3.5
            self.font_size = font_size
            self.valign = 'top'
            self.text_size = (Window.width, None)
        
        # Обновление текстуры для корректного расчета размеров
        self.texture_update()
        self.height = self.texture_size[1]
        
        # Центрирование по горизонтали
        self.pos_hint = {'center_x': 0.5, 'top': 1}

class ClockApp(App):
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Использование FloatLayout для гибкого размещения
        layout = FloatLayout()
        clock_label = ClockLabel()
        layout.add_widget(clock_label)
        
        return layout

if __name__ == "__main__":
    ClockApp().run()
