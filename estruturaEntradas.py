# coding=utf-8
from registro import *

class EstruturaEntradas(object):
	"""Classe contendo a estrutura interna de um Registro de 128 bytes que contem entradas de dados. Mantem o vetor de enderecamento do Registro e contem metodos para buscar, inserir, remover e modificar uma entrada de dados"""
	def __init__(self, registro):
		"""Sejam entradas de dados de tamanho 8. Logo em um Registro de 128 bytes podemos colocar 15 entradas de 8 bytes mais um vetor de enderecamento de 2 bytes"""
		super(EstruturaEntradas, self).__init__()
		self.registro = registro
		self.TAMINT = 4
		self.OFFSETDADOS = 2
		self.enderecos = bytearray(0 for _ in xrange(16))
		self.atualizarEnderecos()
		
	def setRegistro(self,registro):
		self.registro = registro
		self.enderecos = bytearray(byte2bits16(self.registro[0:2])

	def colocarEntrada(self,entrada):
		indicelivre = self.enderecos.find(0)
		if (indicelivre > 0):
			posicaokey = self.OFFSETDADOS + indicelivre
			posicaovalue = self.OFFSETDADOS + self.TAMINT
			self.registro[posicaokey:posicaovalue] = int2bytes(entrada.chave)
			self.registro[posicaovalue:posicaovalue+self.TAMINT] = int2bytes(entrada.rid)
			self.enderecos[indicelivre] = 1
			self.atualizarEnderecos()
		else:
			raise Exception("Registro cheio!")

	def atualizarEnderecos():
		self.registro[0:2] = bits2bytes2(self.enderecos)


def bits2int(x):
	"""Consideramos o armazenamento little endian"""
	for i in range(0,len(x),1):
		val = val + x[i]**2
	return val

def bits2bytes2(x):
	y = bits2int(x)
	z = int2bytes(y)
	return z[0:2]

def int2bits16(x):
	quoc = x
	for i in xrange(0,16):
		retorno[i] = quoc % 2
		quoc = quoc // 2 

def bytes2bits16(x):
	z = x[0] + x[1]*256
	return int2bits16(z)