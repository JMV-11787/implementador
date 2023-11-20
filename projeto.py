from __future__ import annotations

__version__ = "0.3.1"

import os
import shlex
import subprocess
from typing import Callable

import config


class Projeto:
	def __init__(inst, superprojeto: Projeto, caminho_arquivo: str, roda=False):
		inst.repositório: str = superprojeto.repositório
		inst.instruções: list[str] = superprojeto.instruções
		inst.aplica: bool = superprojeto.aplica

		pares = config.lê(caminho_arquivo)
		inst.nome = pares.get("nome", None)
		inst.repositório = pares.get("repositório", inst.repositório)

		instruções = pares.get("instruções")
		if instruções:
			instruções = config.converte_lista(instruções)
			inst.instruções = instruções
		inst.aplica = pares.get("aplica", inst.aplica)

		caminho_diretório = os.path.dirname(caminho_arquivo)
		inst.subprojetos: list[Projeto] = [
			Projeto(inst, caminho) for caminho in config.procura_embaixo(caminho_diretório)
		]

		inst.aplicação: inst.Aplicação | None = None
		if inst.repositório and inst.aplica:
			inst.aplicação = inst.Aplicação(inst.instruções, começa=roda)

		inst.tarefas: list[Callable] = []
		inst.próxima_tarefa: int = 0
		inst.atarefa()

	def roda(inst):
		while True:
			inst.continua()

	def continua(inst):
		if len(inst.tarefas) - 1 > inst.próxima_tarefa:
			inst.atarefa()
			inst.próxima_tarefa: int = 0
			if len(inst.tarefas) >= 1:
				inst.tarefas[inst.próxima_tarefa]()
				inst.próxima_tarefa += 1

	def atarefa(inst):
		inst.tarefas: list[Callable] = []

		if inst.aplicação:
			inst.tarefas.append(inst.aplicação.continua)

		for subprojeto in inst.subprojetos:
			inst.tarefas.append(subprojeto.continua)

	class Aplicação:
		def __init__(inst, etapas: list[str], começa=True):
			inst.etapas: list[inst.Etapa] = []
			inst.índice_etapa_atual: int = 0
			for etapa in etapas:
				inst.etapas.append(inst.Etapa(etapa))
			if começa:
				inst.continua()

		def acabou(inst):
			if inst.etapas[-1].já_terminou():
				return True
			return False

		def etapa_atual(inst):
			return inst.etapas[inst.índice_etapa_atual]

		def continua(inst):
			if inst.acabou():
				return
			if inst.etapa_atual().já_terminou():
				inst.índice_etapa_atual += 1
			elif inst.etapa_atual().está_rodando():
				return
			inst.etapa_atual().roda()

		class Etapa:
			def __init__(inst, comando: str, roda=False):
				inst.subprocesso: subprocess.Popen | None = None
				inst.comando: list[str] = shlex.split(comando)
				if roda:
					inst.roda()

			def já_começou(inst):
				if inst.subprocesso:
					return True
				return False

			def está_rodando(inst):
				if inst.subprocesso:
					if inst.subprocesso.poll() is None:
						return True
				return False

			def já_terminou(inst):
				if inst.subprocesso:
					if inst.subprocesso.poll() is not None:
						return True
				return False

			def roda(inst):
				if not inst.já_começou():
					inst.subprocesso = subprocess.Popen(inst.comando)
				else:
					raise Exception("A aplicação já está rodando ou já rodou")

			def fecha(inst):
				if inst.já_começou():
					inst.subprocesso.terminate()
				else:
					raise Exception("A aplicação não está rodando")

			def recomeça(inst):
				inst.fecha()
				inst.subprocesso = None
				inst.roda()


supremo = object.__new__(Projeto)
supremo.nome = "supremo"
supremo.repositório = None
supremo.instruções = None
supremo.aplica = False
