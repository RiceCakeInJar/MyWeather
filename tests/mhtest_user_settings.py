import unittest
from hypothesis import given, strategies as st
from user_settings import UserSettings
import json
import os

class TestUserSettings(unittest.TestCase):

    def setUp(self):
        """在每个测试前清除配置文件，确保测试的独立性。"""
        self.settings_file = "user_settings.json"
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)

    def tearDown(self):
        """清理测试后的设置文件。"""
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)

    def test_load_default_config_when_file_not_exists(self):
        """测试配置文件不存在时，加载默认配置。"""
        user_settings = UserSettings()
        config = user_settings.loadConfig()

        default_config = user_settings.getDefaultConfig()
        self.assertEqual(config, default_config)

    @given(
        st.text(),  # 用户名
        st.text(),  # 城市
        st.lists(st.booleans(), min_size=2, max_size=2),  # alerts
        st.text()   # 看板娘
    )
    def test_save_and_load_config(self, username, city, alerts, charac):
        """测试保存和加载配置功能。"""
        user_settings = UserSettings()

        # 创建模拟配置
        config = {
            "username": username,
            "selectedCity": city,
            "alerts": alerts,
            "charac": charac
        }

        # 保存配置
        user_settings.saveConfig(config)

        # 加载并验证配置
        loaded_config = user_settings.loadConfig()

        self.assertEqual(config["username"], loaded_config["username"])
        self.assertEqual(config["selectedCity"], loaded_config["selectedCity"])
        self.assertEqual(config["alerts"], loaded_config["alerts"])
        self.assertEqual(config["charac"], loaded_config["charac"])

    @given(
        st.text(min_size=1),  # 用户名
        st.text(min_size=1),  # 城市
        st.lists(st.booleans(), min_size=2, max_size=2),  # alerts
        st.text(min_size=1)   # 看板娘
    )
    def test_save_and_load_individual_keys(self, username, city, alerts, charac):
        """测试保存和加载单个配置项。"""
        user_settings = UserSettings()

        # 保存单个配置项
        user_settings.saveConfig({
            "username": username,
            "selectedCity": city,
            "alerts": alerts,
            "charac": charac
        })

        # 验证每个键的加载
        self.assertEqual(user_settings.loadUserName(), username)
        self.assertEqual(user_settings.loadSelectedCity(), city)
        self.assertEqual(user_settings.loadAlerts(), alerts)
        self.assertEqual(user_settings.loadCharac(), charac)

    def test_reset_to_default(self):
        """测试恢复到默认配置。"""
        user_settings = UserSettings()

        # 创建并保存一个自定义配置
        custom_config = {
            "username": "CustomUser",
            "selectedCity": "北京",
            "alerts": [True, True],
            "charac": "八云紫"
        }
        user_settings.saveConfig(custom_config)

        # 重置为默认配置
        user_settings.saveConfig(user_settings.getDefaultConfig())

        # 验证配置是否恢复为默认
        default_config = user_settings.getDefaultConfig()
        self.assertEqual(user_settings.loadConfig(), default_config)


if __name__ == "__main__":
    unittest.main()
