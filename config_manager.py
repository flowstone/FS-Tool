import json


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                self.db_location = config['database']['location']
                self.answer_pwd = config['AutoAnswers']['password']
                self.answer_driver = config['AutoAnswers']['driver']
        except (FileNotFoundError, KeyError):
            print("配置文件有误")