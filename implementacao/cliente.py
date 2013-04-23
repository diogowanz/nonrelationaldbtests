from SOAPpy import SOAPProxy

url = 'http://localhost:8081'
#namespace = 'ns-hello'

server = SOAPProxy(url)
#server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1

servidores = server.listaEmpregados()

print servidores

#for servidor in servidores:
#	print servidores['no_empregado']

print server.hello()
