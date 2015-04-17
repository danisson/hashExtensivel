from bucket import * 
from arquivo import * 

class Diretorio(object):
	"""Representa um diretório e o Hash Extensivo"""
	qtdPorRegistro = 128//4
	tamEntrada = 4
	def __init__(self, arquivo, arquivoBucket):
		super(Diretorio, self).__init__()
		self.arquivos = (arquivo,arquivoBucket)
		if self.arquivos[0].lerRegistro(0) == 0:
			self.profundidadeGlobal = 2;
			self.arquivos[0].alocarRegistro()
			for i in range(0,4):
				self.adicionarBucket(2)
				print(i,self.pegarProfundidade(i))
		else:
			self.profundidadeGlobal = self.procurarGlobal()

	def pegarProfundidade(self,indice):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		return self.arquivos[0].registro[1][indice*4]

	def editarProfundidade(self,indice,nprof):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		self.arquivos[0].registro[1][indice*4] = nprof

	def pegarReferencia(self,indice):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		if self.pegarProfundidade(indice) != 0:
			return bytes2int(self.arquivos[0].registro[1][indice*4+1:(indice+1)*4]+b'\0')

	def editarReferencia(self,indice,nref):
		numeroRegistro = indice // self.qtdPorRegistro
		indice = indice % self.qtdPorRegistro
		if self.arquivos[0].lerRegistro(numeroRegistro) == 0:
			raise Exception("Indice invalido")
		if self.pegarProfundidade(indice) != 0:
			self.arquivos[0].registro[1][indice*4+1:(indice+1)*4] = int2bytes(nref)[0:3]

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

	def duplicarBuckets(self,indice):
		localDepth = self.pegarProfundidade(indice)
		if localDepth == self.profundidadeGlobal:
			for i in range(0,2**self.profundidadeGlobal):
				self.adicionarReferencia(self.pegarProfundidade(i),self.pegarReferencia(i))
			indiceIrmao = indice+2**self.profundidadeGlobal
			self.editarProfundidade(indice,localDepth+1)
			self.editarProfundidade(indiceIrmao,localDepth+1)

			bucketIndice = self.arquivos[1].alocarRegistro()
			self.arquivos[1].alocarRegistro()
			self.editarReferencia(indiceIrmao,bucketIndice)

			regs = [self.pegarReferencia(indice),self.pegarReferencia(indiceIrmao)]
			bucket1 = Bucket(self.arquivos[1],regs[0],regs[0]+1)
			bucket2 = Bucket(self.arquivos[1],regs[1],regs[1]+1)
			for registro in bucket1.registros:
				self.arquivos[1].lerRegistro(registro)
				entrada = EstruturaEntradas(self.arquivos[1].registro[1])
				for i in range(0,15):
					x = entrada.lerEntrada(i)
					if x:
						print (i,x,bin(x[0]%(2**(self.profundidadeGlobal+1))))
					if x and (x[0]%(2**(self.profundidadeGlobal+1))==indiceIrmao):
						bucket2.adicionarPar(x)
						bucket1.removerPar(x[0])

			self.profundidadeGlobal+=1
		else:
			indiceIrmao = indice+2**localDepth
			self.editarProfundidade(indice,localDepth+1)
			self.editarProfundidade(indiceIrmao,localDepth+1)

			bucketIndice = self.arquivos[1].alocarRegistro()
			self.arquivos[1].alocarRegistro()
			self.editarReferencia(indiceIrmao,bucketIndice)

			regs = [self.pegarReferencia(indice),self.pegarReferencia(indiceIrmao)]
			bucket1 = Bucket(self.arquivos[1],regs[0],regs[0]+1)
			bucket2 = Bucket(self.arquivos[1],regs[1],regs[1]+1)
			for registro in bucket1.registros:
				self.arquivos[1].lerRegistro(registro)
				entrada = EstruturaEntradas(self.arquivos[1].registro[1])
				for i in range(0,15):
					x = entrada.lerEntrada(i)
					if x:
						print (i,x,bin(x[0]%(2**(self.profundidadeGlobal+1))))
					if x and (x[0]%(2**self.profundidadeGlobal)==indiceIrmao):
						bucket2.adicionarPar(x)
						bucket1.removerPar(x[0])

	def buscarEntrada(self,chave):
		hashChave = chave % (2**self.profundidadeGlobal)
		offsetReg = self.pegarReferencia(hashChave)
		bucket = Bucket(self.arquivos[1],offsetReg,offsetReg+1)
		return bucket.buscarRID(chave)

	def inserirEntrada(self,entrada):
		hashChave = entrada[0] % (2**self.profundidadeGlobal)
		offsetReg = self.pegarReferencia(hashChave)
		bucket = Bucket(self.arquivos[1],offsetReg,offsetReg+1)
		print("O hash é "+str(hashChave)+" o bucket vai de: "+str([offsetReg,offsetReg+1]))
		try:
			bucket.adicionarPar(entrada)
		except Exception as e:
			self.duplicarBuckets(hashChave)
			print("Precisa dividir o bucket!")

	def removerEntrada(self,chave):
		hashChave = chave % (2**self.profundidadeGlobal)
		offsetReg = self.pegarReferencia(hashChave)
		bucket = Bucket(self.arquivos[1],offsetReg,offsetReg+1)
		bucket.removerPar(chave)