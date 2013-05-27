from SOAPpy import SOAPServer
import psycopg2
import psycopg2.extras

import os

import commands

from mongo import *

def hello():
	return 'hello world'
	
def tchau():
	print 'Adeus'
	
server = SOAPServer(('localhost',8081))

server.registerFunction(hello)
server.registerFunction(insereOrgao)
server.registerFunction(listaOrgao)
server.registerFunction(insereEmpregado)
server.registerFunction(listaEmpregados)
server.registerFunction(listaDependentes)
server.registerFunction(insereDependente)
server.registerFunction(insereDocEmpregado)
server.registerFunction(insereDocDependente)




server.serve_forever()
