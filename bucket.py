from estruturaEntradas import *

class Bucket(object):
	"""Um bucket do hash"""
	def __init__(self, arquivo, reg1, reg2):
		super(Bucket, self).__init__()
		self.arquivo = arquivo
		self.registros = [reg1,reg2]

	def buscarRID(self,chave):
		entrada = None
		for registro in self.registros:
			self.arquivo.lerRegistro(registro)
			entrada = EstruturaEntradas(self.arquivo.registro[1])
			par = entrada.buscarEntrada(chave)
			if par: return par
		return None

	def adicionarPar(self,par):
		numExceptions = len(self.registros)
		for registro in self.registros:
			try:
				self.arquivo.lerRegistro(registro)
				entrada = EstruturaEntradas(self.arquivo.registro[1])
				entrada.adicionarEntrada(par)
			except Exception as e:
				numExceptions = numExceptions - 1
				if (numExceptions == 0):
					raise e
			else:
				break