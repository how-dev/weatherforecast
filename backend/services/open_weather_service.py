from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Optional, List

import requests


@dataclass
class OpenWeatherRequest:
    SAO_PAULO_LATITUDE = -23.5489
    SAO_PAULO_LONGITUDE = -46.6388

    latitude: int = SAO_PAULO_LATITUDE
    longitude: int = SAO_PAULO_LONGITUDE


@dataclass
class OpenWeatherResponse:
    latitude: float
    longitude: float
    timestamp: int
    sunrise: int
    sunset: int
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather_description: str


class OpenWeatherService:
    def __init__(
        self,
        base_url: str,
        app_id: str,
    ):
        self.base_url = base_url
        self.app_id = app_id

    def get_weather_forecast(
        self, request: OpenWeatherRequest
    ) -> List[OpenWeatherResponse]:
        celsius_unit = "metric"

        url = (
            f"{self.base_url}?"
            f"lat={request.latitude}&"
            f"lon={request.longitude}&"
            f"exclude=minutely,hourly,current&"
            f"units={celsius_unit}&"
            f"appid={self.app_id}"
        )
        response = requests.get(url)
        response_json = response.json()
        dailies = response_json["daily"][1:6]

        return [
            OpenWeatherResponse(
                latitude=response_json["lat"],
                longitude=response_json["lon"],
                timestamp=daily["dt"],
                sunrise=daily["sunrise"],
                sunset=daily["sunset"],
                temperature=daily["temp"],
                feels_like=daily["feels_like"],
                pressure=daily["pressure"],
                humidity=daily["humidity"],
                dew_point=daily["dew_point"],
                uvi=daily["uvi"],
                clouds=daily["clouds"],
                wind_speed=daily["wind_speed"],
                wind_deg=daily["wind_deg"],
                wind_gust=daily["wind_gust"],
                weather_description=daily["weather"][0]["description"],
            )
            for daily in dailies
        ]
