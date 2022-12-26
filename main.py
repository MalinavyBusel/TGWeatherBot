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
    reply_message = """some text"""
    print(resp.json())
    await message.reply(reply_message)


if __name__ == '__main__':
    executor.start_polling(dp)
