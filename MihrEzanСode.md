# Мой обновленный код mihr_ezan до версии 0.3:

## Было добавлено:

1. Создана структура базы данных SQLite для хранения настроек в папке data/
2. Добавлено модальное окно настроек с возможностью выбора цвета
3. Добавлена кнопка настроек в портретном режиме
4. Реализовано сохранение и загрузка настроек
5. Добавлены кнопки принятия и отмены изменений

## Структура проекта:

mihr_ezan/  
│  
├── main.py  
│  
├── logic/  
│   └── time_handler.py  
│  
├── ui/  
│   ├── portrait_clock.py  
│   ├── landscape_clock.py  
│   └── settings_window.py  
│  
├── data/  
│   ├── database.py  
│   └── settings.db  
│  
└── fonts/  
    └── DSEG7Classic-Bold.ttf  
    
## /main.py
```python
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
```

# ui/settings_window.py
```python
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from data.database import SettingsDatabase

class SettingsWindow(ModalView):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        # Делаем фон окна настроек немного светлее основного
        self.background_color = (0.15, 0.15, 0.15, 1)
        self.apply_callback = apply_callback
        self.db = SettingsDatabase()
        
        # Создаем основной layout
        self.layout = BoxLayout(
            orientation='vertical', 
            spacing=10, 
            padding=10,
            # Устанавливаем выравнивание по верхнему краю
            pos_hint={'top': 1}
        )
        
        # Верхняя панель с заголовком и кнопками
        top_panel = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=40,
            spacing=10
        )
        
        # Используем более надежные символы для кнопок
        title_label = Label(
            text="Настройки",  # Заменяем символ шестеренки на текст
            color=(0.9, 0.9, 0.9, 1),
            size_hint_x=0.7,
            halign='left',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        accept_button = Button(
            text="OK",  # Заменяем на более надежный текст
            background_color=(0.2, 0.2, 0.2, 1),
            size_hint_x=0.15,
            color=(0, 1, 0, 1)  # Зеленый цвет для кнопки принятия
        )
        
        cancel_button = Button(
            text="X",  # Заменяем на более надежный символ
            background_color=(0.2, 0.2, 0.2, 1),
            size_hint_x=0.15,
            color=(1, 0, 0, 1)  # Красный цвет для кнопки отмены
        )
        
        accept_button.bind(on_release=self.on_accept)
        cancel_button.bind(on_release=self.dismiss)
        
        top_panel.add_widget(title_label)
        top_panel.add_widget(accept_button)
        top_panel.add_widget(cancel_button)
        
        self.layout.add_widget(top_panel)
        
        # Добавляем разделитель
        separator = BoxLayout(
            size_hint_y=None, 
            height=1, 
            padding=(10, 0),
            # background_color=(0.3, 0.3, 0.3, 1) С фоном окна настроек вышла проблема, пришлось закоментить цвет фона.
        )
        self.layout.add_widget(separator)
        
        # Настройка цвета
        color_label = Label(
            text="Цвет часов",
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None,
            height=30,
            halign='left'
        )
        color_label.bind(size=color_label.setter('text_size'))
        
        self.color_spinner = Spinner(
            text=self.db.get_setting('color'),
            values=('Лайм', 'Красный', 'Оранжевый', 'Аква', 'Голд', 'Серый', 'Белый'),
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        
        self.layout.add_widget(color_label)
        self.layout.add_widget(self.color_spinner)
        
        # Добавляем пустое пространство, чтобы прижать содержимое к верху
        spacer = BoxLayout()
        self.layout.add_widget(spacer)
        
        self.add_widget(self.layout)
    
    def on_accept(self, instance):
        """Обработка нажатия кнопки принять"""
        # Сохраняем настройки в базу
        self.db.save_setting('color', self.color_spinner.text)
        
        # Вызываем callback для применения настроек
        self.apply_callback(self.get_color_tuple(self.color_spinner.text))
        
        # Закрываем окно
        self.dismiss()
    
    @staticmethod
    def get_color_tuple(color_name):
        """Преобразование названия цвета в RGB"""
        colors = {
            'Лайм': (0, 1, 0, 1),
            'Красный': (1, 0, 0, 1),
            'Оранжевый': (1, 0.65, 0, 1),
            'Аква': (0, 1, 1, 1),
            'Голд': (1, 0.84, 0, 1),
            'Серый': (0.7, 0.7, 0.7, 1),
            'Белый': (1, 1, 1, 1)
        }
        return colors.get(color_name, (0, 1, 0, 1))  # По умолчанию лайм
```

# ui/portrait_clock.py
```python
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
        
        # Создаем кнопку настроек
        self.settings_button = Button(
            text="S",  # Заменяем на более надежный символ
            size_hint=(None, None),
            size=(40, 40),
            background_color=(0.2, 0.2, 0.2, 1),  # Немного светлее фона
            pos_hint={'center_x': 0.5, 'y': 0.02},
            color=(0.9, 0.9, 0.9, 1)  # Светло-серый цвет текста
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
```

# ui/landscape_clock.py
```python
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

# logic/time_handler
```python
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

# data/database.py
```python
from pathlib import Path
import sqlite3

class SettingsDatabase:
    def __init__(self):
        # Создаем директорию data если её нет
        Path("data").mkdir(exist_ok=True)
        self.db_path = "data/settings.db"
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            
            # Вставляем значение по умолчанию для цвета, если его нет
            cursor.execute("""
                INSERT OR IGNORE INTO settings (key, value) 
                VALUES ('color', 'lime')
            """)
            conn.commit()
    
    def get_setting(self, key):
        """Получение значения настройки"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def save_setting(self, key, value):
        """Сохранение значения настройки"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value) 
                VALUES (?, ?)
            """, (key, value))
            conn.commit()
```

