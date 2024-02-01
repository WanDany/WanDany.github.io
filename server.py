from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

app = Flask(__name__, static_url_path='/static')


def get_location_and_time_worldtimeserver():
    try:
        # Отправляем GET-запрос на страницу
        url = 'https://www.worldtimeserver.com/worldclock.aspx'
        response = requests.get(url)
        response.raise_for_status()  # Проверяем наличие ошибок при запросе

        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем элемент с информацией о текущей локации и времени
        location_elem = soup.find('div', {'id': 'ContentPlaceHolderMain_headerdiv'})
        if location_elem:
            location_text = location_elem.get_text(strip=True)
            # Пробел после "Kazakhstan"
            location_text = location_text.replace('Kazakhstan', 'Kazakhstan ')
            location_text = location_text.replace('Your Location:', ' ')
            location_text = location_text.replace('Thu', 'Thursday')
            location_text = location_text.replace('Fri', 'Friday')
            return location_text
        else:
            return 'Не удалось найти информацию о текущей локации и времени'
    except (requests.RequestException, Exception) as e:
        return f'Произошла ошибка: {e}'

def get_date_timeanddate():
    try:
        # Отправляем GET-запрос на страницу
        url = 'https://www.timeanddate.com'
        response = requests.get(url)
        response.raise_for_status()  # Проверяем наличие ошибок при запросе

        # Извлекаем текст из ответа
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем элемент с информацией о текущей дате
        date_elem = soup.find('span', {'id': 'ij2'})
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            return date_text
        else:
            return 'Не удалось найти информацию о текущей дате'
    except (requests.RequestException, Exception) as e:
        return f'Произошла ошибка при получении информации о текущей дате с Time and Date: {e}'

def translate_text(text):
    try:
        translated = GoogleTranslator(source='en', target='ru').translate(text)
        return translated
    except Exception as e:
        return f'Произошла ошибка при переводе: {e}'

@app.route('/')
def index():
    location_and_time_worldtimeserver = get_location_and_time_worldtimeserver()
    date_timeanddate = get_date_timeanddate()
    translated_location_and_time_worldtimeserver = translate_text(location_and_time_worldtimeserver)
    translated_date_timeanddate = translate_text(date_timeanddate)
    return render_template('index.html', location_and_time_worldtimeserver=translated_location_and_time_worldtimeserver, date_timeanddate=translated_date_timeanddate)

if __name__ == '__main__':
    app.run(debug=True)
