# logic/time_handler
from datetime import datetime

class TimeHandler:
    # Неразрывный пробел как константа, определенная через chr()
    NBSP = chr(0x00A0)
    
    @staticmethod
    def get_formatted_time(show_colon=True):
        """Форматирование времени с двоеточием или пробелом"""
        current_time = datetime.now().strftime("%H%M")
        separator = ':' if show_colon else TimeHandler.NBSP
        return f"{current_time[:2]}{separator}{current_time[2:]}"
