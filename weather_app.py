import sys
from PyQt5.QtWidgets import QGraphicsBlurEffect, QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QMessageBox, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QPixmap,QFont, QColor
from PyQt5.QtCore import Qt
from user_settings import UserSettings
from weather_service import WeatherService
from notification_service import NotificationService

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_settings = UserSettings()
        self.city = self.user_settings.loadSelectedCity() or "南京市"  # 默认城市
        self.weather_service = WeatherService()
        # self.notification_service = NotificationService(self.alert_label)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MyWeather - HomePage")
        self.setGeometry(100, 100, 1000, 600)  # 宽1000，高600的窗口

        # 设置背景图
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 1000, 600)  # 设置背景图片大小和位置
        pixmap = QPixmap("background.png")  # 替换为你的背景图片路径
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)  # 使背景图片自动适应窗口大小
        # 添加模糊效果
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)  # 设置模糊半径
        self.background_label.setGraphicsEffect(blur_effect)
        
        # 显示所选城市
        self.city_label = QLabel(f"{self.city}  ▼", self)
        self.city_label.setFixedWidth(600)
        self.city_label.setFixedHeight(150)
        font = QFont("Arial", 18)
        font.setBold(True)  # 设置加粗
        self.city_label.setFont(font)
        self.city_label.setStyleSheet("color: white;")
        self.city_label.move(60, 10)

        # 温度标签
        self.tmp_label = QLabel("<loading>°", self)
        self.tmp_label.setFixedWidth(600)
        self.tmp_label.setFixedHeight(200)
        font = QFont("Arial", 60)
        font.setBold(False)  # 设置加粗
        self.tmp_label.setFont(font)
        self.tmp_label.setStyleSheet("color: white;")
        self.tmp_label.move(60, 105)

        # 湿度与风向标签
        self.hum_wid_label = QLabel("<loading>", self)
        self.hum_wid_label.setFixedWidth(1000)
        self.hum_wid_label.setFixedHeight(150)
        font = QFont("Arial", 18)
        font.setBold(True)  # 设置加粗
        self.hum_wid_label.setFont(font)
        self.hum_wid_label.setStyleSheet("color: white;")
        self.hum_wid_label.move(60, 240)

        # 预报标签
        self.foc_label = QLabel("<loading>", self)
        self.foc_label.setFixedWidth(1000)
        self.foc_label.setFixedHeight(200)
        font = QFont("Arial", 20)
        font.setBold(True)  # 设置加粗
        self.foc_label.setFont(font)
        self.foc_label.setStyleSheet("color: white;")
        self.foc_label.move(410, 130)
        
        # 天气标签
        self.wth_label = QLabel("<loading>", self)
        self.wth_label.setFixedWidth(1000)
        self.wth_label.setFixedHeight(200)
        font = QFont("Arial", 20)
        font.setBold(True)  # 设置加粗
        self.wth_label.setFont(font)
        self.wth_label.setStyleSheet("color: white;")
        self.wth_label.move(240, 130)
        
        # 预警标签
        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(98, 360, 300, 50)  # 设置位置和大小
        font = QFont("Arial", 14)
        font.setBold(True)  # 加粗字体
        self.alert_label.setFont(font)
        self.alert_label.setAlignment(Qt.AlignCenter)  # 居中显示文字
        self.alert_label.setStyleSheet(
            "color: white; background-color: blue; padding: 5px; border-radius: 10px;"
        )
        self.alert_label.hide()  # 默认隐藏
        
        self.notification_service = NotificationService(self.alert_label)
        
        # 刷新按钮
        self.refresh_button = QPushButton("刷新", self)
        self.refresh_button.clicked.connect(self.updateWeather)
        self.refresh_button.move(600, 20)

        # 设置按钮
        self.settings_button = QPushButton("设置", self)
        self.settings_button.clicked.connect(self.openSettings)
        self.settings_button.move(700, 20)

        # 界面装饰元素
        # 预报分割线
        self.dic_label_0 = QLabel("|", self)
        self.dic_label_0.setFixedWidth(100)
        self.dic_label_0.setFixedHeight(150)
        font = QFont("Arial", 50)
        font.setBold(False)  # 设置加粗
        self.dic_label_0.setFont(font)
        self.dic_label_0.setStyleSheet("color: white;")
        self.dic_label_0.move(360, 120)  
        
        # 预报标题
        self.dic_label_1 = QLabel("未来两小时", self)
        self.dic_label_1.setFixedWidth(400)
        self.dic_label_1.setFixedHeight(150)
        font = QFont("Arial", 18)
        font.setBold(False)  # 设置加粗
        self.dic_label_1.setFont(font)
        self.dic_label_1.setStyleSheet("color: white;")
        self.dic_label_1.move(410, 100) 
        
        # 初次更新天气
        self.updateWeather()

    def updateWeather(self):
        # 获取当前天气数据
        weather = self.weather_service.getCurrentWeather(self.city)
        
        # 更新各个标签的内容
        self.tmp_label.setText(f"{weather.temperature}°")
        self.hum_wid_label.setText(f"{weather.get_wind_info()} | 湿度{weather.humidity}%")
        self.foc_label.setText(f"{weather.forecast[0]}° {weather.forecast[1]}°")
        self.wth_label.setText(f"{weather.weather}")
        
        # 风险预警
        self.notification_service.sendWeatherAlert(weather)

    def openSettings(self):
        # 打开设置窗口，示例代码仅弹出消息框
        QMessageBox.information(self, "设置", "进入设置界面")

    def start(self):
        self.show()

    def stop(self):
        self.close()
