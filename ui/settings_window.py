"""
Settings Window Module для MihrEzan.
Реализует минималистичный интерфейс настроек с выбором цвета.

Основные компоненты:
- Компактный заголовок
- Сетка из 9 цветов с выделением активного белой рамкой
- Кнопки Save/Cancel для применения/отмены изменений
"""

from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.clock import Clock
from data.database import SettingsDatabase

class ColorButton(Button):
    """Кнопка выбора цвета"""
    def __init__(self, color_name, color_tuple, **kwargs):
        super().__init__(**kwargs)
        self.color_name = color_name
        self.color_tuple = color_tuple
        self.background_color = color_tuple
        self.background_normal = ''
        self.size_hint = (1, None)
        self.height = self.width  # Квадратная кнопка
        
    def on_size(self, *args):
        self.height = self.width  # Поддерживаем квадратную форму при изменении размера

class SettingsCard(BoxLayout):
    """Карточка для группы настроек"""
    def __init__(self, title="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)  # Начальная высота
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        # Фон карточки
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Заголовок секции
        if title:
            title_label = Label(
                text=title.upper(),
                color=(1, 1, 1, 0.8),
                font_size=sp(16),
                size_hint_y=None,
                height=dp(30),
                halign='left'
            )
            title_label.bind(size=title_label.setter('text_size'))
            self.add_widget(title_label)
            
    def _update_rect(self, instance, value):
        """Обновляет позицию и размер фонового прямоугольника"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class SettingsSection(ScrollView):
    """Секция настроек"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(500)  # Будет обновляться динамически
        
        # Фон секции
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 0.95)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Основной layout с адаптивными отступами
        self.layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(15),
            padding=[dp(20), dp(10), dp(20), dp(20)],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_y=None
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class SettingsWindow(ModalView):
    """
    Окно настроек приложения.
    
    Attributes:
        db (SettingsDatabase): База данных настроек
        main_window: Ссылка на главное окно приложения
        apply_callback: Функция обратного вызова для применения настроек
        initial_color (str): Начальный цвет из настроек
        selected_color (str): Выбранный пользователем цвет
    """
    
    # Список доступных цветов
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

    def __init__(self, db, main_window, apply_callback, **kwargs):
        """
        Инициализация окна настроек.
        
        Args:
            db (SettingsDatabase): База данных настроек
            main_window: Главное окно приложения
            apply_callback: Функция применения настроек
            **kwargs: Дополнительные аргументы
        """
        super().__init__(**kwargs)
        
        # Сохраняем начальные значения
        self.db = db
        self.main_window = main_window
        self.apply_callback = apply_callback
        self.initial_color = self.db.get_setting('color')
        self.selected_color = self.initial_color
        
        # Настройка размеров окна
        self.size_hint = (None, None)
        self.width = min(dp(400), Window.width * 0.95)
        self.height = min(dp(500), Window.height * 0.95)
        self.pos_hint = {'center_x': 0.5, 'top': 0.95}
        
        # Основной layout
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(0), dp(0), dp(0), dp(0)]
        )
        
        # Создание заголовка
        title_layout = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            padding=[dp(20), 0]
        )
        
        # Фон заголовка
        with title_layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.title_rect = Rectangle(pos=title_layout.pos, size=title_layout.size)
        title_layout.bind(pos=self._update_title_rect, size=self._update_title_rect)
        
        # Текст заголовка
        title_label = Label(
            text='SETTINGS',
            color=(1, 1, 1, 1),
            font_size=sp(20),
            bold=True,
            halign='center',
            valign='center'
        )
        title_layout.add_widget(title_label)
        self.layout.add_widget(title_layout)
        
        # Сетка цветов сразу после заголовка
        colors_grid = GridLayout(
            cols=3,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(180),
            padding=[dp(20), dp(10)]
        )
        
        # Создаем кнопки цветов
        for color_name, color_tuple in self.colors.items():
            color_button = ColorButton(
                color_name=color_name,
                color_tuple=color_tuple,
                text='',  # Без текста для минималистичного дизайна
                size_hint=(1, None),
                height=dp(50),
                background_normal=''
            )
            color_button.bind(on_release=self._on_color_button_press)
            
            # Сохраняем кнопку если это активный цвет
            if color_name == self.initial_color:
                self.active_button = color_button
            
            colors_grid.add_widget(color_button)
        
        # Добавляем сетку цветов сразу после заголовка
        self.layout.add_widget(colors_grid)
        
        # Растягивающийся виджет между сеткой и кнопками
        self.layout.add_widget(Widget())
        
        # Нижняя панель с кнопками
        bottom_panel = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[dp(20), dp(5)]
        )
        
        # Фон нижней панели
        with bottom_panel.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.bottom_rect = Rectangle(pos=bottom_panel.pos, size=bottom_panel.size)
        bottom_panel.bind(pos=self._update_bottom_rect, size=self._update_bottom_rect)
        
        # Стиль кнопок
        button_style = {
            'size_hint_x': 0.5,
            'size_hint_y': None,
            'height': dp(50),
            'font_size': sp(16)
        }
        
        # Кнопки управления
        cancel_button = Button(
            text="Cancel",
            background_color=(0.8, 0.2, 0.2, 1),
            **button_style
        )
        accept_button = Button(
            text="Save",
            background_color=(0.2, 0.8, 0.2, 1),
            **button_style
        )
        
        cancel_button.bind(on_release=self.dismiss)
        accept_button.bind(on_release=self.on_accept)
        
        bottom_panel.add_widget(cancel_button)
        bottom_panel.add_widget(accept_button)
        
        self.layout.add_widget(bottom_panel)
        self.add_widget(self.layout)
        
        # Добавляем рамку к активной кнопке после отрисовки
        Clock.schedule_once(self._add_initial_border, 0)

    def _add_initial_border(self, dt):
        """Добавляет рамку к изначально активной кнопке."""
        self._add_border_to_button(self.active_button)
    
    def _add_border_to_button(self, button):
        """
        Добавляет белую рамку к кнопке.
        
        Args:
            button: Кнопка, к которой добавляется рамка
        """
        button.canvas.after.clear()
        with button.canvas.after:
            Color(1, 1, 1, 1)
            Line(rectangle=(button.x, button.y, button.width, button.height), width=2)

    def _on_color_button_press(self, button):
        """
        Обработка нажатия на цветную кнопку.
        
        Args:
            button: Нажатая кнопка
        """
        # Убираем рамку со всех кнопок
        for child in button.parent.children:
            child.canvas.after.clear()
        
        # Добавляем рамку на выбранную кнопку
        self._add_border_to_button(button)
        
        # Сохраняем выбранный цвет
        self.selected_color = button.color_name

    def on_accept(self, *args):
        """Сохраняет настройки при нажатии кнопки Save."""
        if self.selected_color:
            self.db.save_setting('color', self.selected_color)
            if hasattr(self.main_window, 'update_color'):
                self.main_window.update_color(self.selected_color)
            if self.apply_callback:
                # Передаем кортеж цвета вместо названия
                self.apply_callback(self.colors[self.selected_color])
        self.dismiss()

    def _update_title_rect(self, instance, value):
        """Обновляет фон заголовка."""
        self.title_rect.pos = instance.pos
        self.title_rect.size = instance.size
    
    def _update_bottom_rect(self, instance, value):
        """Обновляет фон нижней панели."""
        self.bottom_rect.pos = instance.pos
        self.bottom_rect.size = instance.size

    def on_window_resize(self, instance, width, height):
        """
        Обновляет размеры окна при изменении размера экрана.
        
        Args:
            width: Новая ширина окна
            height: Новая высота окна
        """
        self.width = min(dp(400), width * 0.95)
        self.height = min(dp(500), height * 0.95)
    
    def dismiss(self, *args):
        """При отмене возвращаем исходный цвет"""
        if not self.selected_color or args:  # args будут не пусты при явном вызове dismiss
            if hasattr(self.main_window, 'update_color') and self.initial_color:
                self.main_window.update_color(self.initial_color)
        super().dismiss()
    
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
