from domain.weather_forecast import WeatherForecast
from mongodb_adapter.basic_mongodb_adapter import BasicMongoDBAdapter


class WeatherForecastAdapter(BasicMongoDBAdapter):
    def __init__(self, host: str, db_name: str, logger=None):
        super().__init__(
            host=host,
            db_name=db_name,
            adapted_class=WeatherForecast,
            logger=logger,
        )
