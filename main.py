import ast
import httpx

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.config import weather_api_config, bot_config

weather_api_version = weather_api_config.VERSION
weather_api_key = weather_api_config.KEY
bot_token = bot_config.TOKEN

bot = Bot(bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    location = State()


@dp.message_handler(state="*", commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("""Привет!
Отправь мне своё местоположение для получения прогноза погоды!
Для этого открой 'Вложения -> Геопозиция' и нажми 'Отправить свою геопозицию'.""")


@dp.message_handler(state="*", commands=["set_location"])
async def define_constant_location(message: types.Message):
    await UserState.location.set()
    await message.reply("Отправьте геолокацию, которая будет стандартной для команды /weather.")


@dp.message_handler(state=UserState.location, content_types=["location"])
async def process_location(message: types.Message, state: FSMContext):
    await state.set_state(state=str((message.location.latitude, message.location.longitude)))
    await message.reply(f"Геолокация для /weather установлена.")


@dp.message_handler(state=UserState.location)
async def process_invalid_location(message: types.Message, state: FSMContext):
    await message.reply(f"Неверный формат ответа. Пожалуйста, отправьте геолокацию.")


@dp.message_handler(state='*', commands=["weather"])
async def get_predefined_location_forecast(message: types.Message):
    state = await dp.current_state(user=message.from_user.id).get_state()
    if state is None:
        await message.reply("""Нельзя использовать сокращенную команду /weather,
т.к. не было задано стандартное местоположение. Для того, чтобы задать местоположение, 
используйте команду /set_location""")
        return

    lat, lon = ast.literal_eval(state)
    forecast = await get_forecast(lat, lon)
    await message.reply(forecast)


@dp.message_handler(state="*", content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    forecast = await get_forecast(lat, lon)
    await message.reply(forecast)


def get_temp_celsius(kelvin: float):
    return int(kelvin - 273.15)


async def get_forecast(lat, lon):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.openweathermap.org/data/{weather_api_version}/weather?lat={lat}&lon={lon}&appid={weather_api_key}")
        resp_data = resp.json()

    return create_forecast_message(resp_data)


def create_forecast_message(resp_data):
    return f"""Населенный пункт: {resp_data['name']},
температура: {get_temp_celsius(resp_data['main']['temp'])}°C,
ощущается как: {get_temp_celsius(resp_data['main']['feels_like'])}°C,
ветер: {resp_data['wind']['speed']}м/с, направление: {get_wind_direction(resp_data['wind']['deg'])},
{resp_data['weather'][0]['description']} {get_weather_emoji(resp_data['weather'][0]['id'])*3}"""


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


def get_weather_emoji(ID):
    if ID in range(200, 203) or ID in range(230, 233):
        return "⛈"  # thunderstorm with rain
    elif ID in range(210, 213):
        return "🌩"  # thunderstorm
    elif ID in range(300, 322) or ID in range(500, 532):
        return "🌧"  # rain or drizzle
    elif ID in range(600, 623):
        return "🌨"  # snow
    elif ID in range(701, 763):
        return "🌫"  # mist, fog and other
    elif ID == 771:
        return "🌬"  # squall
    elif ID == 781:
        return "🌪"  # tornado
    elif ID == 800:
        return "☀"  # clear sky
    elif ID == 801 or ID == 802:
        return "🌤"  # few clouds
    elif ID == 803 or ID == 804:
        return "🌥"  # broken clouds


if __name__ == '__main__':
    executor.start_polling(dp)
