from bucket import * 
from arquivo import * 

class Diretorio(object):
	"""Representa um diretório e o Hash Extensivo"""
	qtdPorRegistro = 128//4
	def __init__(self, arquivo, arquivoBucket):
		super(Diretorio, self).__init__()
		self.arquivos = (arquivo,arquivoBucket)
		if self.arquivos[0].lerRegistro(0) == 0:
			self.profundidadeGlobal = 2;
			self.arquivos[0].alocarRegistro()
			for i in range(0,4):
				self.adicionarBucket(2)
				# print(i,self.pegarProfundidade(i))
		else:
			self.profundidadeGlobal = self.procurarGlobal()

	def pegarProfundidade(self,indice):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		return self.arquivos[0].registro[1][indice*4]

	def pegarReferencia(self,indice):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		if self.pegarProfundidade(indice) != 0:
			return bytes2int(self.arquivos[0].registro[1][indice*4+1:(indice+1)*4]+b'\0')

	def procurarGlobal(self):
		i = 0
		maximo = 0
		while True:
			try:
				maximo = max(self.pegarProfundidade(i),maximo)
				i+=1
				# print (maximo)
			except Exception as e:
				break
		return maximo

	def adicionarReferencia(self,prof,ref):
		i=0
		while self.arquivos[0].lerRegistro(i) != 0:
			reg = self.arquivos[0].registro[1]
			for j in range(0,self.qtdPorRegistro):
				if reg[j*4]==0:
					reg[j*4] = prof
					reg[j*4+1:(j+1)*4] = int2bytes(ref)[0:3]
					return (i,j)

		self.arquivos[0].alocarRegistro()
		reg = self.arquivos[0].registro[1]
		reg[0] = prof
		reg[1:4] = int2bytes(ref)[0:3]
		return (i,0)

	def adicionarBucket(self,prof):
		indice = self.arquivos[1].alocarRegistro()
		self.arquivos[1].alocarRegistro()
		return self.adicionarReferencia(prof,indice)