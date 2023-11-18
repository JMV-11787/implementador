
__version__ = "0.2.0-descontinuada"

import os

type ValorÚnico = str | bool
type Valor = ValorÚnico | list[ValorÚnico]
type ChaveValor = str, Valor


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
			linha = linha.split("#")[0]
			linha = linha.strip()
			if not linha:
				continue

			chave, valor = linha.split("=")
			chave, valor = chave.strip(), valor.strip()
			pares[chave] = tipifica(valor)
	return pares


def tipifica(valor: str) -> Valor:
	valores = valor.split(";")
	for item in valores:
		if item == "sim":
			item = True
		if item == "não":
			item = False

	if len(valores) == 1:
		return valores[0]
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
