import os
from registro import *

class Arquivo(object):
	"""Classe associada a um arquivo em disco, contendo métodos para alocar um Registro e ler um Registro"""
	def __init__(self, nomearquivo):
		super(Arquivo, self).__init__()
		try:
			self.arquivo = open(nomearquivo, 'r+b')
		except IOError as e:
			print("Arquivo não encontrado!")

	def alocarRegistro(self):
		tamanhoarq = os.path.getsize(self.arquivo.name)
		novoreg = Registro()
		self.arquivo.write(novoreg.vetor)
		self.arquivo.flush()
		return (tamanhoarq // 128)

	def lerRegistro(self,offset):
		self.arquivo.seek(offset)
		result_leitura = bytearray(self.arquivo.read(128))
		return Registro(result_leitura)		
