from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
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
    def __init__(self, db, main_window, apply_callback, **kwargs):
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
        
        self.db = db
        self.main_window = main_window  # Сохраняем ссылку на главное окно
        self.apply_callback = apply_callback
        self.colors_visible = False  # Флаг видимости сетки цветов
        self.selected_color = None  # Временное хранение выбранного цвета
        self.initial_color = self.db.get_setting('color')  # Сохраняем начальный цвет
        
        # Основной layout
        self.layout = BoxLayout(
            orientation='vertical', 
            spacing=dp(15),
            size_hint_y=1,
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

        # Основная секция с настройками
        self.settings_section = SettingsSection()
        
        # Карточка с настройками цвета
        color_card = SettingsCard(title="Appearance")
        
        # Создаем кнопку выбора цвета
        current_color = self.db.get_setting('color')
        color_tuple = self.get_color_tuple(current_color)
        
        self.color_button = Button(
            text=f"Color: {current_color}",
            size_hint_y=None,
            height=dp(50),
            background_color=color_tuple,
            background_normal = '',
            color=(0, 0, 0, 1) if current_color == 'Lime' else (0, 0, 0, 1) if sum(color_tuple[:3]) > 1.5 else (1, 1, 1, 1),  # Черный текст для лайма и светлых цветов
            font_size=sp(16)
        )
        self.color_button.bind(on_release=self.toggle_color_grid)
        color_card.add_widget(self.color_button)

        # Контейнер для сетки цветов
        self.colors_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            opacity=0  # Изначально прозрачный
        )
        
        # Сетка для цветных кнопок
        self.colors_grid = GridLayout(
            cols=3,
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(5), dp(5)]
        )
        
        # Список цветов
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
        
        # Создаем кнопки для каждого цвета
        button_size = (Window.width - dp(100)) / 3  # Размер кнопки (с учетом отступов)
        grid_height = button_size * 3 + dp(30)  # Высота сетки (3 ряда кнопок + отступы)
        self.colors_grid.height = grid_height
        self.colors_container.height = grid_height  # Устанавливаем фиксированную высоту
        
        for color_name, color_tuple in colors.items():
            color_button = ColorButton(
                color_name=color_name,
                color_tuple=color_tuple,
                size_hint=(None, None),
                width=button_size,
                height=button_size,
                color=(0, 0, 0, 1) if color_name == 'Lime' else (1, 1, 1, 1) if sum(color_tuple[:3]) > 1.5 else (0, 0, 0, 1)  # Черный текст для лайма и светлых цветов
            )
            color_button.bind(on_release=self._on_color_button_press)
            self.colors_grid.add_widget(color_button)
        
        self.colors_container.add_widget(self.colors_grid)
        color_card.add_widget(self.colors_container)
        color_card.bind(minimum_height=color_card.setter('height'))
        
        # Добавляем карточку в секцию
        self.settings_section.layout.add_widget(color_card)
        
        # Добавляем секцию в основной layout
        self.layout.add_widget(self.settings_section)
        
        # Нижняя панель с кнопками
        bottom_panel = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[dp(10), dp(5)]
        )
        
        # Кнопки управления с увеличенной высотой
        button_style = {
            'size_hint_x': 0.5,
            'color': (1, 1, 1, 1),
            'font_size': sp(16),
            'height': dp(50),
            'size_hint_y': None
        }
        
        cancel_button = Button(
            text="Cancel",
            background_color=(0.8, 0.2, 0.2, 1),
            **button_style
        )
        cancel_button.background_normal_color = cancel_button.background_color
        
        accept_button = Button(
            text="Save",
            background_color=(0.2, 0.8, 0.2, 1),
            **button_style
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
    
    def toggle_color_grid(self, instance):
        """Показать/скрыть сетку цветов"""
        target_opacity = 1 if not self.colors_visible else 0
        
        anim = Animation(
            opacity=target_opacity,
            duration=0.3
        )
        anim.start(self.colors_container)
        self.colors_visible = not self.colors_visible

    def _on_color_button_press(self, button):
        """Обработка нажатия на цветную кнопку"""
        # Обновляем основную кнопку
        self.color_button.text = f"Color: {button.color_name}"
        self.color_button.background_normal = ''
        self.color_button.background_color = button.color_tuple
        # Для лайма всегда используем черный текст
        self.color_button.color = (0, 0, 0, 1) if button.color_name == 'Lime' else (0, 0, 0, 1) if sum(button.color_tuple[:3]) > 1.5 else (1, 1, 1, 1)
        
        # Сохраняем выбранный цвет временно
        self.selected_color = button.color_name
        
        # Скрываем сетку цветов
        self.toggle_color_grid(None)

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
        """Сохраняем настройки при нажатии кнопки Save"""
        if self.selected_color:
            self.db.save_setting('color', self.selected_color)
            if hasattr(self.main_window, 'update_color'):
                self.main_window.update_color(self.selected_color)
        self.dismiss()

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
