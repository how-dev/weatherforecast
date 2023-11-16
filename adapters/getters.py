from adapters.weather_forecast_adapter import WeatherForecastAdapter
from settings import Settings
import logging

logger = logging.getLogger(__name__)


def get_weather_forecast_adapter():
    return WeatherForecastAdapter(
        host=Settings.DB_HOST, db_name=Settings.DB_NAME, logger=logger
    )
