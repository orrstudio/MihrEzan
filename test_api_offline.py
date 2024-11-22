from data.prayer_times import PrayerTimesManager, format_hijri_date
import json

# Тестовые данные
test_data = {
    "code": 200,
    "status": "OK",
    "data": {
        "timings": {
            "Midnight": "00:00",
            "Fajr": "05:30",
            "Sunrise": "07:00",
            "Dhuhr": "12:00",
            "Asr": "15:00",
            "Maghrib": "17:00",
            "Isha": "18:30"
        },
        "date": {
            "readable": "22 Nov 2024",
            "timestamp": "1732032000",
            "gregorian": {
                "date": "22-11-2024",
                "format": "DD-MM-YYYY",
                "day": "22",
                "weekday": {"en": "Friday"},
                "month": {"number": 11, "en": "November"},
                "year": "2024"
            },
            "hijri": {
                "date": "20-05-1446",
                "format": "DD-MM-YYYY",
                "day": "20",
                "weekday": {"en": "Al Juma'a"},
                "month": {"number": 5, "en": "Jumādá al-ūlá"},
                "year": "1446"
            }
        },
        "meta": {
            "latitude": 40.3777,
            "longitude": 49.892,
            "timezone": "Asia/Baku"
        }
    }
}

# Форматируем дату хиджри из тестовых данных
hijri = test_data['data']['date']['hijri']
day = hijri['day']
month = int(hijri['month']['number'])
year = hijri['year']
date_str = f"{day}-{month}-{year}"
formatted_date = format_hijri_date(date_str)

print("\nTest data:")
print(f"Raw Hijri date: {hijri['date']}")
print(f"Formatted Hijri date: {formatted_date}")
print(f"Expected format: DD Month YYYY")
print(f"Month number: {month}")
print(f"Month name: {hijri['month']['en']}")
