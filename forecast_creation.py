def create_forecast_message(resp_data):
    return f"""Населенный пункт: {resp_data['name']},
температура: {get_temp_celsius(resp_data['main']['temp'])}°C,
ощущается как: {get_temp_celsius(resp_data['main']['feels_like'])}°C,
ветер: {resp_data['wind']['speed']}м/с, направление: {get_wind_direction(resp_data['wind']['deg'])},
{resp_data['weather'][0]['description']} {get_weather_emoji(resp_data['weather'][0]['id'])*3}"""


def get_temp_celsius(kelvin: float):
    return int(kelvin - 273.15)


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
