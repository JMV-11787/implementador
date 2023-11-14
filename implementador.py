
__version__ = "0.0.0"

import configparser
import os

import appdirs

dir_config = appdirs.user_config_dir(appname="implementador")
os.makedirs(dir_config, exist_ok=True)

arquivo_config = os.path.join(dir_config, "config.ini")


config = configparser.ConfigParser()
config.read(arquivo_config)
