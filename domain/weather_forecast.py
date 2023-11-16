from datetime import date

from marshmallow import fields, post_load, EXCLUDE

from basic.basic_entity import BasicEntity


class WeatherForecast(BasicEntity):
    def __init__(
        self,
        latitude: float,
        longitude: float,
        competence: date,
        sunrise: int,
        sunset: int,
        temperature: dict,
        feels_like: dict,
        pressure: int,
        humidity: int,
        dew_point: float,
        uvi: float,
        clouds: int,
        wind_speed: float,
        wind_deg: int,
        wind_gust: float,
        weather_description: str,
        entity_id=None,
    ):
        super().__init__(entity_id=entity_id)
        self.latitude = latitude
        self.longitude = longitude
        self.competence = competence
        self.sunrise = sunrise
        self.sunset = sunset
        self.temperature = temperature
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.dew_point = dew_point
        self.uvi = uvi
        self.clouds = clouds
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.wind_gust = wind_gust
        self.weather_description = weather_description

    class Schema(BasicEntity.Schema):
        class Meta:
            unknown = EXCLUDE

        latitude = fields.Float(required=True)
        longitude = fields.Float(required=True)
        competence = fields.Date(required=True)
        sunrise = fields.Integer(required=True)
        sunset = fields.Integer(required=True)
        temperature = fields.Dict(required=True)
        feels_like = fields.Dict(required=True)
        pressure = fields.Integer(required=True)
        humidity = fields.Integer(required=True)
        dew_point = fields.Float(required=True)
        uvi = fields.Float(required=True)
        clouds = fields.Integer(required=True)
        wind_speed = fields.Float(required=True)
        wind_deg = fields.Integer(required=True)
        wind_gust = fields.Float(required=True)
        weather_description = fields.String(required=True)

        @post_load
        def make_weather_forecast(self, data, **_kwargs):
            return WeatherForecast(**data)
