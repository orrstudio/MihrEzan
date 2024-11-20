from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
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
        
        # Устанавливаем цвет фона и скругление углов
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
            padding=[dp(20), dp(15), dp(20), dp(20)],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Верхняя панель
        top_panel = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(50),
            spacing=dp(10)
        )
        
        # Заголовок с адаптивным размером шрифта
        title_label = Label(
            text="Настройки",
            color=(1, 1, 1, 1),
            size_hint_x=0.7,
            halign='left',
            valign='middle',
            font_size=sp(24)
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Стилизованные кнопки
        accept_button = Button(
            text="✓",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            color=(1, 1, 1, 1),
            font_size=sp(20)
        )
        accept_button.background_normal_color = accept_button.background_color
        
        cancel_button = Button(
            text="✕",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            color=(1, 1, 1, 1),
            font_size=sp(20)
        )
        cancel_button.background_normal_color = cancel_button.background_color
        
        # Добавляем эффекты при нажатии
        for btn in [accept_button, cancel_button]:
            btn.bind(on_press=self.button_pressed, on_release=self.button_released)
        
        accept_button.bind(on_release=self.on_accept)
        cancel_button.bind(on_release=self.dismiss)
        
        top_panel.add_widget(title_label)
        top_panel.add_widget(accept_button)
        top_panel.add_widget(cancel_button)
        
        self.layout.add_widget(top_panel)
        
        # Разделитель с градиентом
        separator = BoxLayout(size_hint_y=None, height=dp(2))
        with separator.canvas:
            Color(0.3, 0.3, 0.3, 1)
            Line(points=[separator.x, separator.y, separator.width, separator.y], width=2)
        
        self.layout.add_widget(separator)
        
        # Секция выбора цвета
        color_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10)
        )
        
        color_label = Label(
            text="Цвет часов",
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(30),
            halign='left',
            font_size=sp(18)
        )
        color_label.bind(size=color_label.setter('text_size'))
        
        self.color_spinner = Spinner(
            text=self.db.get_setting('color'),
            values=('Lime', 'Aqua', 'Blue', 'Red', 'Yellow', 'Magenta', 'Pink', 'Grey', 'White'),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 0.9),
            font_size=sp(16)
        )
        
        color_section.add_widget(color_label)
        color_section.add_widget(self.color_spinner)
        
        self.layout.add_widget(color_section)
        
        self.add_widget(self.layout)
    
    def on_window_resize(self, instance, width, height):
        # Обновляем размеры окна при изменении размера экрана
        self.width = min(dp(400), width * 0.95)
        self.height = min(dp(500), height * 0.95)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def button_pressed(self, instance):
        # Анимация нажатия: уменьшение размера + затемнение цвета
        anim = Animation(
            size=(dp(35), dp(35)), 
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
        # Анимация отпускания: возврат размера + цвета
        anim = Animation(
            size=(dp(40), dp(40)),
            background_color=instance.background_normal_color,
            duration=0.1
        )
        anim.start(instance)
    
    def on_accept(self, *args):
        self.db.save_setting('color', self.color_spinner.text)
        self.apply_callback(self.get_color_tuple(self.color_spinner.text))
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
