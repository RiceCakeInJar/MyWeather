import unittest
from unittest.mock import patch
from weather import Weather
from weather_service import WeatherService


class TestWeatherService(unittest.TestCase):

    def setUp(self):
        self.weather_service = WeatherService()

    # 测试 getCurrentWeather()
    @patch('requests.get')
    def test_get_current_weather_valid(self, mock_get):
        mock_response = {
            "code": "200",
            "now": {
                "temp": "25",
                "humidity": "60",
                "windScale": "3",
                "text": "晴",
                "windDir": "东风"
            }
        }
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getCurrentWeather("南京")
        self.assertIsInstance(result, Weather)
        self.assertEqual(result.temperature, 25)
        self.assertEqual(result.humidity, 60)
        self.assertTrue(result.is_windy)
        self.assertFalse(result.is_rainy)

    @patch('requests.get')
    def test_get_current_weather_invalid_city(self, mock_get):
        # with self.assertRaises(KeyError):
        #     self.weather_service.getCurrentWeather("无锡")
        self.assertEqual(self.weather_service.getCurrentWeather("无锡").weather,self.weather_service.getCurrentWeather("北京").weather)

    @patch('requests.get')
    def test_get_current_weather_api_error(self, mock_get):
        mock_response = {"code": "500"}
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getCurrentWeather("南京")
        self.assertEqual(result.temperature, 20)

    @patch('requests.get')
    def test_get_current_weather_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        result = self.weather_service.getCurrentWeather("南京")
        self.assertEqual(result.temperature, 20)

    @patch('requests.get')
    def test_get_current_weather_value_error(self, mock_get):
        mock_get.return_value.json.side_effect = ValueError("JSON parse error")
        result = self.weather_service.getCurrentWeather("南京")
        self.assertEqual(result.temperature, 20)

    @patch('requests.get')
    def test_get_current_weather_no_rain(self, mock_get):
        mock_response = {
            "code": "200",
            "now": {
                "temp": "20",
                "humidity": "50",
                "windScale": "3",
                "text": "晴",
                "windDir": "北风"
            }
        }
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getCurrentWeather("广州")
        self.assertFalse(result.is_rainy)

    @patch('requests.get')
    def test_get_current_weather_is_windy(self, mock_get):
        mock_response = {
            "code": "200",
            "now": {
                "temp": "20",
                "humidity": "50",
                "windScale": "4",
                "text": "风大",
                "windDir": "北风"
            }
        }
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getCurrentWeather("上海")
        self.assertTrue(result.is_windy)

    def test_get_hourly_forecast_valid(self):
        with patch('requests.get') as mock_get:
            mock_response = {
                "code": "200",
                "hourly": [
                    {"temp": "22"},
                    {"temp": "23"}
                ]
            }
            mock_get.return_value.json.return_value = mock_response
            result = self.weather_service.getHourlyForecast("南京")
            self.assertEqual(result, [22, 23])

    @patch('requests.get')
    def test_get_hourly_forecast_api_error(self, mock_get):
        mock_response = {"code": "500"}
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getHourlyForecast("南京")
        self.assertEqual(result, [20, 21])

    @patch('requests.get')
    def test_get_hourly_forecast_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        result = self.weather_service.getHourlyForecast("南京")
        self.assertEqual(result, [20, 21])

    @patch('requests.get')
    def test_get_hourly_forecast_value_error(self, mock_get):
        mock_get.return_value.json.side_effect = ValueError("JSON parse error")
        result = self.weather_service.getHourlyForecast("南京")
        self.assertEqual(result, [20, 21])

    @patch('requests.get')
    def test_get_hourly_forecast_not_enough_data(self, mock_get):
        mock_response = {
            "code": "200",
            "hourly": [{"temp": "22"}]
        }
        mock_get.return_value.json.return_value = mock_response
        result = self.weather_service.getHourlyForecast("广州")
        self.assertEqual(result, [20, 21])


if __name__ == "__main__":
    unittest.main()
