import os
from registro import *

class Arquivo(object):
	"""Classe associada a um arquivo em disco, contendo métodos para alocar um Registro e ler um Registro"""
	def __init__(self, nomearquivo):
		super(Arquivo, self).__init__()
		try:
			self.registro = (None,None)
			self.arquivo = open(nomearquivo, 'r+b')
		except IOError as e:
			print("Arquivo não encontrado!")

	def alocarRegistro(self):
		tamanhoarq = os.path.getsize(self.arquivo.name)
		self.salvarRegistro()
		novoreg = Registro()
		self.arquivo.seek(tamanhoarq)
		self.arquivo.write(novoreg.vetor)
		self.arquivo.flush()
		self.registro = (tamanhoarq,novoreg)
		return tamanhoarq//128

	def salvarRegistro(self):
		if self.registro[1] is not None and self.registro[1].dirty:
			self.arquivo.seek(self.registro[0])
			self.arquivo.write(self.registro[1].vetor)
			self.arquivo.flush()

	def lerRegistro(self,offset):
		self.salvarRegistro()
		self.arquivo.seek(offset*128)
		result_leitura = bytearray(self.arquivo.read(128))
		self.registro = (offset*128,Registro(result_leitura))
		return len(result_leitura)

	def __str__(self):
		return "<Arquivo "+self.arquivo.name+">"