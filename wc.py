import socket
import time
import re

def Busca(host,port,prof,dps):
	print host + '/' + dps + ' ', prof
	if prof != 0:
		s = socket.create_connection((host, port), 3)
		s.send("GET /"+dps+" HTTP/1.1\r\nHost: "+ host+"\r\n\r\n")
		time.sleep(1)
		strg = s.recv(4096*16)
		s.close()
		# print strg
		i = 0
		strg = re.sub(r'<!--[\w\W]*?-->',r'',strg)

		matchies = re.findall(r'<a [\w\W]*?href=\"([^\"]+)\"',strg)
		for match in matchies:
			# print match
			match = re.sub(r'https?://',r'',match)
			# print match
			# match2 = re.search(r'(^.*?)/?(.*$)',match)
			match2 = match.split('/',1)
			# print match2
			if match2[0] != '':
				host = match2[0]
			if len(match2) > 1:
				Busca(host,port,prof-1,match2[1])
			else:
				Busca(host,port,prof-1,'')
					


host = 'www.ufpel.edu.br'
port = 80
prof = 3

Busca(host,port,prof,'')