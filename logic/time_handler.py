# logic/time_handler
from datetime import datetime

class TimeHandler:
    @staticmethod
    def get_formatted_time(show_colon=True):
        """Форматирование времени с двоеточием или пробелом"""
        current_time = datetime.now().strftime("%H%M")
        return f"{current_time[:2]}{':' if show_colon else '\u00A0'}{current_time[2:]}"
