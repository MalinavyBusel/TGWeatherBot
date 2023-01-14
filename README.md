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
