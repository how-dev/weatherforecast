from adapters.weather_forecast_adapter import WeatherForecastAdapter


class ListWeatherForecastInteractor:
    def __init__(self, weather_forecast_adapter: WeatherForecastAdapter):
        self.weather_forecast_adapter = weather_forecast_adapter

    def run(self):
        weather_forecasts = self.weather_forecast_adapter.list_all()

        return [
            weather_forecast.to_json()
            for weather_forecast in weather_forecasts
        ]
