# TGWeatherBot
[![Supported python versions](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-lightgrey?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api/)
[![Aiogram](https://img.shields.io/badge/Aiogram-blue?style=flat-square)](https://github.com/aiogram/aiogram/)

Простой бот для получения прогноза погоды через телеграм.


## Примеры работы
Получение прогноза при отправке геолокации:
<p>
    <img src="readme-imgs/example1.PNG" />
</p>

Получение прогноза при заданной геолокации:
<p>
    <img src="readme-imgs/example2.PNG" />
</p>


## Команды
/start, /help - стандартные команды;

'Вложения -> Геопозиция -> Отправить свою геопозицию' - возвращает погоду для отправленного местоположения;

/set_location - просит отправить местоположение и устанавливает его как стандартное;

/weather - возвращает погоду для стандартного местоположения, поставленного через /set_location. В целом проще и удобнее,
чем каждый раз отправлять местоположение заново, поэтому при ежедневном использовании предполагается использовать её.


## Установка
1. Создаём телеграм бота в [BotFather](https://telegram.me/BotFather). По желанию там же можно сразу установить начальное описание бота и изображение профиля.

2. Регистрируем аккаунт [Openweathermap](https://openweathermap.org) и получаем ключ для использования API текущей погоды.
До 1000 запросов в день можно совершить бесплатно.

3. Создаем в папке config файл под названием .env и помещаем туда токен нашего бота, а также ключ от openweathermap api. И ключ, и токен указываем без кавычек.
<p align="center">
    <img src="readme-imgs/config_example.PNG" />
</p>

4. Пользуемся
