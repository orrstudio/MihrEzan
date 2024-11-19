from datetime import datetime

class TimeHandler:
    @staticmethod
    def get_formatted_time(is_colon_visible=True):
        """
        Получает текущее время и форматирует его.
        
        :param is_colon_visible: Флаг видимости двоеточия
        :return: Отформатированная строка времени
        """
        return datetime.now().strftime("%H:%M").replace(":", ":" if is_colon_visible else " ")
