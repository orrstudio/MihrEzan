from data.prayer_times import format_gregorian_date
from datetime import datetime

# Тестируем форматирование даты
test_date = "22-11-2024"
test_weekday = "Friday"  # Добавляем день недели
formatted_date = format_gregorian_date(test_date, test_weekday)
print(f"Original date: {test_date}")
print(f"Weekday: {test_weekday}")
print(f"Formatted date: {formatted_date}")

# Тестируем с текущей датой
current_date = datetime.now()
date_str = current_date.strftime("%d-%m-%Y")
weekday = current_date.strftime("%A")
formatted_current = format_gregorian_date(date_str, weekday)
print(f"\nCurrent date: {date_str}")
print(f"Current weekday: {weekday}")
print(f"Formatted current date: {formatted_current}")
