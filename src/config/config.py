import configparser

class ConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        try:
            self.config.read(self.file_path)
        except configparser.Error as e:
            print(f"Error reading config file: {str(e)}")

    def get_value(self, section, key):
        try:
            return self.config[section][key]
        except KeyError:
            print(f"Key not found in config file: [{section}] {key}")
            return None
        except configparser.Error as e:
            print(f"Error accessing config file: {str(e)}")
            return None

    def get_token(self):
        try:
            return self.config['GITHUB']['TOKEN']
        except KeyError:
            print("Token not found in config file.")
            return None
