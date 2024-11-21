from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.animation import Animation
from data.database import SettingsDatabase

class SettingsWindow(ModalView):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        # Адаптивный размер окна
        self.width = min(dp(400), Window.width * 0.95)
        self.height = min(dp(500), Window.height * 0.95)
        
        # Привязываем обновление размеров к изменению окна
        Window.bind(on_resize=self.on_window_resize)
        
        # Устанавливаем цвет фона
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 0.95)  # Темный полупрозрачный фон
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.apply_callback = apply_callback
        self.db = SettingsDatabase()
        
        # Основной layout с адаптивными отступами
        self.layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(15),
            padding=[dp(20), dp(10), dp(20), dp(20)],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Заголовок
        title_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(20), 0]
        )
        
        # Добавляем темный фон для заголовка
        with title_layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.title_rect = Rectangle(pos=title_layout.pos, size=title_layout.size)
        title_layout.bind(pos=self._update_title_rect, size=self._update_title_rect)
        
        title_label = Label(
            text='SETTINGS',
            color=(1, 1, 1, 1),
            font_size=sp(24),
            halign='left',
            valign='center'
        )
        title_label.bind(size=title_label.setter('text_size'))
        title_layout.add_widget(title_label)
        
        self.layout.add_widget(title_layout)

        # Основное содержимое
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=1,
            padding=[dp(20), dp(20)]  # Добавляем отступы
        )
        
        # Создаем спиннер для выбора цвета
        current_color = self.db.get_setting('color')
        color_tuple = self.get_color_tuple(current_color)
        
        self.color_spinner = Spinner(
            text=f"Color: {current_color}",
            values=[f"Color: {color}" for color in ['Lime', 'Aqua', 'Blue', 'Red', 'Yellow', 'Magenta', 'Pink', 'Grey', 'White']],
            size_hint_y=None,
            height=dp(50),
            background_color=(*color_tuple[:3], 0.8),
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )
        self.color_spinner.bind(text=self._on_color_select)
        
        # Добавляем спиннер в начало content_layout
        content_layout.add_widget(self.color_spinner)
        
        # Добавляем растягивающийся виджет, чтобы заполнить пространство
        content_layout.add_widget(Widget())
        
        self.layout.add_widget(content_layout)
        
        # Нижняя панель с кнопками
        bottom_panel = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=[dp(10), 0]
        )
        
        # Кнопки управления
        cancel_button = Button(
            text="Cancel",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint_x=0.5,
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )
        cancel_button.background_normal_color = cancel_button.background_color
        
        accept_button = Button(
            text="Save",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint_x=0.5,
            color=(1, 1, 1, 1),
            font_size=sp(16)
        )
        accept_button.background_normal_color = accept_button.background_color
        
        # Добавляем эффекты при нажатии
        for btn in [accept_button, cancel_button]:
            btn.bind(on_press=self.button_pressed, on_release=self.button_released)
        
        accept_button.bind(on_release=self.on_accept)
        cancel_button.bind(on_release=self.dismiss)
        
        bottom_panel.add_widget(cancel_button)
        bottom_panel.add_widget(accept_button)
        
        self.layout.add_widget(bottom_panel)
        self.add_widget(self.layout)
    
    def on_window_resize(self, instance, width, height):
        # Обновляем размеры окна при изменении размера экрана
        self.width = min(dp(400), width * 0.95)
        self.height = min(dp(500), height * 0.95)
    
    def _update_rect(self, instance, value):
        """Обновление фона основного окна"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def _update_title_rect(self, instance, value):
        """Обновление фона заголовка"""
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size
    
    def _on_color_select(self, instance, value):
        """Обработка выбора цвета"""
        color_name = value.replace("Color: ", "")
        color_tuple = self.get_color_tuple(color_name)
        instance.background_color = (*color_tuple[:3], 0.8)
    
    def button_pressed(self, instance):
        # Анимация нажатия: затемнение цвета
        anim = Animation(
            background_color=(
                instance.background_color[0] * 0.8,
                instance.background_color[1] * 0.8,
                instance.background_color[2] * 0.8,
                1
            ),
            duration=0.1
        )
        anim.start(instance)
    
    def button_released(self, instance):
        # Анимация отпускания: возврат цвета
        anim = Animation(
            background_color=instance.background_normal_color,
            duration=0.1
        )
        anim.start(instance)
    
    def on_accept(self, *args):
        color_name = self.color_spinner.text.replace("Color: ", "")
        self.db.save_setting('color', color_name)
        self.apply_callback(self.get_color_tuple(color_name))
        self.dismiss()

    @staticmethod
    def get_color_tuple(color_name):
        """Преобразование названия цвета в RGB"""
        colors = {
            'Lime': (0, 1, 0, 1),
            'Aqua': (0, 1, 1, 1),
            'Blue': (0, 0, 1, 1),
            'Red': (1, 0, 0, 1),
            'Yellow': (1, 1, 0, 1),
            'Magenta': (1, 0, 1, 1),
            'Pink': (1, 0.75, 0.8, 1),
            'Grey': (0.7, 0.7, 0.7, 1),
            'White': (1, 1, 1, 1)
        }
        return colors.get(color_name, (0, 1, 0, 1))  # По умолчанию возвращаем Lime
