from backend.services.open_weather_service import OpenWeatherService
from settings import Settings


def get_open_weather_service():
    return OpenWeatherService(
        base_url=Settings.OPEN_WEATHER_API_URL,
        app_id=Settings.OPEN_WEATHER_APP_ID,
    )
