import aiogram.utils.markdown
import httpx

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config.config import weather_api_config, bot_config

weather_api_version = weather_api_config.VERSION
weather_api_key = weather_api_config.KEY
bot_token = bot_config.TOKEN

bot = Bot(bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("""Привет!
    Отправь мне своё местоположение!
    Для этого открой 'Вложения -> Геопозиция' и нажми 'Отправить свою геопозицию'.""")


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.openweathermap.org/data/{weather_api_version}/weather?lat={lat}&lon={lon}&appid={weather_api_key}")
        resp_data = resp.json()

    reply_message = get_forecast_message(resp_data)
    await message.reply(reply_message, parse_mode="Markdown")


def get_temp_celsius(kelvin: float):
    return int(kelvin - 273.15)


def get_forecast_message(resp_data):
    return f"""Населенный пункт: {resp_data['name']},
температура: {get_temp_celsius(resp_data['main']['temp'])}°C,
ощущается как: {get_temp_celsius(resp_data['main']['feels_like'])}°C,
ветер: {resp_data['wind']['speed']}м/с, направление: {get_wind_direction(resp_data['wind']['deg'])},
{attach_image_with_markdown(resp_data['weather'][0])}"""


def attach_image_with_markdown(weather_descr):
    return f'[{weather_descr["description"]}](http://openweathermap.org/img/w/{weather_descr["icon"]}.png)'


def get_wind_direction(degree):
    if degree < 22.5 or degree > 337.5:
        return "N"
    elif degree < 67.5:
        return "NE"
    elif degree < 112.5:
        return "E"
    elif degree < 157.5:
        return "SE"
    elif degree < 202.5:
        return "S"
    elif degree < 247.5:
        return "SW"
    elif degree < 292.5:
        return "W"
    elif degree < 337.5:
        return "NW"
    ...


if __name__ == '__main__':
    executor.start_polling(dp)
