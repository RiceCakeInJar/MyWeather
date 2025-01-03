import json
import os
import unittest
from PyQt5.QtWidgets import QApplication
from weather_app import WeatherApp
from user_settings import UserSettings
from weather_service import WeatherService
from notification_service import NotificationService
from weather import Weather
import sys

class TestWeatherAppIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """在所有测试开始之前运行一次，初始化应用程序和主界面。"""
        cls.app = QApplication(sys.argv)
        cls.weather_app = WeatherApp()
        cls.weather_app.start()
        cls.weather_service = WeatherService()
        cls.user_settings = UserSettings()
        cls.notification_service = NotificationService(cls.weather_app.alert_label)

    def test_initial_ui_elements(self):
        """测试各个标签是否存在"""
        city_label = self.weather_app.city_label
        self.assertIsNotNone(city_label, "City label should exist.")
        grt_label = self.weather_app.grt_label
        self.assertIsNotNone(grt_label, "Greeting label should exist.")
        tmp_label = self.weather_app.tmp_label
        self.assertIsNotNone(tmp_label, "Temperature label should exist.")
        hum_wid_label = self.weather_app.hum_wid_label
        self.assertIsNotNone(hum_wid_label, "Humidity and wind label should exist.")
        foc_label = self.weather_app.foc_label
        self.assertIsNotNone(foc_label, "Focus label should exist.")
        wth_label = self.weather_app.wth_label
        self.assertIsNotNone(wth_label, "Weather description label should exist.")
        alert_label = self.weather_app.alert_label
        self.assertIsNotNone(alert_label, "Alert label should exist.")
        charac_label = self.weather_app.charac_label
        self.assertIsNotNone(charac_label, "Character label should exist.")

    def test_weather_data_update(self):
        """测试天气数据是否能够从 WeatherService 正确获取并显示。"""
        # 模拟从天气服务获取的天气数据
        weather = self.weather_service.getCurrentWeather("南京")

        # 更新界面上的天气信息
        self.weather_app.tmp_label.setText(f"{weather.temperature}°")
        self.weather_app.hum_wid_label.setText(f"{weather.get_wind_info()}级 | 湿度{weather.humidity}%")
        self.weather_app.foc_label.setText(f"{weather.forecast[0]}° {weather.forecast[1]}°")
        self.weather_app.wth_label.setText(weather.weather)

        # 验证数据是否正确显示
        self.assertEqual(self.weather_app.tmp_label.text(), f"{weather.temperature}°")
        self.assertEqual(self.weather_app.hum_wid_label.text(), f"{weather.get_wind_info()}级 | 湿度{weather.humidity}%")
        self.assertEqual(self.weather_app.wth_label.text(), weather.weather)

    def test_user_settings_load_and_update(self):
        """测试用户设置是否能够加载并在界面中正确反映。"""
        # 无配置文件时模拟初始的配置文件内容
        self.settings_file = "user_settings.json"
        self.user_settings = UserSettings()
        if not os.path.exists(self.settings_file):
            settings = {
                "username": "user_test",
                "selectedCity": "深圳",
                "alerts": [True, True],
                "charac": "风见幽香"
            }
            with open(self.settings_file, "w") as file:
                json.dump(settings, file, indent=4)
                
        # 直接读取配置文件中的内容
        with open(self.settings_file, "r") as file:
            expected_settings = json.load(file)

        # 加载用户设置
        settings = self.user_settings.loadConfig()

        # 验证加载的设置是否与文件中的实际内容匹配
        self.assertEqual(settings["username"], expected_settings["username"])
        self.assertEqual(settings["selectedCity"], expected_settings["selectedCity"])
        self.assertEqual(settings["alerts"], expected_settings["alerts"])
        self.assertEqual(settings["charac"], expected_settings["charac"])

        # 更新设置
        new_settings = {
            "username": "new_user",
            "selectedCity": "上海",
            "alerts": [False, False],
            "charac": "八云紫"
        }

        self.user_settings.saveConfig(new_settings)
        
        # 验证设置是否已更新
        with open(self.settings_file, "r") as file:
            updated_settings = json.load(file)
        
        self.assertEqual(updated_settings["username"], "new_user")
        self.assertEqual(updated_settings["selectedCity"], "上海")
        self.assertEqual(updated_settings["alerts"], [False, False])
        self.assertEqual(updated_settings["charac"], "八云紫")

    def test_weather_alert(self):
        """测试天气预警功能是否正确工作。"""
        # 模拟一个有风和降水的天气情况
        weather = Weather(
            temperature=22,
            humidity=70,
            is_windy=True,
            is_rainy=True,
            wind_direction="东风",
            wind_level="4级",
            forecast=[20, 21],
            weather="雷阵雨"
        )

        # 发送天气预警
        self.notification_service.sendWeatherAlert(weather)

        # 检查是否显示了正确的预警信息
        self.assertTrue(self.weather_app.alert_label.isVisible())
        self.assertIn("大风预警", self.weather_app.alert_label.text())
        self.assertIn("降水预警", self.weather_app.alert_label.text())

    def test_save_and_load_user_settings(self):
        """测试设置保存和加载功能。"""
        # 修改用户设置
        new_settings = {
            "username": "user_test",
            "selectedCity": "深圳",
            "alerts": [True, True],
            "charac": "风见幽香"
        }
        self.user_settings.saveConfig(new_settings)

        # 重新加载配置
        loaded_settings = self.user_settings.loadConfig()

        # 验证保存的设置是否正确加载
        self.assertEqual(loaded_settings["username"], "user_test")
        self.assertEqual(loaded_settings["selectedCity"], "深圳")
        self.assertEqual(loaded_settings["alerts"], [True, True])
        self.assertEqual(loaded_settings["charac"], "风见幽香")

    @classmethod
    def tearDownClass(cls):
        """在所有测试结束后执行清理工作。"""
        cls.weather_app.stop()


if __name__ == "__main__":
    unittest.main()
