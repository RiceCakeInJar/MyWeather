from PyQt5.QtWidgets import QMessageBox

class NotificationService:
    def __init__(self):
        self.isEnabled = True

    def sendWeatherAlert(self, weather):
        if self.isEnabled:
            if weather.is_windy:
                message = f"风暴预警"
                QMessageBox.information(None, "Warning", message)
            if weather.is_rainy:
                message = "暴雨预警"
                QMessageBox.information(None, "Warning", message)
