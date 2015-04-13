import os

class Arquivo(object):
	"""Classe associada a um arquivo em disco, contendo métodos para alocar um Registro e ler um Registro"""
	def __init__(self, nomearquivo):
		super(Arquivo, self).__init__()
		try:
			self.arquivo = open(nomearquivo, 'a+b')
		except Exception as e:
			raise e
	def alocarRegistro():
		archsize = os.path.getsize(nomearquivo)
		return archsize // 128
		
