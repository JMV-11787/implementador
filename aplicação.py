
__version__ = "0.0.0"

import subprocess
import shlex


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
