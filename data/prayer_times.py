"""
Prayer Times Module для MihrEzan.
Обеспечивает получение и кэширование времен молитв через API Aladhan.
"""

import json
import sqlite3
import logging
from datetime import datetime, timedelta
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Полные названия времен молитв для портретной ориентации
PRAYER_NAMES_PORTRAIT = {
    'Fajr': 'Sübh',
    'Sunrise': 'Günəş',
    'Dhuhr': 'Zöhr',
    'Asr': 'Əsr',
    'Maghrib': 'Məğrib',
    'Isha': 'İşa'
}

# Сокращенные названия для ландшафтной ориентации
PRAYER_NAMES_LANDSCAPE = {
    'Fajr': 'Sb',
    'Sunrise': 'Gn',
    'Dhuhr': 'Zh',
    'Asr': 'Əs',
    'Maghrib': 'Mg',
    'Isha': 'İş'
}

class PrayerTimesAPI:
    """
    Класс для работы с API Aladhan.
    
    Attributes:
        BASE_URL (str): Базовый URL API
        city (str): Город для получения времен молитв
        country (str): Страна для получения времен молитв
        method (int): Метод расчета времен молитв (13 для Университета Исламских Наук, Карачи)
    """
    
    BASE_URL = "http://api.aladhan.com/v1"
    
    def __init__(self, city="Baku", country="Azerbaijan", method=13):
        self.city = city
        self.country = country
        self.method = method
        
    def get_prayer_times(self, date=None):
        """
        Получает времена молитв с API Aladhan для указанной даты.
        
        Args:
            date (str, optional): Дата в формате YYYY-MM-DD. По умолчанию - сегодня.
            
        Returns:
            dict: Данные о временах молитв или None в случае ошибки
        """
        try:
            if date is None:
                date = datetime.now().strftime('%Y-%m-%d')
                
            params = {
                'city': self.city,
                'country': self.country,
                'method': self.method,
                'date': date,
                'adjustment': 0,  # Без корректировки времени
                'tune': '0,0,0,0,0,0,0,0',  # Без тонкой настройки
                'school': 0,  # Стандартный метод для Asr
                'midnightMode': 0,  # Стандартный метод для полуночи
                'timezonestring': 'auto'  # Автоопределение временной зоны
            }
            
            logger.info(f"Fetching prayer times for {date} from Aladhan API")
            response = requests.get(f"{self.BASE_URL}/timingsByCity", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Проверяем наличие всех необходимых данных
            if not data.get('data'):
                logger.error("No data received from API")
                return None
                
            required_timings = ['Midnight', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
            if not all(timing in data['data']['timings'] for timing in required_timings):
                logger.error("Missing required prayer times in API response")
                return None
                
            if not all(key in data['data'] for key in ['date', 'meta']):
                logger.error("Missing required date or meta information in API response")
                return None
            
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching prayer times: {e}")
            return None
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing API response: {e}")
            return None
            
    def get_prayer_times_range(self, start_date, end_date):
        """
        Получает времена молитв для диапазона дат.
        
        Args:
            start_date (str): Начальная дата в формате YYYY-MM-DD
            end_date (str): Конечная дата в формате YYYY-MM-DD
            
        Returns:
            dict: Словарь с временами молитв для каждой даты
        """
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            results = {}
            current = start
            while current <= end:
                date_str = current.strftime('%Y-%m-%d')
                prayer_times = self.get_prayer_times(date_str)
                if prayer_times:
                    results[date_str] = prayer_times
                current += timedelta(days=1)
            
            return results
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return None

class PrayerTimesDB:
    """
    Класс для работы с базой данных времен молитв.
    
    Attributes:
        db_path (Path): Путь к файлу базы данных
    """
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / '.mihrezan' / 'prayer_times.db'
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_db()
    
    def _init_db(self):
        """Инициализирует структуру базы данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица для кэширования времен молитв
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prayer_times (
                    date TEXT PRIMARY KEY,
                    gregorian_date TEXT,
                    hijri_date TEXT,
                    city TEXT,
                    country TEXT,
                    midnight TEXT,
                    fajr TEXT,
                    sunrise TEXT,
                    dhuhr TEXT,
                    asr TEXT,
                    maghrib TEXT,
                    isha TEXT,
                    timestamp INTEGER
                )
            ''')
            
            conn.commit()
    
    def save_prayer_times(self, data):
        """
        Сохраняет времена молитв в базу данных.
        
        Args:
            data (dict): Данные от API Aladhan
        """
        if not data or 'data' not in data:
            logger.error("Invalid data format received from API")
            return
        
        try:
            timings = data['data']['timings']
            date = data['data']['date']
            meta = data['data']['meta']
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO prayer_times 
                    (date, gregorian_date, hijri_date, city, country,
                     midnight, fajr, sunrise, dhuhr, asr, maghrib, isha,
                     timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date['gregorian']['date'],
                    json.dumps(date['gregorian']),
                    json.dumps(date['hijri']),
                    meta.get('city', ''),
                    meta.get('country', ''),
                    timings.get('Midnight', ''),
                    timings.get('Fajr', ''),
                    timings.get('Sunrise', ''),
                    timings.get('Dhuhr', ''),
                    timings.get('Asr', ''),
                    timings.get('Maghrib', ''),
                    timings.get('Isha', ''),
                    int(datetime.now().timestamp())
                ))
                
                conn.commit()
        except (KeyError, TypeError) as e:
            logger.error(f"Error saving prayer times: {e}")
    
    def get_prayer_times(self, date=None):
        """
        Получает времена молитв из базы данных.
        
        Args:
            date (str, optional): Дата в формате YYYY-MM-DD. По умолчанию - сегодня.
            
        Returns:
            dict: Времена молитв или None если данные не найдены
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM prayer_times 
                WHERE date = ?
            ''', (date,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'date': row[0],
                    'gregorian': json.loads(row[1]),
                    'hijri': json.loads(row[2]),
                    'meta': {
                        'city': row[3],
                        'country': row[4]
                    },
                    'times': {
                        'Midnight': row[5],
                        'Fajr': row[6],
                        'Sunrise': row[7],
                        'Dhuhr': row[8],
                        'Asr': row[9],
                        'Maghrib': row[10],
                        'Isha': row[11]
                    },
                    'timestamp': row[12]
                }
            
            return None
    
    def get_prayer_times_range(self, start_date, end_date):
        """
        Получает времена молитв для диапазона дат из базы данных.
        
        Args:
            start_date (str): Начальная дата в формате YYYY-MM-DD
            end_date (str): Конечная дата в формате YYYY-MM-DD
            
        Returns:
            dict: Словарь с временами молитв для каждой даты
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM prayer_times 
                WHERE date BETWEEN ? AND ?
                ORDER BY date
            ''', (start_date, end_date))
            
            results = {}
            for row in cursor.fetchall():
                results[row[0]] = {
                    'date': row[0],
                    'gregorian': json.loads(row[1]),
                    'hijri': json.loads(row[2]),
                    'meta': {
                        'city': row[3],
                        'country': row[4]
                    },
                    'times': {
                        'Midnight': row[5],
                        'Fajr': row[6],
                        'Sunrise': row[7],
                        'Dhuhr': row[8],
                        'Asr': row[9],
                        'Maghrib': row[10],
                        'Isha': row[11]
                    },
                    'timestamp': row[12]
                }
            
            return results
    
    def is_cache_valid(self, date=None, max_age=3600):
        """
        Проверяет актуальность кэша.
        
        Args:
            date (str, optional): Дата в формате YYYY-MM-DD. По умолчанию - сегодня.
            max_age (int): Максимальный возраст кэша в секундах (по умолчанию 1 час)
            
        Returns:
            bool: True если кэш актуален, False если нет
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp FROM prayer_times 
                WHERE date = ?
            ''', (date,))
            
            row = cursor.fetchone()
            
            if not row:
                return False
                
            cache_age = int(datetime.now().timestamp()) - row[0]
            return cache_age < max_age

class PrayerTimesManager:
    """
    Менеджер для работы с временами молитв.
    Объединяет функциональность API и базы данных.
    """
    
    def __init__(self, city="Baku", country="Azerbaijan", method=13):
        self.api = PrayerTimesAPI(city, country, method)
        self.db = PrayerTimesDB()
    
    def get_prayer_times(self, date=None, force_update=False):
        """
        Получает времена молитв, при необходимости обновляя кэш.
        
        Args:
            date (str, optional): Дата в формате YYYY-MM-DD. По умолчанию - сегодня.
            force_update (bool): Принудительное обновление кэша
            
        Returns:
            dict: Времена молитв
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Проверяем кэш
        if not force_update and self.db.is_cache_valid(date):
            cached_data = self.db.get_prayer_times(date)
            if cached_data:
                return cached_data
        
        # Получаем новые данные
        api_data = self.api.get_prayer_times(date)
        if api_data:
            self.db.save_prayer_times(api_data)
            return self.db.get_prayer_times(date)
        
        # Возвращаем кэш даже если он устарел
        return self.db.get_prayer_times(date)
    
    def get_prayer_times_range(self, start_date, end_date, force_update=False):
        """
        Получает времена молитв для диапазона дат.
        
        Args:
            start_date (str): Начальная дата в формате YYYY-MM-DD
            end_date (str): Конечная дата в формате YYYY-MM-DD
            force_update (bool): Принудительное обновление кэша
            
        Returns:
            dict: Словарь с временами молитв для каждой даты
        """
        try:
            # Проверяем формат дат
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            
            if not force_update:
                # Пробуем получить данные из кэша
                cached_data = self.db.get_prayer_times_range(start_date, end_date)
                if cached_data and all(self.db.is_cache_valid(date) for date in cached_data.keys()):
                    return cached_data
            
            # Получаем новые данные
            api_data = self.api.get_prayer_times_range(start_date, end_date)
            if api_data:
                for date_data in api_data.values():
                    self.db.save_prayer_times(date_data)
                return self.db.get_prayer_times_range(start_date, end_date)
            
            # Возвращаем кэш даже если он устарел
            return self.db.get_prayer_times_range(start_date, end_date)
            
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return None
    
    def get_next_prayer(self):
        """
        Определяет следующую молитву и время до нее.
        
        Returns:
            tuple: (название молитвы, время до молитвы в минутах)
        """
        prayer_times = self.get_prayer_times()
        if not prayer_times:
            return None, None
            
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        
        # Сортируем молитвы по времени
        prayers = list(prayer_times['times'].items())
        prayers.sort(key=lambda x: x[1])
        
        # Ищем следующую молитву
        for prayer, time in prayers:
            if time > current_time:
                # Вычисляем разницу во времени
                prayer_time = datetime.strptime(time, '%H:%M').replace(
                    year=now.year, month=now.month, day=now.day
                )
                time_diff = prayer_time - now
                minutes = int(time_diff.total_seconds() / 60)
                return prayer, minutes
        
        # Если все молитвы на сегодня прошли, возвращаем первую молитву следующего дня
        tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
        tomorrow_prayers = self.get_prayer_times(tomorrow)
        if tomorrow_prayers:
            first_prayer = min(tomorrow_prayers['times'].items(), key=lambda x: x[1])
            prayer_time = datetime.strptime(first_prayer[1], '%H:%M').replace(
                year=now.year, month=now.month, day=now.day + 1
            )
            time_diff = prayer_time - now
            minutes = int(time_diff.total_seconds() / 60)
            return first_prayer[0], minutes
        
        return None, None
    
    def should_notify(self, prayer_name, minutes_before=15):
        """
        Проверяет, нужно ли отправить уведомление о предстоящей молитве.
        
        Args:
            prayer_name (str): Название молитвы
            minutes_before (int): За сколько минут до молитвы уведомлять
            
        Returns:
            bool: True если нужно отправить уведомление
        """
        next_prayer, minutes_to_prayer = self.get_next_prayer()
        return (next_prayer == prayer_name and 
                minutes_to_prayer is not None and 
                minutes_to_prayer <= minutes_before)

def format_gregorian_date(date_str, weekday):
    """
    Форматирует григорианскую дату в формат 'V - 18.XII.2024'
    где первое римское число - это номер дня недели
    Args:
        date_str: Дата в формате 'DD-MM-YYYY'
        weekday: День недели (Monday, Tuesday, etc.)
    Returns:
        str: Отформатированная дата
    """
    ROMAN_MONTHS = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
        6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
        11: 'XI', 12: 'XII'
    }
    
    WEEKDAY_ROMAN = {
        'Monday': 'I',
        'Tuesday': 'II',
        'Wednesday': 'III',
        'Thursday': 'IV',
        'Friday': 'V',
        'Saturday': 'VI',
        'Sunday': 'VII'
    }
    
    day, month, year = map(int, date_str.split('-'))
    return f"{WEEKDAY_ROMAN[weekday]} - {day}.{ROMAN_MONTHS[month]}.{year}"

def format_hijri_date(date_str):
    """
    Форматирует дату хиджри в формат '20 Jumādá al-ūlá 1446'
    Args:
        date_str: Дата в формате 'DD-MM-YYYY'
    Returns:
        str: Отформатированная дата
    """
    HIJRI_MONTHS = {
        1: 'Muharram',
        2: 'Safar',
        3: 'Rabi al-awwal',
        4: 'Rabi al-thani',
        5: 'Jumada al-ula',
        6: 'Jumada al-akhirah',
        7: 'Rajab',
        8: 'Shaban',
        9: 'Ramadan',
        10: 'Shawwal',
        11: 'Dhu al-Qadah',
        12: 'Dhu al-Hijjah'
    }
    
    day, month, year = map(int, date_str.split('-'))
    return f"{day} {HIJRI_MONTHS[month]} {year}"
