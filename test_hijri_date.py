from data.prayer_times import PrayerTimesManager, format_hijri_date

# Создаем экземпляр менеджера
prayer_manager = PrayerTimesManager()

# Получаем данные
data = prayer_manager.get_prayer_times()

if data and 'data' in data:
    date_data = data['data'].get('date', {})
    if date_data and 'hijri' in date_data:
        hijri = date_data['hijri']
        print("\nRaw Hijri data:")
        print(f"Day: {hijri['day']}")
        print(f"Month: {hijri['month']}")
        print(f"Year: {hijri['year']}")
        
        # Форматируем дату
        day = hijri['day']
        month = int(hijri['month']['number'])
        year = hijri['year']
        date_str = f"{day}-{month}-{year}"
        formatted_date = format_hijri_date(date_str)
        print(f"\nFormatted Hijri date: {formatted_date}")
    else:
        print("No Hijri date data found")
else:
    print("Failed to get prayer times data")
