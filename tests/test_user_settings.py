import json
import unittest
import tempfile
from unittest.mock import mock_open, patch, MagicMock
from user_settings import UserSettings, SettingsDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class TestUserSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        self.user_settings = UserSettings()

    # 测试 loadConfig() 方法：正常加载配置
    @patch('builtins.open', return_value=MagicMock(read=MagicMock(return_value='{"username": "test_user"}')))
    @patch('json.load', return_value={"username": "test_user"})
    def test_load_config_valid(self, mock_json_load, mock_open):
        config = self.user_settings.loadConfig()
        self.assertEqual(config, {"username": "test_user"})

    # 测试 loadConfig() 方法：配置文件不存在
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_open):
        config = self.user_settings.loadConfig()
        self.assertEqual(config, self.user_settings.getDefaultConfig())

    # 测试 loadConfig() 方法：配置文件损坏
    @patch('builtins.open', return_value=MagicMock(read=MagicMock(return_value='{username: "test_user",}')))
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_config_invalid_json(self, mock_json_load, mock_open):
        config = self.user_settings.loadConfig()
        self.assertEqual(config, self.user_settings.getDefaultConfig())

    # 测试 saveConfig() 方法：保存配置
    def test_saveConfig(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_name = temp_file.name
        user_settings = UserSettings()
        user_settings.settings_file = temp_file_name
        config = {
            "username": "testuser",
            "selectedCity": "北京",
            "alerts": [True, False],
            "charac": "八云紫"
        }
        user_settings.saveConfig(config)
        saved_config = user_settings.loadConfig()
        self.assertEqual(saved_config, config)
        import os
        os.remove(temp_file_name)

    # 测试 getDefaultConfig() 方法
    def test_get_default_config(self):
        default_config = self.user_settings.getDefaultConfig()
        self.assertEqual(default_config, {
            "username": "默认用户",
            "selectedCity": "南京",
            "alerts": [False, False],
            "charac": "浅色"
        })

    # 测试 SettingsDialog：打开窗口并设置用户名
    @patch('user_settings.UserSettings.loadConfig', return_value={"username": "test_user"})
    def test_open_settings_dialog(self, mock_load_config):
        dialog = SettingsDialog(self.user_settings)
        dialog.username_edit.setText("new_user")
        dialog.saveSettings()
        self.assertEqual(dialog.username_edit.text(), "new_user")

    # 测试 SettingsDialog：点击保存按钮后更新配置
    @patch('user_settings.UserSettings.saveConfig')
    @patch('user_settings.UserSettings.loadConfig', return_value={"username": "old_user"})
    def test_save_settings(self, mock_load_config, mock_save_config):
        dialog = SettingsDialog(self.user_settings)
        dialog.username_edit.setText("new_user")
        dialog.saveSettings()
        mock_save_config.assert_called_once()
        self.assertEqual(dialog.username_edit.text(), "new_user")

    # 测试 SettingsDialog：恢复默认设置
    @patch('user_settings.UserSettings.saveConfig')
    def test_reset_to_default(self, mock_save_config):
        dialog = SettingsDialog(self.user_settings)
        dialog.username_edit.setText("changed_user")
        dialog.resetToDefaultSettings()
        self.assertEqual(dialog.username_edit.text(), "默认用户")
        mock_save_config.assert_called_once_with(dialog.user_settings.getDefaultConfig())

    # 测试 SettingsDialog：切换菜单并加载不同页面
    def test_switch_content(self):
        dialog = SettingsDialog(self.user_settings)
        dialog.switchContent(0)  # 切换到第一个页面
        self.assertEqual(dialog.content_stack.currentIndex(), 0)  # 个人账户页面

    # 测试 SettingsDialog：点击取消按钮
    def test_cancel_dialog(self):
        dialog = SettingsDialog(self.user_settings)
        dialog.reject()  # 模拟取消操作
        self.assertFalse(dialog.isVisible())  # 确保窗口关闭

if __name__ == "__main__":
    unittest.main()
