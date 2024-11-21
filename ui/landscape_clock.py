# ui/landscape_clock.py
from kivy.core.window import Window
from ui.base_clock import BaseClockLabel
from logic.time_handler import TimeHandler
from data.database import SettingsDatabase
from ui.settings_window import SettingsWindow

class LandscapeClockLabel(BaseClockLabel):
    """
    Виджет часов для ландшафтной ориентации.
    Наследуется от BaseClockLabel и добавляет поддержку настроек цвета.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_colon_visible = True
        # Инициализация базы данных для доступа к настройкам
        self.db = SettingsDatabase()
        
        # Загрузка и применение сохраненного цвета из настроек
        saved_color = self.db.get_setting('color')
        if saved_color:
            self.color = SettingsWindow.get_color_tuple(saved_color)
        
    def setup_style(self):
        """
        Настройка стиля для альбомной ориентации.
        Центрирует часы по вертикали и горизонтали.
        """
        super().setup_style()
        self.valign = 'middle'  # Центрирование по вертикали
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Центрирование по горизонтали
        
    def toggle_colon_visibility(self):
        """
        Переключение видимости двоеточия для эффекта мигания.
        Обновляет текст с учетом текущего состояния двоеточия.
        """
        self.is_colon_visible = not self.is_colon_visible
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        
    def apply_settings(self, color):
        """
        Применение новых настроек цвета.
        Args:
            color: Кортеж (r, g, b, a) с новым цветом
        """
        self.color = color
