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

#	dependentes = server.listaDependentes(nomeDependente='Diogo')
#	for dependente in dependentes:
#		print dependente['nome']

#	empregados = server.listaEmpregados (nome='Debora')
#	print server.insereDependente('Tassia','1234234','222.222.222-22',None,'29/09/1992','Filho',None,empregados[0]['id'])

#	file=open('/home/wanzeller/python/teste.txt', 'rb')
#	data=file.read()
#	print server.insereDocEmpregado('M000005','Comprovante de Residencia','comprv_residencia.txt',data.encode('base64'))
#	file.close()

	file=open('/home/wanzeller/python/bkp_lista_orgaos.txt', 'rb')
	data=file.read()
	print server.insereDocDependente('M808130','2649051','34347984793',None,'5216ae1f6e955269534b077f','certidao_nascimento.txt',data.encode('base64'))
	file.close()






if __name__=="__main__":
	main()
