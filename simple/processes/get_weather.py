import requests
import logging
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from simple.models.weather import Weather

logger = logging.getLogger(__name__)


def get_weather_data():
    """
    Fetch weather data from OpenWeatherMap API for Moscow and save to database.

    Returns:
        tuple: (success: bool, message: str)
    """
    API_KEY = getattr(settings, "OPENWEATHER_API_KEY", None)

    if not API_KEY:
        error_msg = "OPENWEATHER_API_KEY not found in settings"
        logger.error(error_msg)
        return False, error_msg

    # Coordinates for Moscow
    LAT = 55.75
    LON = 37.61

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"

    try:
        logger.info(
            f"Fetching weather data from OpenWeatherMap API for Moscow (lat: {LAT}, lon: {LON})"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Validate response structure
        if data.get("cod") != 200:
            error_msg = f"API returned error: {data.get('message', 'Unknown error')}"
            logger.error(error_msg)
            return False, error_msg

        # Extract data from response
        coord = data.get("coord", {})
        weather_data = data.get("weather", [{}])[0] if data.get("weather") else {}
        main_data = data.get("main", {})
        wind_data = data.get("wind", {})
        clouds_data = data.get("clouds", {})
        sys_data = data.get("sys", {})

        # Convert timestamp to datetime
        api_timestamp = (
            timezone.make_aware(datetime.fromtimestamp(data.get("dt", 0)))
            if data.get("dt")
            else timezone.now()
        )

        sunrise_time = (
            timezone.make_aware(datetime.fromtimestamp(sys_data.get("sunrise", 0)))
            if sys_data.get("sunrise")
            else None
        )

        sunset_time = (
            timezone.make_aware(datetime.fromtimestamp(sys_data.get("sunset", 0)))
            if sys_data.get("sunset")
            else None
        )

        # Create Weather object
        weather = Weather(
            city_name=data.get("name", "Moscow"),
            country_code=sys_data.get("country", "RU"),
            longitude=coord.get("lon", 0.0),
            latitude=coord.get("lat", 0.0),
            weather_id=weather_data.get("id", 0),
            weather_main=weather_data.get("main", ""),
            weather_description=weather_data.get("description", ""),
            weather_icon=weather_data.get("icon", ""),
            temperature=main_data.get("temp", 0.0),
            feels_like=main_data.get("feels_like", 0.0),
            temp_min=main_data.get("temp_min", 0.0),
            temp_max=main_data.get("temp_max", 0.0),
            pressure=main_data.get("pressure", 0),
            humidity=main_data.get("humidity", 0),
            visibility=data.get("visibility"),
            wind_speed=wind_data.get("speed", 0.0),
            wind_degree=wind_data.get("deg", 0),
            clouds=clouds_data.get("all", 0),
            sunrise=sunrise_time,
            sunset=sunset_time,
            api_timestamp=api_timestamp,
            timezone_offset=data.get("timezone", 0),
        )

        weather.full_clean()
        weather.save()

        success_msg = f"Weather data for {weather.city_name} successfully fetched and saved"
        logger.info(success_msg)
        return True, success_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Network error while fetching weather data: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error while fetching weather data: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except KeyError as e:
        error_msg = f"Missing expected data in API response: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Unexpected error while fetching weather data: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
