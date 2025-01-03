import time
from PyQt5.QtWidgets import QGraphicsBlurEffect, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from user_settings import UserSettings
from weather_service import WeatherService
from notification_service import NotificationService


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_settings = UserSettings()
        self.weather_service = WeatherService()

        self.city = self.user_settings.loadSelectedCity() or "南京"
        self.username = self.user_settings.loadUserName() or "admin"
        self.character = self.user_settings.loadCharac() or "风见幽香"

        self.initUI()

    def initUI(self):
        self.setWindowTitle("MyWeather - HomePage")
        self.setGeometry(100, 100, 1000, 600)  # 宽1000，高600的窗口

        # 背景设置
        self.setBackground("background.png")

        # 添加 UI 组件
        self.city_label = self.createLabel(f"{self.city}", 60, 10, 600, 150, "Arial", 18, bold=True)
        self.grt_label = self.createLabel(self.getGreetingText(), 60, 450, 600, 150, "Arial", 12, bold=True)
        self.tmp_label = self.createLabel("<loading>°", 60, 105, 600, 200, "Arial", 60)
        self.hum_wid_label = self.createLabel("<loading>", 60, 260, 1000, 150, "Arial", 16, bold=True)
        self.foc_label = self.createLabel("<loading>", 410, 130, 1000, 200, "Arial", 20, bold=True)
        self.wth_label = self.createLabel("<loading>", 240, 130, 1000, 200, "Arial", 20, bold=True)
        self.alert_label = self.createLabel("", 60, 380, 300, 50, "Arial", 14, bold=True, center=True,
                                            style="color: white; background-color: blue; padding: 5px; border-radius: 10px;")
        self.alert_label.hide()

        self.notification_service = NotificationService(self.alert_label)

        # 图标按钮
        self.createButton("refresh_icon.png", self.refresh, 850, 20)  # 刷新
        self.createButton("settings_icon.png", self.openSettings, 920, 20)  # 设置


        # 界面装饰
        self.createLabel("|", 360, 120, 100, 150, "Arial", 50)
        self.createLabel("未来两小时", 410, 100, 400, 150, "Arial", 14)

        # 看板娘
        self.charac_label = QLabel(self)
        self.charac_label.setGeometry(800, 400, 200, 200)
        self.loadCharacterImage()
        # 初次更新天气
        self.refresh()

    def setBackground(self, image_path):
        """设置背景图和模糊效果"""
        background_label = QLabel(self)
        background_label.setGeometry(0, 0, 1000, 600)
        pixmap = QPixmap(image_path)
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        background_label.setGraphicsEffect(blur_effect)

    def loadCharacterImage(self):
        """加载用户选择的看板娘图片"""
        if self.character == "风见幽香":
            image_path = "char_0.png"  # 假设对应图片文件
        else:
            image_path = "char_1.png"
        pixmap = QPixmap(image_path)
        self.charac_label.setPixmap(pixmap)
        self.charac_label.setScaledContents(True)

    def createLabel(self, text, x, y, width, height, font_family, font_size, bold=False, center=False, style="color: white;"):
        """辅助函数：创建标签并设置样式"""
        label = QLabel(text, self)
        label.setGeometry(x, y, width, height)
        font = QFont(font_family, font_size)
        font.setBold(bold)
        label.setFont(font)
        label.setStyleSheet(style)
        if center:
            label.setAlignment(Qt.AlignCenter)
        return label

    def createButton(self, icon_path, callback, x, y, width=50, height=50):
        """辅助函数：创建图标按钮并绑定点击事件"""
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(width - 10, height - 10))
        button.setFixedSize(width, height)
        button.clicked.connect(callback)
        button.setStyleSheet("border: none; padding: 5px;")
        button.move(x, y)
        return button


    def getGreetingText(self):
        """获取时间段问候语"""
        hour = time.localtime().tm_hour
        if 5 <= hour < 9:
            return f"早上好, {self.username}"
        elif 9 <= hour < 12:
            return f"上午好, {self.username}"
        elif 12 <= hour < 14:
            return f"中午好, {self.username}"
        elif 14 <= hour < 18:
            return f"下午好, {self.username}"
        else:
            return f"晚上好, {self.username}"

    def refresh(self):
        """更新天气数据并刷新界面"""
        weather = self.weather_service.getCurrentWeather(self.city)
        self.city_label.setText(f"{self.city}")
        self.tmp_label.setText(f"{weather.temperature}°")
        self.hum_wid_label.setText(f"{weather.get_wind_info()}级 | 湿度{weather.humidity}%")
        self.foc_label.setText(f"{weather.forecast[0]}° {weather.forecast[1]}°")
        self.wth_label.setText(f"{weather.weather}")
        self.grt_label.setText(self.getGreetingText())
        self.loadCharacterImage()
        self.notification_service.sendWeatherAlert(weather)

    def updateUserSettings(self, updated_settings):
        """接收设置更新并更新主界面"""
        self.username = updated_settings.get("username", self.username)
        self.city = updated_settings.get("selectedCity", self.city)
        self.character = updated_settings.get("charac", self.character)
        self.refresh()
        print("用户设置已更新:", updated_settings)

    def openSettings(self):
        """打开设置界面"""
        self.user_settings.openSettingsDialog(parent=self, on_settings_updated=self.updateUserSettings)

    def start(self):
        self.show()

    def stop(self):
        self.close()
