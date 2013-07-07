import socket
import time
import re
import urlparse
import sys
import os



def Busca(url, depth):

	BLOCO = 1024

	parse = urlparse.urlparse(url)
	host = parse.netloc
	path = parse.path
	
	if parse.port == None:
		port = 80
	else:
		port = parse.port
	
	addr = url
	
	if not (addr in lista):

		if depth != 0:
			lista.append(addr)

			print parse.scheme + "://" + host + path + ' ', depth
			# tries = 3

			# while tries > 0:
				# try:
			s = socket.create_connection((host, port), 5)
			s.send("GET /" + parse.path + " HTTP/1.1\r\nHost: "+ host + "\r\n\r\n")
			# time.sleep(1)
				# except socket.error:
					# erro = sys.exc_info()[:2]
					# if erro == socket.timeout:
						# print "Primeiro AQUI"
						# tries -= 1

			# if tries == 0:
				# print "Verify your connection!"

			time.sleep(1)
			strg = s.recv(BLOCO)

			# Diretorio correspondente ao host
			caminho = host
			pasta = host
			if not (caminho in diretorios):
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
				pasta = novalista[i]
				caminho = caminho + '/' + novalista[i]
				if not (caminho in diretorios):
					os.system("mkdir " + caminho + ' 2>> /dev/null')
					diretorios.append(caminho)
				i = i + 1

			if arq:
				nome = caminho + '/' + arq
			else:
				nome = caminho + '/SUBSTITUIR.html'
			saida = open(nome, 'w')

			#  Nem sempre a mensagem encerra com connection close
			#  A maneira correta eh pegar a primeira linha em branco
			#  como separador entre cabecalho e resto

			tam = len(strg)

			resposta = re.match(r'(.*)\n\r\n(.*)', strg, re.DOTALL)
			cabecalho = resposta.group(1)
			conteudo = resposta.group(2)

			# batata = re.search(r'Content-Length: (\d+)', cabecalho)

			# tam = int(batata.group(1))
			
			saida.write(conteudo)

			#while (len(conteudo) < tam):
			#	strg = s.recv(4096)
			#	conteudo = conteudo + strg
			#	saida.write(strg)

			while(tam == BLOCO):
				strg = s.recv(BLOCO)
				tam = (len(strg))
				conteudo = conteudo + strg
				saida.write(strg)


			saida.close()
					
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

					Busca(match, depth - 1)

lista = []
diretorios = []
Busca('http://minerva.ufpel.edu.br/~campani/', 3)
