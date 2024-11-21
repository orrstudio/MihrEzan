import requests
import json
from data.prayer_times import format_gregorian_date, format_hijri_date

def test_aladhan_api():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {
        'city': 'Baku',
        'country': 'Azerbaijan',
        'method': 13
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Получаем григорианскую дату и день недели
        gregorian_date = data['data']['date']['gregorian']['date']
        weekday = data['data']['date']['gregorian']['weekday']['en']
        formatted_gregorian = format_gregorian_date(gregorian_date, weekday)
        
        # Получаем дату хиджри
        hijri_date = data['data']['date']['hijri']['date']
        formatted_hijri = format_hijri_date(hijri_date)
        
        print("Raw API Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("\nFormatted Gregorian Date:")
        print(formatted_gregorian)
        print("\nFormatted Hijri Date:")
        print(formatted_hijri)
        
    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_aladhan_api()
