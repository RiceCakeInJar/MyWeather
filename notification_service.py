from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class NotificationService:
    def __init__(self, alert_label: QLabel):
        """
        :param alert_label: 用于显示预警的 QLabel 来自主界面
        """
        self.alert_label = alert_label
        self.isEnabled = True

        # 初始化标签样式
        self.alert_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.alert_label.setAlignment(Qt.AlignCenter)
        self.alert_label.setStyleSheet(
            "color: white; background-color: blue; padding: 5px; border-radius: 10px;"
        )
        self.alert_label.hide()  # 默认隐藏

    def sendWeatherAlert(self, weather):
        """
        显示天气预警信息到主界面警告标签
        :param weather: 天气对象，包含 is_windy 和 is_rainy 属性
        """
        if self.isEnabled:
            alerts = []  # 用于存储所有风险类型

            if weather.is_windy:
                alerts.append("大风预警")
            if weather.is_rainy:
                alerts.append("降水预警")

            if alerts:
                # 设置警告文本
                self.alert_label.setText(" | ".join(alerts))
                # 调整标签大小以适应文本
                self.alert_label.adjustSize()
                self.alert_label.show()
            else:
                self.alert_label.hide()  # 无预警时隐藏标签
