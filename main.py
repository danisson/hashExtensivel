from diretorio import *

def main():
	sair = False
	arquivoBucket = Arquivo("bucket.dat")
	arquivoDiretorio = Arquivo("diretorio.dat")

	try:
		diretorio = Diretorio(arquivoDiretorio,arquivoBucket)
	except Exception as e:
		raise e

	try:
		arquivoRID = open("ridsalvo.txt")
		ultimoRID = int(arquivoRID.read())
		arquivoRID.close()
	except Exception as e:
		print("Não é possível abrir/não existe um arquivo com o último RID salvo. Usando 0 para o valor...")
		ultimoRID = 0

	while not sair:
		option = input("Bem vindo ao nosso banco de dados! Por favor, selecione a opção desejada: (I)nserir uma chave, (B)uscar uma chave, (R)emover uma chave, (S)air: ")
		if (option=="I"):
			chave = input("Insira uma chave: ")
			diretorio.inserirEntrada((int(chave),ultimoRID))
			ultimoRID = ultimoRID+1
			print("Entrada adicionada com sucesso!")
		elif (option=="B"):
			chave = input("Insira uma chave: ")
			resultado = diretorio.buscarEntrada(int(chave))
			print("O RID buscado é:" + str(resultado))
		elif (option=="R"):
			chave = input("Insira uma chave: ")
			diretorio.removerEntrada(int(chave))
			print("Entradas removidas com sucesso!")
		elif (option=="S"):
			sair=True
		else:
			print("Opção incorreta! :(")
		arquivoBucket.salvarRegistro()
		arquivoDiretorio.salvarRegistro()

	try:
		arquivoRID = open("ridsalvo.txt","w")
		arquivoRID.write(ultimoRID)
		arquivoRID.close()
	except Exception as e:
		print("Não foi possível salvar o último RID!")
	
if __name__ == '__main__':
	main()