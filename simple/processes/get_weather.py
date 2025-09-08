import logging
import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from simple.models import Weather

logger = logging.getLogger(__name__)


def get_weather_data():
    """
    Получить данные о погоде из OpenWeatherMap API для Москвы
    и сохранить в базу данных
    """
    api_key = settings.OPENWEATHER_API_KEY
    lat = 55.75
    lon = 37.61

    if api_key == 'your_api_key_here':
        error_msg = "OPENWEATHER_API_KEY не настроен в settings"
        logger.error(error_msg)
        return False, error_msg

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('cod') != 200:
            error_msg = f"API вернуло ошибку: {data.get('message', 'Unknown error')}"
            logger.error(error_msg)
            return False, error_msg

        weather = Weather.objects.create(
            city_name=data.get('name', ''),
            country_code=data.get('sys', {}).get('country', ''),

            longitude=data.get('coord', {}).get('lon', 0),
            latitude=data.get('coord', {}).get('lat', 0),

            weather_id=data.get('weather', [{}])[0].get('id', 0),
            weather_main=data.get('weather', [{}])[0].get('main', ''),
            weather_description=data.get('weather', [{}])[0].get('description', ''),
            weather_icon=data.get('weather', [{}])[0].get('icon', ''),

            temperature=data.get('main', {}).get('temp', 0),
            feels_like=data.get('main', {}).get('feels_like', 0),
            temp_min=data.get('main', {}).get('temp_min', 0),
            temp_max=data.get('main', {}).get('temp_max', 0),
            pressure=data.get('main', {}).get('pressure', 0),
            humidity=data.get('main', {}).get('humidity', 0),

            visibility=data.get('visibility'),
            wind_speed=data.get('wind', {}).get('speed', 0),
            wind_degree=data.get('wind', {}).get('deg', 0),
            wind_gust=data.get('wind', {}).get('gust'),

            clouds=data.get('clouds', {}).get('all', 0),

            sunrise=datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)),
            sunset=datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0)),

            api_timestamp=datetime.fromtimestamp(data.get('dt', 0)),
            timezone_offset=data.get('timezone', 0),
        )

        success_msg = f"Данные о погоде для {weather.city_name} успешно сохранены"
        logger.info(success_msg)
        return True, success_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка сети при запросе к OpenWeatherMap API: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except requests.exceptions.Timeout:
        error_msg = "Таймаут при запросе к OpenWeatherMap API"
        logger.error(error_msg)
        return False, error_msg

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            error_msg = "Неверный API ключ для OpenWeatherMap"
        elif e.response.status_code == 404:
            error_msg = "Город не найден в OpenWeatherMap API"
        else:
            error_msg = f"HTTP ошибка: {e.response.status_code} - {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except ValueError as e:
        error_msg = f"Ошибка парсинга JSON ответа: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Неожиданная ошибка: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
