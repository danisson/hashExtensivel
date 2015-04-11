from array import array

class Registro(object):
	"""Registro 128 bytes"""
	def __init__(self):
		super(Registro, self).__init__()
		self.vetor = array('B',(0 for _ in xrange(128)))
		self.dirty = False
	def __getitem__(self, key):
		if key > 128 or key < 0: raise Exception('Chave fora do vetor')
		return self.vetor[key]
	def __setitem__(self, key, value):
		if key > 128 or key < 0: raise Exception('Chave fora do vetor')
		self.vetor[key] = value
		self.dirty = True
	def __str__(self):
		string = "["
		for x in self.vetor:
			string += format(x,'02x')+", "
		string+="]"
		return string