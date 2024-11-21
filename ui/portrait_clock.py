# ui/portrait_clock.py
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from ui.base_clock import BaseClockLabel
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
            text="SETTINGS",
            size_hint=(None, None),
            size=(120, 50),
            background_color=(0.2, 0.2, 0.2, 1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            color=(0.9, 0.9, 0.9, 1),
            font_size='16sp'
        )
        self.settings_button.bind(on_release=self.show_settings)
        self.add_widget(self.settings_button)
        
        # Применяем сохраненные настройки
        saved_color = self.db.get_setting('color')
        if saved_color:
            self.clock_label.color = SettingsWindow.get_color_tuple(saved_color)
    
    def show_settings(self, instance):
        """Показать окно настроек"""
        settings_window = SettingsWindow(self.db, self, self.apply_settings)
        settings_window.open()
    
    def apply_settings(self, color):
        """Применить настройки"""
        self.clock_label.color = color

class PortraitClockLabel(BaseClockLabel):
    def setup_style(self):
        """Настройка стиля для портретной ориентации"""
        super().setup_style()
        # Специфичные настройки для портретного режима
        self.valign = 'top'
        self.pos_hint = {'center_x': 0.5, 'top': 1}
