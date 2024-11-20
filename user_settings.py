import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QCheckBox, QListWidget, QStackedWidget, QWidget, QListWidgetItem
)
from PyQt5.QtCore import pyqtSignal, Qt


class UserSettings:
    def __init__(self):
        self.settings_file = "user_settings.json"

    def loadConfig(self):
        """加载用户配置文件，若文件不存在或损坏则返回默认配置。"""
        try:
            with open(self.settings_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.getDefaultConfig()

    def saveConfig(self, settings):
        """保存用户配置到文件。"""
        with open(self.settings_file, "w") as file:
            json.dump(settings, file, indent=4)

    def loadUserName(self):
        return self.loadConfig().get("username", "默认用户")

    def loadSelectedCity(self):
        return self.loadConfig().get("selectedCity", "南京")

    def loadAlerts(self):
        return self.loadConfig().get("alerts", [False, False])

    def loadCharac(self):
        return self.loadConfig().get("charac", "风见幽香")

    def getDefaultConfig(self):
        """返回默认配置，避免多处硬编码。"""
        return {
            "username": "默认用户",
            "selectedCity": "南京",
            "alerts": [False, False],
            "charac": "浅色"
        }

    def openSettingsDialog(self, parent, on_settings_updated):
        """打开设置窗口。"""
        dialog = SettingsDialog(self, parent)
        dialog.settingsUpdated.connect(on_settings_updated)
        dialog.exec_()


class SettingsDialog(QDialog):
    settingsUpdated = pyqtSignal(dict)

    def __init__(self, user_settings, parent=None):
        super().__init__(parent)
        self.user_settings = user_settings
        self.setWindowTitle("NewWeather - 设置")
        self.setFixedSize(500, 400)
        self.initUI()

    def initUI(self):
        """初始化界面布局和控件。"""
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # 主布局：左侧菜单 + 右侧内容
        content_layout = QGridLayout()
        main_layout.addLayout(content_layout)

        self.initMenu(content_layout)  # 初始化左侧菜单
        self.initContentStack(content_layout)  # 初始化右侧内容区域

        # 添加功能按钮
        self.addControlButtons(main_layout)

    def initMenu(self, layout):
        """初始化左侧菜单。"""
        self.menu = QListWidget()
        self.menu.addItems(["个人账户", "天气预警", "看板娘", "城市", "关于"])
        self.menu.setFixedWidth(120)
        self.menu.currentRowChanged.connect(self.switchContent)
        layout.addWidget(self.menu, 0, 0)

    def initContentStack(self, layout):
        """初始化右侧内容区域。"""
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack, 0, 1)

        # 各功能页面
        self.initAccountPage()
        self.initNotificationsPage()
        self.initCharacPage()
        self.initCitySelectionPage()
        self.initAboutPage()

    def addControlButtons(self, layout):
        """添加保存和恢复默认按钮。"""
        button_layout = QGridLayout()
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.saveSettings)
        reset_button = QPushButton("恢复默认设置")
        reset_button.clicked.connect(self.resetToDefaultSettings)
        button_layout.addWidget(save_button, 0, 0)
        button_layout.addWidget(reset_button, 0, 1)

        layout.addLayout(button_layout)

    def initAccountPage(self):
        """初始化个人账户设置页。"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("用户名:"))
        self.username_edit = QLineEdit(self.user_settings.loadUserName())
        layout.addWidget(self.username_edit)
        self.content_stack.addWidget(page)

    def initNotificationsPage(self):
        """初始化预警设置页。"""
        page = QWidget()
        layout = QVBoxLayout(page)
        alerts = self.user_settings.loadAlerts()

        self.alert_icon_checkbox = QCheckBox("图标预警")
        self.alert_icon_checkbox.setChecked(alerts[0])
        layout.addWidget(self.alert_icon_checkbox)

        self.alert_popup_checkbox = QCheckBox("弹窗预警")
        self.alert_popup_checkbox.setChecked(alerts[1])
        layout.addWidget(self.alert_popup_checkbox)

        self.content_stack.addWidget(page)

    def initCitySelectionPage(self):
        """初始化城市设置页。"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("选择默认城市:"))

        self.city_combobox = QComboBox()
        self.city_combobox.addItems(["南京", "北京", "上海", "广州", "深圳"])
        self.city_combobox.setCurrentText(self.user_settings.loadSelectedCity())
        layout.addWidget(self.city_combobox)

        self.content_stack.addWidget(page)

    def initCharacPage(self):
        """初始化看板娘设置页。"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("选择看板娘:"))

        self.charac_combobox = QComboBox()
        self.charac_combobox.addItems(["风见幽香", "八云紫"])
        self.charac_combobox.setCurrentText(self.user_settings.loadCharac())
        layout.addWidget(self.charac_combobox)

        self.content_stack.addWidget(page)

    def initAboutPage(self):
        """初始化关于页面。"""
        page = QWidget()
        layout = QVBoxLayout(page)
        about_label = QLabel("NewWeather v1.0\n作者: NJUCS Craly")
        about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_label)

        self.content_stack.addWidget(page)

    def switchContent(self, index):
        """切换右侧内容区域的显示页面。"""
        self.content_stack.setCurrentIndex(index)

    def saveSettings(self):
        """保存当前设置到配置文件。"""
        config = self.user_settings.loadConfig()
        config.update({
            "username": self.username_edit.text(),
            "alerts": [
                self.alert_icon_checkbox.isChecked(),
                self.alert_popup_checkbox.isChecked(),
            ],
            "selectedCity": self.city_combobox.currentText(),
            "charac": self.charac_combobox.currentText(),
        })
        self.user_settings.saveConfig(config)
        self.settingsUpdated.emit(config)
        self.accept()

    def resetToDefaultSettings(self):
        """恢复默认设置。"""
        default_config = self.user_settings.getDefaultConfig()

        # 更新控件状态
        self.username_edit.setText(default_config["username"])
        self.city_combobox.setCurrentText(default_config["selectedCity"])
        self.alert_icon_checkbox.setChecked(default_config["alerts"][0])
        self.alert_popup_checkbox.setChecked(default_config["alerts"][1])
        self.charac_combobox.setCurrentText(default_config["charac"])

        # 保存并发出信号
        self.user_settings.saveConfig(default_config)
        self.settingsUpdated.emit(default_config)
