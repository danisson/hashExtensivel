from array import array

class Registro(object):
	"""Registro 128 bytes"""
	def __init__(self,vetorbytes=None):
		super(Registro, self).__init__()
		if vetorbytes is None:
			self.vetor = bytearray(0 for _ in range(128))
		else:
			self.vetor = vetorbytes
		self.dirty = False
	def __getitem__(self, key):
		if isinstance(key,slice):
			return self.vetor[key]
		elif isinstance(key, int):
			if key > 127 or key < 0: raise Exception('Chave fora do vetor')
			return self.vetor[key]
		else:
			raise TypeError("Argumento invalido")
	def __setitem__(self, key, value):
		if isinstance(key,slice):
			self.vetor[key] = value
			self.dirty = True
		elif isinstance(key, int):
			if key > 127 or key < 0: raise Exception('Chave fora do vetor')
			self.vetor[key] = value
			self.dirty = True
		else:
			raise TypeError("Argumento invalido")
	def __str__(self):
		string = "["
		for i in range(0,128,4):
			string += str(bytes2int(self[i:i+4]))
			if i<124: string+=", "
		string+="]"
		return string

def int2bytes(x):
	"""Consideramos o armazenamento little endian"""
	if x<0 or x>(2**32-1): raise TypeError("Argumento invalido")
	vetor = bytearray([0,0,0,0])
	vetor[0] = x%256;
	vetor[1] = (x//256)%256;
	vetor[2] = (x//65536)%256;
	vetor[3] = (x//16777216)%256;
	return vetor

def bytes2int(x):
	"""Consideramos o armazenamento como little endian"""
	return x[0] + 256*x[1] + 65536*x[2] + 16777216*x[3]
