# data/database.py
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

