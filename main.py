import sys
from PyQt5.QtWidgets import QApplication
from weather_app import WeatherApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.start()
    sys.exit(app.exec_())
