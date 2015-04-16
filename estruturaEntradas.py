# coding=utf-8
from registro import *

class EstruturaEntradas(object):
	"""Classe contendo a estrutura interna de um Registro de 128 bytes que contem
	entradas de dados. Mantem o vetor de enderecamento do Registro e contem 
	metodos para buscar, inserir, remover e modificar uma entrada de dados"""
	TAMINT = 4
	OFFSETDADOS = 2
	def __init__(self, registro):
		"""Sejam entradas de dados de tamanho 8. Logo em um Registro de 
		128 bytes podemos colocar 15 entradas de 8 bytes mais um vetor de 
		enderecamento de 2 bytes"""
		super(EstruturaEntradas, self).__init__()
		self.registro = registro
		self.enderecos = bytes2bits16(self.registro[0:2])
		
	def setRegistro(self,registro):
		self.registro = registro
		self.enderecos = bytearray(byte2bits16(self.registro[0:2]))

	def adicionarEntrada(self,entrada):
		indicelivre = self.enderecos.find(0)
		if (indicelivre != -1):
			posicaokey = self.OFFSETDADOS + indicelivre * 2 * self.TAMINT
			posicaovalue = posicaokey + self.TAMINT
			self.registro[posicaokey:posicaovalue] = int2bytes(entrada[0])
			self.registro[posicaovalue:posicaovalue+self.TAMINT] = int2bytes(entrada[1])
			self.enderecos[indicelivre] = 1
			self.atualizarEnderecos()
		else:
			raise Exception("Registro cheio!")

	def lerEntrada(self,indice):
		if self.enderecos[indice] == 0:
			raise Exception("Não há entrada")
		posicaokey = self.OFFSETDADOS + indice * 2 * self.TAMINT
		posicaovalue = posicaokey + self.TAMINT
		chave = bytes2int(self.registro[posicaokey:posicaovalue])
		rid = bytes2int(self.registro[posicaovalue:posicaovalue+self.TAMINT])
		return (chave,rid)

	def atualizarEnderecos(self):
		self.registro[0:2] = bits2bytes2(self.enderecos)


def bits2int(x):
	"""Consideramos o armazenamento little endian"""
	val = 0
	for i in range(0,len(x),1):
		val += (2**i)*x[i]
	return val

def bits2bytes2(x):
	y = bits2int(x)
	z = int2bytes(y)
	return z[0:2]

def int2bits16(x):
	retorno = bytearray(0 for i in range(0,16))
	quoc = x
	for i in range(0,16):
		retorno[i] = quoc % 2
		quoc = quoc // 2 
	return retorno

def bytes2bits16(x):
	z = x[0] + x[1]*256
	return int2bits16(z)