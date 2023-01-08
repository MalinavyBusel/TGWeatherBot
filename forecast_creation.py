def create_forecast_message(resp_data: dict) -> str:
    """
    Returns the forecast message to show to the user.

    :param resp_data: the .json() of the openweathermap response
    """
    return f"""Населенный пункт: {resp_data['name']},
температура: {temp_to_celsius(resp_data['main']['temp'])}°C,
ощущается как: {temp_to_celsius(resp_data['main']['feels_like'])}°C,
ветер: {resp_data['wind']['speed']}м/с, направление: {get_wind_direction(resp_data['wind']['deg'])},
{resp_data['weather'][0]['description']} {get_weather_emoji(resp_data['weather'][0]['id'])*3}"""


def temp_to_celsius(kelvin: float) -> int:
    """
    Converts the temperature in kelvin to temperature in celsius.
    """
    return int(kelvin - 273.15)


def get_wind_direction(degree: int | float) -> str:
    """
    Returns the wind direction in compass letters from it's movement degree.
    N - north, SW - south-west and etc.
    """
    if degree < 22.5 or degree > 337.5:
        return "N"  # North
    elif degree < 67.5:
        return "NE"
    elif degree < 112.5:
        return "E"  # East
    elif degree < 157.5:
        return "SE"
    elif degree < 202.5:
        return "S"  # South
    elif degree < 247.5:
        return "SW"
    elif degree < 292.5:
        return "W"  # West
    elif degree <= 337.5:
        return "NW"


def get_weather_emoji(weather_id: int) -> str:
    """
    Returns the emoji associated with given weather id.
    """
    if weather_id in range(200, 203) or weather_id in range(230, 233):
        return "⛈"  # thunderstorm with rain
    elif weather_id in range(210, 213):
        return "🌩"  # thunderstorm
    elif weather_id in range(300, 322) or weather_id in range(500, 532):
        return "🌧"  # rain or drizzle
    elif weather_id in range(600, 623):
        return "🌨"  # snow
    elif weather_id in range(701, 763):
        return "🌫"  # mist, fog and other
    elif weather_id == 771:
        return "🌬"  # squall
    elif weather_id == 781:
        return "🌪"  # tornado
    elif weather_id == 800:
        return "☀"  # clear sky
    elif weather_id == 801 or weather_id == 802:
        return "🌤"  # few clouds
    elif weather_id == 803 or weather_id == 804:
        return "🌥"  # broken clouds
    else:
        return ""  # unknown weather id
