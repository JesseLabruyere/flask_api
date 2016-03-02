import yaml


class ConfigLoader:

    def __init__(self):
        pass

    @staticmethod
    def load_config():
        with open("config/config.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config
