import requests
from weather import Weather


class WeatherService:
    def __init__(self):
        self.api_key = "1065a96d69544fd3aa192c26b5eac905"
        self.current_weather_url = "https://devapi.qweather.com/v7/weather/now"
        self.hourly_forecast_url = "https://devapi.qweather.com/v7/weather/24h"
        self.city_id = {"南京": 101190101, "上海": 101020100,
                        "北京": 101010100, "广州": 101280101, "深圳": 101280601}

    def getCurrentWeather(self, city):
        # 城市名转代码
        city = self.city_id[city]  # 默认南京

        # 构造当前天气请求参数
        params = {
            "location": city,
            "key": self.api_key
        }

        try:
            # 发起当前天气请求
            response = requests.get(self.current_weather_url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()

            # 检查返回的状态码
            if data.get("code") != "200":
                raise ValueError(f"API 返回错误码：{data.get('code')}")

            # 解析 JSON 数据
            now_data = data.get("now", {})
            temperature = int(now_data.get("temp", 20))  # 默认温度为 20
            humidity = int(now_data.get("humidity", 50))  # 默认湿度为 50
            is_windy = int(now_data.get("windScale", 0)) >= 3  # 风力大于等于 3 级视为有风
            is_rainy = now_data.get("text", "").find(
                "雨") != -1  # 天气描述中包含“雨”视为下雨
            wind_direction = now_data.get("windDir", "未知")
            wind_level = now_data.get("windScale", "未知")
            weather_description = now_data.get("text", "未知")

            # 获取未来两小时天气预报
            forecast = self.getHourlyForecast(city)

            # 返回 Weather 对象
            return Weather(
                temperature=temperature,
                humidity=humidity,
                is_windy=is_windy,
                is_rainy=is_rainy,
                wind_direction=wind_direction,
                wind_level=wind_level,
                forecast=forecast,
                weather=weather_description
            )

        except requests.RequestException as e:
            print(f"网络请求失败：{e}")
        except ValueError as e:
            print(f"数据解析错误：{e}")
        except Exception as e:
            print(f"未知错误：{e}")

        # 如果发生错误，返回默认值
        return Weather(
            temperature=20,
            humidity=50,
            is_windy=False,
            is_rainy=False,
            wind_direction="未知",
            wind_level="未知",
            forecast=[20, 21],
            weather="未知"
        )

    def getHourlyForecast(self, city):
        """获取未来两小时逐小时天气预报"""
        params = {
            "location": city,
            "key": self.api_key
        }

        try:
            response = requests.get(self.hourly_forecast_url, params=params)
            response.raise_for_status()
            data = response.json()

            # 检查返回的状态码
            if data.get("code") != "200":
                raise ValueError(f"API 返回错误码：{data.get('code')}")

            # 提取未来两小时的温度
            hourly_forecast = data.get("hourly", [])
            return [
                int(hourly_forecast[i]["temp"])
                for i in range(2)
            ] if len(hourly_forecast) >= 2 else [20, 21]  # 默认值

        except requests.RequestException as e:
            print(f"网络请求失败：{e}")
        except ValueError as e:
            print(f"数据解析错误：{e}")
        except Exception as e:
            print(f"未知错误：{e}")

        # 发生错误时返回默认值
        return [20, 21]
