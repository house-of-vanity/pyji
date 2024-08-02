import os
import configparser
import platform

def get_config_path(config=True):
    app_name = 'PyJi'
    config_filename = 'config.ini'

    if platform.system() == 'Windows':
        config_dir = os.path.join(os.getenv('APPDATA'), app_name)
    else:
        config_dir = os.path.join(os.getenv('HOME'), '.config', app_name)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(os.path.join(config_dir, 'decks')):
        os.makedirs(os.path.join(config_dir, 'decks'))

    return os.path.join(config_dir, config_filename) if config else config_dir

def read_config(config_path):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    else:
        config['UI'] = {}
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    return config

def write_config(config):
    config_path = get_config_path()
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def init():
    config_path = get_config_path()
    config = read_config(config_path)
    return config
