import random
from weather import Weather

class WeatherService:
    def getCurrentWeather(self, city):
        wind_directions = ["东风", "西风", "南风", "北风"]
        wind_level = f"{random.randint(1, 5)}级"  # 随机生成风力等级 1-5 级
        wind_direction = random.choice(wind_directions)  # 随机选择风向
        weathers = ["晴","阴","多云","阵风","小雨","大雨","暴雨"]
        weather = random.choice(weathers)  # 随机选择天气
        
        return Weather(
            temperature=random.randint(15, 30),
            humidity=random.randint(30, 70),
            is_windy=bool(random.getrandbits(1)),
            is_rainy=bool(random.getrandbits(1)),
            wind_direction=wind_direction,
            wind_level=wind_level,
            forecast=[random.randint(15, 30), random.randint(15, 30)],
            weather=weather
        )