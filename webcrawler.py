import socket
import time
import re
import urlparse
import sys
import os


# FLAGS PARA DEBUG

# SEM ESCRITA
# Quando ela eh True, nenhum arquivo ou diretorio eh criado.
DEBUG_FLAG = True

# IMPRIME CABECALHO
# Quando ela eh True, o cabecalho obtido como resposta eh mostrado abaixo do
# endereco do site
IMPRIME_CABECALHO = False



def GeraLink(scheme, host, path, s):
	ret = s
	if (re.match(r'mailto:|javascript:', s)):
		ret = ""
	else:
		if re.match(r'/', s):
			ret = scheme + "://" + host + s
		elif not(re.match(r'https?://', s)):
			ret = scheme + "://" + path + '/' + s
	return ret


def CriaDiretorios(host, path):
	# Diretorio correspondente ao host
	caminho = host
	if not (caminho in diretorios):
		if not DEBUG_FLAG:		# DEBUG
			os.system("mkdir " + caminho + ' 2>> /dev/null')
		diretorios.append(caminho)

	# Diretorios correspondentes ao path
	novalista = re.split(r'/', path)
	novalista.pop()			# o ultimo elemento eh um nome de arquivo e nao de pasta
	if novalista:
		novalista.pop(0)	# o primeiro elemento eh uma string nula
	npastas = len(novalista)
	i = 0
	while i < npastas:
		caminho = caminho + '/' + novalista[i]
		if not (caminho in diretorios):
			if not DEBUG_FLAG:		# DEBUG
				os.system("mkdir " + caminho + ' 2>> /dev/null')
			diretorios.append(caminho)
		i = i + 1

	return caminho



def Busca(url, depth):

	BLOCO = 2048

	houve_erro = False

	parse = urlparse.urlparse(url)
	host = parse.netloc
	path = parse.path
	
	if parse.port == None:
		port = 80
	else:
		port = parse.port
	
	addr = host + path

	if not (addr in lista_visitados):

		lista_visitados.append(addr)

		scheme = parse.scheme
		print scheme + '://' + host + path + ' '

		# Inicia a comunicacao, envia a requisicao e recebe o cabecalho
		# mais o inicio do conteudo, se houver
		try:
			s = socket.create_connection((host, port), 5)
			s.send("GET /" + parse.path + " HTTP/1.1\r\nHost: "+ host + "\r\n\r\n")
			strg = s.recv(BLOCO)
		
		except socket.error:
			if DEBUG_FLAG:		# DEBUG
				erro = sys.exc_info()[:2]
				print erro
			else:
				print '\t<erro no socket>\n'
			houve_erro = True

		if not houve_erro:

			bytes_recebidos = len(strg)

			# Separa o cabecalho do inicio do conteudo
			resposta = re.match(r'(.*)\n\r\n(.*)', strg, re.DOTALL)
			cabecalho = resposta.group(1)
			conteudo = resposta.group(2)

			if IMPRIME_CABECALHO:
				print '\n' + cabecalho + '\n\n'
			
			# Define se a requisicao foi bem sucedida
			codigo_retorno = int(cabecalho.split(" ", 2)[1])

			# Verifica se o cabecalho disponibiliza o tamanho do
			# conteudo
			batata = re.search(r'Content-Length: (\d+)', cabecalho)
			if batata:
				tamanho_disponivel = True
				tam = int(batata.group(1))
			else:
				tamanho_disponivel = False
			
			
			if codigo_retorno == 200 or codigo_retorno == 300:
			# Site encontrado

				# Assegura que os diretorios necessarios
				# existem
				caminho = CriaDiretorios(host,path)
				
				# Monta o caminho do arquivo de saida
				re_arquivo = re.search(r'/([^/]+)$', path)
				if re_arquivo:
					arq = re_arquivo.group(1)
				else:
					arq = 'PRINCIPAL'
				
				nome = caminho + '/' + arq

				
				if not DEBUG_FLAG:		# DEBUG
					saida = open(nome, 'w')
				
				if not DEBUG_FLAG:		# DEBUG
					saida.write(conteudo)

				# Recebe o restante do conteudo
				# Se houver indicacao explicita de content-length,
				# ela deve ser respeitada. Senao, paramos quando o
				# server para de mandar.
				if tamanho_disponivel:
					bytes_recebidos = len(conteudo)
					while (bytes_recebidos < tam):
						strg = s.recv(BLOCO)
						ultimo_br = bytes_recebidos
						bytes_recebidos += len(strg)
						conteudo = conteudo + strg
						if not DEBUG_FLAG:		# DEBUG
							saida.write(strg)
						if bytes_recebidos == ultimo_br:
							break
				else:
					while(bytes_recebidos == BLOCO):
						strg = s.recv(BLOCO)
						bytes_recebidos = (len(strg))
						conteudo = conteudo + strg
						if not DEBUG_FLAG:		# DEBUG
							saida.write(strg)


				if not DEBUG_FLAG:		# DEBUG
					saida.close()

				# Procura todos os links dentro de tags
				# <a href> na pagina recebida
				strg = conteudo
				strg = re.sub(r'<!--[\w\W]*?-->',r'',strg)
				matchies = re.findall(r'<a [\w\W]*?href=\"([^\"]+)\"',strg)
				for match in matchies:
					link = GeraLink(parse.scheme, host, caminho, match)
					if link:
						lista_por_visitar.append(link)
				
				print "\t<recebido>\n"
			
			elif codigo_retorno == 301 or codigo_retorno == 302 or codigo_retorno == 307:
			# Fui redirecionado!
				
				re_novo_endereco = re.search(r'Location: (.+)\r', cabecalho)
				if re_novo_endereco:
					novo_endereco = re_novo_endereco.group(1)
					lista_por_visitar.append(novo_endereco)
					msg = '\t<redirecionado para ' + str(novo_endereco) + '>\n'
					print msg
				else:
					print '\t<redirecionado sem endereco destino>\n'
			
			else:
				print '\t<resposta com codigo invalido>\n'
						
			s.close()


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
