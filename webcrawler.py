import socket
import time
import re
import urlparse
import sys

import os

def Busca(url, depth):
	parse = urlparse.urlparse(url)

	# print parse

	host = parse.netloc

	path = parse.path

	if parse.port == None:
		port = 80
	else:
		port = parse.port

	# if path == '':
	# 	path = '/'

	addr = url

	if not (addr in lista):
		lista.append(addr)

		# print lista

		if depth != 0:
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

			# print tries
			# print "LOL"

			# strg = ""

			# try:
			time.sleep(1)
			strg = s.recv(1024)


			caminho = host
			pasta = host
			novalista = re.split(r'/', path)
			print novalista
			i = 0
			npastas = len(novalista)

			while i < (npastas):
				# print "CAMINHO " + caminho
				# print "PASTA " + pasta
				if not (caminho in diretorios):
					
					os.system("mkdir " + caminho)
					diretorios.append(caminho)


				if i > 0 :
					caminho = caminho + '/' + novalista[i]

				i += 1



			# 	if npastas > 1:
			# 		caminho = caminho + '/' + novalista[i]
			# 	i = i + 1



			# # host = ufpel.edu.br
			# # path = ifm/index.html
			# # pasta = ufpel.edu.br/ifm

			if novalista[-1]:
				nome = caminho + "/" + novalista[-1]
			else:
				nome = caminho + '/' + 'batata'
			print nome
			saida = open(nome, 'w')



			resposta = re.split(r'Connection: close', strg)
			cabecalho = resposta[0]
			conteudo = resposta[1]

			batata = re.search(r'Content-Length: (\d+)', strg)
			tam = int(batata.group(1))
			saida.write(conteudo)
			while (len(conteudo) < tam):
				strg = s.recv(1024)
				conteudo = conteudo + strg
				saida.write(strg)
				# print strg,

			saida.close()

			# print(strg)
			# batata = re.search(r'Content-Length: (\d+)', strg)
			# tam = batata.group(1)
			# print (len(strg))
			# print (tam)

			# arquivo = open("php.html","w")
			# arquivo.write(strg)

			# except socket.error:
			# 	erro = sys.exc_info()[:2]
			# 	if erro == socket.timeout:
			# 		print "AQUI"
					
			s.close()
			# print strg
			# i = 0

			strg = conteudo

			strg = re.sub(r'<!--[\w\W]*?-->',r'',strg)

			matchies = re.findall(r'<a [\w\W]*?href=\"([^\"]+)\"',strg)
			for match in matchies:
				# print match

				if not (re.match(r'mailto:', match)):
					if re.match(r'/', match):
						match = parse.scheme + "://" + host + match
					elif not(re.match(r'https?://', match)):
						match = parse.scheme + "://" + host + '/' + match


					Busca(match, depth - 1)

				# match = re.sub(r'https?://',r'',match)
				# print match
				# match2 = re.search(r'(^.*?)/?(.*$)',match)
				# match2 = match.split('/',1)
				# print match2
				# if match2[0] != '':
				# 	host = match2[0]
				# if len(match2) > 1:
				# 	Busca(host,port,prof-1,match2[1])
				# else:
				# 	Busca(host,port,prof-1,'')

lista = []
diretorios = []
Busca('http://www.pudim.com.br', 3)