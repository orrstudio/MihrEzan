from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime
from kivy.metrics import sp
from data.prayer_times import PrayerTimesManager, format_gregorian_date, format_hijri_date

class DateLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Comfortaa-Bold'
        self.font_size = sp(20)
        self.color = (0.502, 0.502, 0, 1)  # Olive color
        self.size_hint = (None, None)
        self.size = (400, 30)
        self.prayer_manager = PrayerTimesManager()
        Clock.schedule_interval(self.update_date, 1)  # Обновление каждую секунду

class GregorianDateLabel(DateLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': 0.5, 'y': 0.65}  # Теперь григорианская дата внизу
        self.update_date(0)

    def update_date(self, dt):
        current_date = datetime.now()
        date_str = current_date.strftime("%d-%m-%Y")
        weekday = current_date.strftime("%A")
        
        data = self.prayer_manager.get_prayer_times()
        if data and 'data' in data:
            timings = data['data'].get('timings', {})
            if timings:
                self.text = format_gregorian_date(date_str, weekday)
        else:
            self.text = format_gregorian_date(date_str, weekday)  # Запасной вариант

class HijriDateLabel(DateLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x': 0.5, 'y': 0.7}  # Теперь хиджри наверху
        self.opacity = 0  # Начинаем скрытым
        self.update_date(0)

    def update_date(self, dt):
        data = self.prayer_manager.get_prayer_times()
        if data and 'data' in data:
            date_data = data['data'].get('date', {})
            if date_data and 'hijri' in date_data:
                hijri = date_data['hijri']
                self.text = f"{hijri['day']} {hijri['month']['en']} {hijri['year']}"
                self.opacity = 1
            else:
                self.opacity = 0
        else:
            self.opacity = 0
