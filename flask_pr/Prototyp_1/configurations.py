import configparser

class config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def get_option(self, section, option):
        return self.config.get(section, option)

    def set_option(self, section, option, value):
        self.config[section][option] = value
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)

if __name__ == '__main__':
# Example usage:
    config_path = 'config.ini'
    my_config = config(config_path)

    # Reading from the config
    option_value = my_config.get_option('Settings', 'max_num_boxes')
    print(f'Option value: {option_value}')

    # Modifying the config
    #my_config.set_option('Settings', 'option1', 'new_value')
