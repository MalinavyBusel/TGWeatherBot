from pydantic import BaseSettings
from decouple import config


class BotConfig(BaseSettings):
    TOKEN = config("TG_BOT_TOKEN", cast=str)


class WeatherApiConfig(BaseSettings):
    VERSION = config("WEATHER_API_VERSION", cast=str)
    KEY = config("WEATHER_API_KEY", cast=str)


BOT_CONFIG = BotConfig()
WEATHER_API_CONFIG = WeatherApiConfig()
