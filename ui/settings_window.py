# ui/portrait_clock.py
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Line, Rectangle
from data.database import SettingsDatabase

class SettingsWindow(ModalView):
    def __init__(self, apply_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        
        # Устанавливаем цвет фона через canvas
        with self.canvas.before:
            Color(0.25, 0.25, 0.25, 1)  # Светло-серый цвет
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.apply_callback = apply_callback
        self.db = SettingsDatabase()
        
        # Создаем основной layout с увеличенным отступом
        self.layout = BoxLayout(
            orientation='vertical', 
            spacing=20,  # Увеличили spacing
            padding=20,  # Увеличили padding
            pos_hint={'top': 1}
        )
        
        # Верхняя панель с увеличенной высотой
        top_panel = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=60,  # Увеличили высоту
            spacing=15   # Увеличили spacing
        )
        
        # Увеличенный заголовок
        title_label = Label(
            text="Настройки",
            color=(1, 1, 1, 1),  # Сделали текст белым для лучшей видимости
            size_hint_x=0.7,
            halign='left',
            valign='middle',
            font_size='20sp'  # Увеличили размер шрифта
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        accept_button = Button(
            text="OK",
            background_color=(0.3, 0.3, 0.3, 1),  # Сделали кнопки темнее фона
            size_hint_x=0.15,
            color=(0, 1, 0, 1),
            font_size='18sp'  # Увеличили размер шрифта
        )
        
        cancel_button = Button(
            text="X",
            background_color=(0.3, 0.3, 0.3, 1),
            size_hint_x=0.15,
            color=(1, 0, 0, 1),
            font_size='18sp'
        )
        
        accept_button.bind(on_release=self.on_accept)
        cancel_button.bind(on_release=self.dismiss)
        
        top_panel.add_widget(title_label)
        top_panel.add_widget(accept_button)
        top_panel.add_widget(cancel_button)
        
        self.layout.add_widget(top_panel)
        
        # Добавляем разделитель с более заметным цветом
        separator = BoxLayout(size_hint_y=None, height=2)  # Увеличили толщину
        with separator.canvas:
            Color(0.4, 0.4, 0.4, 1)  # Сделали разделитель светлее
            Line(points=[separator.x, separator.y, separator.width, separator.y], width=2)
        
        self.layout.add_widget(separator)
        
        # Увеличенный отступ перед следующим элементом
        self.layout.add_widget(BoxLayout(size_hint_y=None, height=20))
        
        # Настройка цвета с увеличенными размерами
        color_label = Label(
            text="Цвет часов",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40,
            halign='left',
            font_size='18sp'  # Увеличили размер шрифта
        )
        color_label.bind(size=color_label.setter('text_size'))
        
        self.color_spinner = Spinner(
            text=self.db.get_setting('color'),
            values=('Лайм', 'Красный', 'Оранжевый', 'Аква', 'Голд', 'Серый', 'Белый'),
            size_hint_y=None,
            height=50,  # Увеличили высоту
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),  # Сделали текст белым
            font_size='18sp'  # Увеличили размер шрифта
        )
        
        self.layout.add_widget(color_label)
        self.layout.add_widget(self.color_spinner)
        
        # Добавляем пустое пространство
        spacer = BoxLayout()
        self.layout.add_widget(spacer)
        
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_accept(self, instance):
        """Обработка нажатия кнопки принять"""
        self.db.save_setting('color', self.color_spinner.text)
        self.apply_callback(self.get_color_tuple(self.color_spinner.text))
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
        return colors.get(color_name, (0, 1, 0, 1))
