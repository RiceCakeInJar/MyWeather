import json


class UserSettings:
    def __init__(self):
        self.settings_file = "user_settings.json"

    def loadConfig(self):
        try:
            with open(self.settings_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def saveConfig(self, settings):
        with open(self.settings_file, "w") as file:
            json.dump(settings, file)

    def loadSelectedCity(self):
        config = self.loadConfig()
        return config.get("selectedCity")

    def saveSelectedCity(self, city):
        config = self.loadConfig()
        config["selectedCity"] = city
        self.saveConfig(config)
