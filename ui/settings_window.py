# ui/settings_window.py
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
            #background_color=(0.3, 0.3, 0.3, 1)
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
