from data.prayer_times import format_gregorian_date

# Тестируем форматирование даты
test_date = "22-11-2024"
formatted_date = format_gregorian_date(test_date)
print(f"Original date: {test_date}")
print(f"Formatted date: {formatted_date}")
