class Weather:
    def __init__(self, temperature, humidity, is_windy, is_rainy, wind_direction, wind_level, forecast, weather):
        self.temperature = temperature
        self.humidity = humidity
        self.is_windy = is_windy
        self.is_rainy = is_rainy
        self.wind_direction = wind_direction  # 风向，例如 "东风"
        self.wind_level = wind_level  # 风力等级，例如 "2级"
        self.forecast = forecast
        self.weather = weather
        
    def get_wind_info(self):
        return f"{self.wind_direction}{self.wind_level}"
