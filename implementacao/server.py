from SOAPpy import SOAPServer
import psycopg2
import psycopg2.extras

import os

import commands

from postgres_dict import *

def hello():
	return 'hello world'
	
def tchau():
	print 'Adeus'
	
server = SOAPServer(('localhost',8081))

server.registerFunction(hello)
server.registerFunction(listaEmpregados)

servidores = listaEmpregados(id_empregado = 7)

for servidor in servidores:
	print servidor['no_empregado']

server.serve_forever()
