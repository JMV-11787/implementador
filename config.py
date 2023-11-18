
__version__ = "0.2.0"

import os

type ChaveValor = str, str | list[str]


def lê(caminho: str) -> dict[ChaveValor]:
	with open(caminho, "r") as arquivo:
		pares = {}

		nome_arquivo = os.path.basename(arquivo.name)
		índice_último_ponto = nome_arquivo.rfind(".")
		nome_arquivo = nome_arquivo[:índice_último_ponto]

		nome_diretório = os.path.dirname(arquivo.name)
		nome_diretório = os.path.basename(nome_diretório)
		pares["nome"] = nome_diretório

		for linha in arquivo:
			linha = linha.split('#')[0]
			linha = linha.strip()
			if not linha:
				continue

			chave, valor = linha.split("=")
			chave, valor = chave.strip(), valor.strip()
			pares[chave] = valor
	return pares


def converte_lista(valor: str, tira_vazios=True) -> list[str]:
	valores = valor.split(";")
	for i in range(len(valores)):
		valores[i] = valores[i].strip()
	if tira_vazios:
		while "" in valores:
			valores.remove("")
	return valores


def procura_em(diretório: str) -> str | None:
	arquivo = os.path.join(diretório, "config")
	if os.path.exists(arquivo):
		return arquivo


def lista_dirs(caminho_dir: str) -> list[str]:
	diretórios = []
	conteúdo_dir = os.listdir(caminho_dir)
	for nome_base_item in conteúdo_dir:
		caminho_completo_item = os.path.join(caminho_dir, nome_base_item)
		if os.path.isdir(caminho_completo_item):
			diretórios.append(caminho_completo_item)
	return diretórios


def procura_embaixo(diretório: str) -> list[str]:
	arquivos_config = []
	for subdiretório in lista_dirs(diretório):
		arquivo_config = procura_em(subdiretório)
		if arquivo_config:
			arquivos_config.append(arquivo_config)
	return arquivos_config
