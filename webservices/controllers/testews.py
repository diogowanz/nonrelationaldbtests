def test_soap_sub():
	from gluon.contrib.pysimplesoap.client import SoapClient, SoapFault
	 #create a SOAP client
	client = SoapClient(wsdl="http://localhost:8000/webservices/sample/call/soap?WSDL")
	 #call SOAP method
	#response = client.listaOrgao(nome='Ministerio 1',endereco='',cidade='',uf='')
	#response = client.insereOrgao(cnpj='1223456',nome='Ministerio WEB',endereco='dfdf',cidade='dddd',uf='df')
	response = client.insereEmpregado(nome='Empregado WEB',dt_contratacao='18/07/2013',dt_desligamento='',dt_nascimento='19/09/1989',nu_matricula='M123456',rg='123',cpf='123456',id_orgao='2',documentos='',dependentes='')
	try:
		result = response['s']
		#result = response['orgaos']
	except SoapFault:
		result = None
		
	return dict(xml_request=client.xml_request,xml_response=client.xml_response,result=result)

#	import mongo
#	Model = mongo.Model()
#	orgaos = Model.listaOrgao(nome='Ministerio 1')
#	return dict(orgaos)
