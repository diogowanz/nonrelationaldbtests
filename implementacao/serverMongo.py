from SOAPpy import SOAPServer
import psycopg2
import psycopg2.extras
import sys

import os

import commands

db = __import__(sys.argv[1])

Model = db.Model()

#from mongo import *
	
server = SOAPServer(('localhost',8081))

server.registerObject(Model)
#server.registerFunction(Model.insereOrgao)
#server.registerFunction(Model.listaOrgao)
#server.registerFunction(Model.insereEmpregado)
#server.registerFunction(Model.listaEmpregados)
#server.registerFunction(Model.listaDependentes)
#server.registerFunction(Model.insereDependente)
#server.registerFunction(Model.insereDocEmpregado)
#server.registerFunction(Model.insereDocDependente)




server.serve_forever()
