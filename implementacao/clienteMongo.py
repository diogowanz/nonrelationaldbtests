from SOAPpy import SOAPProxy


def main():
	url = 'http://localhost:8081'
	#namespace = 'ns-hello'

	server = SOAPProxy(url)
	#server.config.dumpSOAPOut = 1
	#server.config.dumpSOAPIn = 1

	#print server.insereOrgao('Ministerio do Planejamento', 'Esplanada dos Ministerios N 1', 'Brasilia','DF')
	
#	orgaos = server.listaOrgao(nome='Ministerio do Planejamento')
#	for orgao in orgaos:
#		print orgao['id']
		
#	if len(orgaos) == 1:
#		print orgaos[0]['id']
#		server.insereEmpregado('Debora Natsue', '01/01/2010',None,'06/10/1989','M000005','9876765','222222222-22',orgaos[0]['id'],None,None)

#	empregados = server.listaEmpregados(nome='Debora')
#	for empregado in empregados:
#		print empregado['nome']

	dependentes = server.listaDependentes(nomeDependente='Diogo')
	for dependente in dependentes:
		print dependente['nome']






if __name__=="__main__":
	main()
