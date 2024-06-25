# app/config.py
import os
import yaml

CONFIG_FILE = 'config.yaml'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config=yaml.load(f, Loader=yaml.FullLoader)
        return config
    return {}

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

