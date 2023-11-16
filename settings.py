from decouple import config as env


class Settings:
    DB_HOST = env('DB_HOST')
    DB_NAME = env('DB_NAME')
    OPEN_WEATHER_APP_ID = env('OPEN_WEATHER_APP_ID')
    OPEN_WEATHER_API_URL = env('OPEN_WEATHER_API_URL')
