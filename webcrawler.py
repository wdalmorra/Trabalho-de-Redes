import socket
import time
import re
import urlparse
import sys
import os


# FLAG PARA DEBUG
# Quando ela eh True, nenhum arquivo ou diretorio eh criado.
NO_WRITE_FLAG = True


def CriaDiretorios(host, path):
	# Diretorio correspondente ao host
	caminho = host
	if not (caminho in diretorios):
		if not NO_WRITE_FLAG:		# DEBUG
			os.system("mkdir " + caminho + ' 2>> /dev/null')
		diretorios.append(caminho)

	# Diretorios correspondentes ao path
	novalista = re.split(r'/', path)
	arq = novalista.pop()		# o ultimo elemento eh um nome de arquivo e nao de pasta
	if novalista:
		novalista.pop(0)	# o primeiro elemento eh uma string nula
	npastas = len(novalista)
	i = 0
	while i < npastas:
		caminho = caminho + '/' + novalista[i]
		if not (caminho in diretorios):
			if not NO_WRITE_FLAG:		# DEBUG
				os.system("mkdir " + caminho + ' 2>> /dev/null')
			diretorios.append(caminho)
		i = i + 1

	# if arq:
	# 	nome = caminho + '/' + arq
	# else:
	# 	nome = caminho + '/SUBSTITUIR.html'

	return (caminho, arq)



def Busca(url, depth):

	BLOCO = 8192

	parse = urlparse.urlparse(url)
	host = parse.netloc
	path = parse.path
	
	if parse.port == None:
		port = 80
	else:
		port = parse.port
	
	addr = url
	
	if not (addr in lista_visitados):

		lista_visitados.append(addr)

		scheme = parse.scheme
		print scheme + "://" + host + path
		# tries = 3
		# while tries > 0:
		try:
			s = socket.create_connection((host, port), 5)
			s.send("GET /" + parse.path + " HTTP/1.1\r\nHost: "+ host + "\r\n\r\n")
			strg = s.recv(BLOCO)
		# time.sleep(1)
		except socket.error:
			erro = sys.exc_info()[:2]
			print erro
				# if erro == socket.timeout:
					# print "Primeiro AQUI"
					# tries -= 1

		ret = CriaDiretorios(host,path)

		caminho = ret[0]
		print "Caminho: " + caminho
		arq = ret[1]
		print "Arq: " + arq
		
		if arq:
			nome = caminho + '/' + arq
		else:
			nome = caminho + '/SUBSTITUIR.html'

		#  Nem sempre a mensagem encerra com connection close
		#  A maneira correta eh pegar a primeira linha em branco
		#  como separador entre cabecalho e resto

		bytes_recebidos = len(strg)

		resposta = re.match(r'(.*)\n\r\n(.*)', strg, re.DOTALL)
		cabecalho = resposta.group(1)
		conteudo = resposta.group(2)
		
		# CORRIGIR: pode retornar index out of range para um cabecalho
		# nulo ou com uma unica linha.
		codigo_retorno = int(cabecalho.split(" ", 2)[1])

		batata = re.search(r'Content-Length: (\d+)', cabecalho)
		if batata:
			tamanho_disponivel = True
			tam = int(batata.group(1))
			print 'Tamanho disponivel ' + str(tam)
		else:
			tamanho_disponivel = False
		
		
		if codigo_retorno == 200 or codigo_retorno == 300:	# Achei o site de prima!
			
			if not NO_WRITE_FLAG:		# DEBUG
				saida = open(nome, 'w')
			
			if not NO_WRITE_FLAG:		# DEBUG
				saida.write(conteudo)

			# Se houver indicacao explicita de content-length,
			# ela deve ser respeitada. Senao, paramos quando o
			# server para de mandar.
			if tamanho_disponivel:
				bytes_recebidos = len(conteudo)
				while (bytes_recebidos < tam):
					strg = s.recv(BLOCO)
					ultimo_br = bytes_recebidos
					bytes_recebidos += len(strg)
					print 'Bytes recebidos ' + str(bytes_recebidos)
					conteudo = conteudo + strg
					if not NO_WRITE_FLAG:		# DEBUG
						saida.write(strg)
					if bytes_recebidos == ultimo_br:
						break
			else:
				while(bytes_recebidos == BLOCO):
					strg = s.recv(BLOCO)
					bytes_recebidos = (len(strg))
					conteudo = conteudo + strg
					if not NO_WRITE_FLAG:		# DEBUG
						saida.write(strg)

			# print len(conteudo)

			if not NO_WRITE_FLAG:		# DEBUG
				saida.close()
		
		elif codigo_retorno == 301 or codigo_retorno == 302 or codigo_retorno == 307:
		# Fui redirecionado!
			
			cebola = re.search(r'Location: (.+)', cabecalho)
			if cebola:
				lista_por_visitar.append(cebola.group(1))
					
		s.close()

		strg = conteudo

		strg = re.sub(r'<!--[\w\W]*?-->',r'',strg)

		matchies = re.findall(r'<a [\w\W]*?href=\"([^\"]+)\"',strg)
		for match in matchies:
			# print caminho
			if not (re.match(r'mailto:', match)):
				if re.match(r'/', match):
					match = parse.scheme + "://" + host + match
				elif not(re.match(r'https?://', match)):
					match = parse.scheme + "://" + caminho + '/' + match


				lista_por_visitar.append(match)


lista_visitados = []
diretorios = []
lista_por_visitar = ['http://minerva.ufpel.edu.br/~campani/']

ii = 0
jj = 0
while ii < 4:								# Profundidade
	tam = len(lista_por_visitar)
	ii += 1
	jj = 0
	# for host in lista_por_visitar:
	while(jj < tam):						# Lista de sites numa determinada profundidade
			host = lista_por_visitar.pop(0)
			Busca(host,1)
			jj += 1
