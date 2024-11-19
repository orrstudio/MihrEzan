# ui/portrait_clock.py
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from logic.time_handler import TimeHandler
from ui.settings_window import SettingsWindow
from data.database import SettingsDatabase

class PortraitClockLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = SettingsDatabase()
        
        # Создаем метку времени
        self.clock_label = PortraitClockLabel()
        self.add_widget(self.clock_label)
        
        # Создаем увеличенную кнопку настроек
        self.settings_button = Button(
            text="SETTINGS",  # Изменили текст
            size_hint=(None, None),
            size=(120, 50),  # Увеличили размер кнопки
            background_color=(0.2, 0.2, 0.2, 1),
            pos_hint={'center_x': 0.5, 'y': 0.05},  # Немного подняли кнопку
            color=(0.9, 0.9, 0.9, 1),
            font_size='16sp'  # Добавили размер шрифта
        )
        self.settings_button.bind(on_release=self.show_settings)
        self.add_widget(self.settings_button)
        
        # Применяем сохраненные настройки
        saved_color = self.db.get_setting('color')
        if saved_color:
            self.clock_label.color = SettingsWindow.get_color_tuple(saved_color)
    
    def show_settings(self, instance):
        """Показать окно настроек"""
        settings_window = SettingsWindow(self.apply_settings)
        settings_window.open()
    
    def apply_settings(self, color):
        """Применить настройки"""
        self.clock_label.color = color

class PortraitClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "fonts/DSEG7Classic-Bold.ttf"
        self.color = (0, 1, 0, 1)  # Начальный цвет
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
