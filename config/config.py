from pydantic import BaseSettings
from decouple import config


class BotConfig(BaseSettings):
    # token, provided by BotFather
    TOKEN = config("TG_BOT_TOKEN", cast=str)


class OpenWeatherMapApiConfig(BaseSettings):
    # simply the version of api
    VERSION = "2.5"
    # the personal access key given after the registration
    KEY = config("WEATHER_API_KEY", cast=str)


BOT_CONFIG = BotConfig()
WEATHER_API_CONFIG = OpenWeatherMapApiConfig()
