import unittest
from unittest.mock import Mock, patch
from hypothesis import given, strategies as st
from weather_service import WeatherService
from weather import Weather
import json

# 模拟的API返回数据
def mock_get_weather_data(city, params):
    """模拟API返回的天气数据"""
    mock_response = Mock()
    # 设置模拟的返回状态码
    mock_response.status_code = 200  # 模拟一个成功的响应
    # 模拟 `raise_for_status()` 方法，不抛出异常
    mock_response.raise_for_status = Mock()
    # 设置模拟的响应内容
    mock_response.json.return_value = {
        "code": "200",
        "now": {
            "temp": "20",  # 温度
            "humidity": "50",  # 湿度
            "windScale": "3",  # 风力
            "text": "晴",  # 天气描述
            "windDir": "东风",  # 风向
        },
        "hourly": [
            {"temp": "19"},  # 未来1小时的温度
            {"temp": "21"}   # 未来2小时的温度
        ]
    }

    return mock_response

class TestWeatherService(unittest.TestCase):

    # 测试WeatherService正常数据处理
    @given(st.text())
    def test_get_weather_normal(self, city):
        weather_service = WeatherService()

        # 使用patch模拟API请求，返回模拟数据
        with patch('requests.get', side_effect=mock_get_weather_data):
            weather = weather_service.getCurrentWeather(city)

            # 检查返回的Weather对象的各个属性
            self.assertIsInstance(weather, Weather)
            self.assertIsInstance(weather.temperature, int)
            self.assertIsInstance(weather.humidity, int)
            self.assertIsInstance(weather.is_windy, bool)
            self.assertIsInstance(weather.is_rainy, bool)
            self.assertIsInstance(weather.wind_direction, str)
            self.assertIsInstance(weather.wind_level, str)
            self.assertIsInstance(weather.forecast, list)
            self.assertIsInstance(weather.weather, str)
            self.assertEqual(weather.weather, "晴")  # 根据模拟数据检查

    # 测试WeatherService应对API返回空数据
    @given(st.text())
    def test_get_weather_empty_response(self, city):
        # 模拟API返回空数据
        def mock_get_weather_data_empty(city):
            return {}

        weather_service = WeatherService()

        # 使用patch模拟API请求，返回空数据
        with patch('requests.get', side_effect=mock_get_weather_data_empty):
            weather = weather_service.getCurrentWeather(city)

            # 检查返回的Weather对象是否是默认值
            self.assertIsInstance(weather, Weather)
            self.assertEqual(weather.temperature, 20)  # 默认值
            self.assertEqual(weather.humidity, 50)  # 默认值
            self.assertFalse(weather.is_windy)  # 默认值
            self.assertFalse(weather.is_rainy)  # 默认值
            self.assertEqual(weather.weather, "未知")  # 默认值

if __name__ == "__main__":
    unittest.main()
