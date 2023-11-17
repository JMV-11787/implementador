
__version__ = "0.1.1"

import os

import appdirs

import projeto

dir_config = appdirs.user_config_dir(appname="implementador")
os.makedirs(dir_config, exist_ok=True)

arquivo_config = os.path.join(dir_config, "config")

implementador = projeto.Projeto(projeto.supremo, arquivo_config)
implementador.roda()
