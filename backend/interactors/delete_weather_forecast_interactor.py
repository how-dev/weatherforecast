from adapters.weather_forecast_adapter import WeatherForecastAdapter


class DeleteWeatherForecastInteractor:
    def __init__(
        self, weather_forecast_adapter: WeatherForecastAdapter, entity_id: str
    ):
        self.weather_forecast_adapter = weather_forecast_adapter
        self.entity_id = entity_id

    def run(self):
        weather_forecast = self.weather_forecast_adapter.get_by_id(
            self.entity_id
        )

        weather_forecast.delete()
