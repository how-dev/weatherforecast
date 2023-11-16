from datetime import datetime, timedelta
from typing import List

from adapters.weather_forecast_adapter import WeatherForecastAdapter
from backend.services.open_weather_service import (
    OpenWeatherService,
    OpenWeatherRequest,
)
from domain.weather_forecast import WeatherForecast


class CreateWeatherForecastInteractor:
    def __init__(
        self,
        weather_forecast_adapter: WeatherForecastAdapter,
        open_weather_service: OpenWeatherService,
    ):
        self.weather_forecast_adapter = weather_forecast_adapter
        self.open_weather_service = open_weather_service

    def run(self):
        existents_weather_forecasts = self._get_existents()

        if existents_weather_forecasts:
            return [
                weather_forecast.to_json()
                for weather_forecast in existents_weather_forecasts
            ]

        open_weather_request = OpenWeatherRequest()
        open_weather_dailies = self.open_weather_service.get_weather_forecast(
            request=open_weather_request
        )

        weather_forecasts = []

        for open_wather_daily in open_weather_dailies:
            weather_forecast = self._create_weather_forecast(open_wather_daily)
            weather_forecasts.append(weather_forecast.to_json())

        return weather_forecasts

    def _get_existents(self) -> List[WeatherForecast]:
        now = datetime.now().date()

        next_five_days = [str(now + timedelta(days=i)) for i in range(1, 6)]

        return self.weather_forecast_adapter.filter(
            competence__in=next_five_days
        )

    def _create_weather_forecast(
        self, open_weather_response
    ) -> WeatherForecast:
        datetime_competence = datetime.fromtimestamp(
            open_weather_response.timestamp
        )
        weather_forecast = WeatherForecast(
            latitude=open_weather_response.latitude,
            longitude=open_weather_response.longitude,
            competence=datetime_competence.date(),
            sunrise=open_weather_response.sunrise,
            sunset=open_weather_response.sunset,
            temperature=open_weather_response.temperature,
            feels_like=open_weather_response.feels_like,
            pressure=open_weather_response.pressure,
            humidity=open_weather_response.humidity,
            dew_point=open_weather_response.dew_point,
            uvi=open_weather_response.uvi,
            clouds=open_weather_response.clouds,
            wind_speed=open_weather_response.wind_speed,
            wind_deg=open_weather_response.wind_deg,
            wind_gust=open_weather_response.wind_gust,
            weather_description=open_weather_response.weather_description,
        )
        weather_forecast.set_adapter(self.weather_forecast_adapter)
        weather_forecast.save()

        return weather_forecast
