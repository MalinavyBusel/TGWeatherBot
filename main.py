import ast
import httpx

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.config import WEATHER_API_CONFIG, BOT_CONFIG
from forecast_creation import create_forecast_message

weather_api_version = WEATHER_API_CONFIG.VERSION
weather_api_key = WEATHER_API_CONFIG.KEY
bot_token = BOT_CONFIG.TOKEN

bot = Bot(bot_token)
storage = RedisStorage2(db=0)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    location = State()


@dp.message_handler(state="*", commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("""Привет!
Отправь мне своё местоположение для получения прогноза погоды!
Для этого открой 'Вложения -> Геопозиция' и нажми 'Отправить свою геопозицию'.""")


@dp.message_handler(state="*", commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("""Список команд:
*Вложения -> Геопозиция -> Отправить свою геопозицию* - Возвращает текущую погоду для отправленной геопозиции;
/set_location - устанавливает постоянное местоположение для команды /weather;
/weather - более удобный вариант получения прогноза. Отправляет текущий прогноз погоды для заданного местоположения.""")


# sets location for the /weather command
@dp.message_handler(state="*", commands=["set_location"])
async def define_constant_location(message: types.Message):
    # this instruction tells the bot that the next message from the user will contain the state
    # and should be handled as the answer, not as the other command
    await UserState.location.set()

    await message.reply("Отправьте геолокацию, которая будет стандартной для команды /weather.")


# the next two functions are the second part of the upper one

# this function handles the correct scenario, when the user sends the location
@dp.message_handler(state=UserState.location, content_types=["location"])
async def process_location(message: types.Message, state: FSMContext):
    # the state of the user is set to the given location
    await state.set_state(state=str((message.location.latitude, message.location.longitude)))
    await message.reply(f"Геолокация для /weather установлена.")


# that one handles the case when the other type of data is sent and asks user to send the location
@dp.message_handler(state=UserState.location)
async def process_invalid_location(message: types.Message, state: FSMContext):
    await message.reply(f"Неверный формат ответа. Пожалуйста, отправьте геолокацию.")


# Gives user the forecast according to location the user set with /set_location
@dp.message_handler(state='*', commands=["weather"])
async def get_predefined_location_forecast(message: types.Message):
    # get the user location from the storage
    current_location = await dp.current_state(user=message.from_user.id).get_state()
    # if there is no predefined location, print error message
    if current_location is None:
        await message.reply("""Нельзя использовать сокращенную команду /weather,
т.к. не было задано стандартное местоположение. Для того, чтобы задать местоположение, 
используйте команду /set_location.""")
        return

    # else print the forecast
    lat, lon = ast.literal_eval(current_location)  # parse string with latitude and longitude
    forecast = await get_forecast(lat, lon)
    await message.reply(forecast)


# this function replies with forecast when the user sends its location.
# To use it you should turn on gps, open paperclip icon, then geoloc and tap "send your location",
# so its more convenient to use /weather command in day-to-day use
@dp.message_handler(state="*", content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    forecast = await get_forecast(lat, lon)
    await message.reply(forecast)


async def get_forecast(lat: float, lon: float) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.openweathermap.org/data/{weather_api_version}/weather?lat={lat}&lon={lon}&appid={weather_api_key}")
        resp_data = resp.json()

    return create_forecast_message(resp_data)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
