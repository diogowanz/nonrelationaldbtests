import copy
import sys
import os
import re
import datetime

from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
	
#	try:
		
#		c = Connection(host="localhost",port=27017)
#		print "Conectado!"
		
#	except ConnectionFailure, e:
#		sys.stderr.write("Nao foi possivel conectar: %s" % e)
#		sys.exit(1)

#	dbh = c["rhdb001"]
	
#	assert dbh.connection == c
#	print "banco de dados setado"
	
#	insereOrgao('','','','')
#	insereEmpregado('','','','','','','','')
#	insereDependente('','','','')
#	listaOrgao('','','','')
	listaEmpregados(nome='Empre')
	
def conectaMongo():
	try:
		
		c = Connection(host="localhost",port=27017)
		print "Conectado!"
		
	except ConnectionFailure, e:
		sys.stderr.write("Nao foi possivel conectar: %s" % e)
		sys.exit(1)

	dbh = c["rhdb001"]
	
	assert dbh.connection == c
	print "banco de dados setado"
	
	return dbh
	
	
def insereOrgao(nome,endereco,cidade,uf):
	
	dbh = conectaMongo()
	
	orgao = {
		"nome" : "Ministerio da Cultura",
		"endereco" : "esplanada dos ministerios",
		"cidade" : "Brasilia",
		"uf" : "DF"
	}
	
	orgao2 = {
		"nome" : nome,
		"endereco" : endereco,
		"cidade" : cidade,
		"uf" : uf
	}
	
	dbh.orgaos.insert(orgao,safe=True)
	print "orgao inserido com sucesso %s" % orgao
	
def insereEmpregado(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,id_orgao,documentos,dependentes):
	
	dbh = conectaMongo()
	
	id1 = 12321
	id2 = 98741
	
	empregado = {
		"nome" : "Empregado T. Mongo Db",
		"dt_contratacao" : "01-01-2000",
		"dt_desligamento" : "01-01-2009",
		"dt_nascimento" : "01-01-1970",
		"nu_matricula" : "M999999",
		"id_orgao" : None,
		"Documentos" : [
		
			{
				"tp_documento" : "Certidao de Nascimento",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
			{
				"tp_documento" : "Carteira de trabalho",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
			{
				"tp_documento" : "Copia de RG",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
		],
		"Dependentes": [id1,id2]
	}
	
	empregado2 = {
		"nome" : nome,
		"dt_contratacao" : dt_contratacao,
		"dt_desligamento" : dt_desligamento,
		"dt_nascimento" : dt_nascimento,
		"nu_matricula" : nu_matricula,
		"id_orgao" : id_orgao,
		"Documentos" : documentos,
		"Dependentes": dependentes
	}
	
	dbh.empregados.insert(empregado,safe=True)
	print "empregado inserido com sucesso %s" % empregado
	
def insereDependente(nome,dt_nascimento,tp_vinculo,documentos):
	dbh = conectaMongo()
	
	dependente = {
		"nome" : "Dependente T. Mongo Db",
		"dt_nascimento" : "01-01-1970",
		"tp_vinculo" : "filho",
		"Documentos" : [
		
			{
				"tp_documento" : "Certidao de Nascimento",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
			{
				"tp_documento" : "Carteira de trabalho",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
			{
				"tp_documento" : "Copia de RG",
				"no_documento" : "/home/wanzeller/Documentos/teste.odt",
				"dh_updload" : datetime.datetime.now()
			},
		]
	}
	
	
	dependente2 = {
		"nome" : nome,
		"dt_nascimento" : dt_nascimento,
		"tp_vinculo" : tp_vinculo,
		"Documentos" : documentos
	}
	dbh.dependentes.insert(dependente,safe=True)
	print "dependente inserido com sucesso %s" % dependente	
	
def insereDocEmpregado(matricula,id_empregado,no_doc)
	if os.path.isfile(no_doc):
		dbh = conectaMongo()
		query = {
			'matricula' : matricula
		}
		empregado = dbh.empregados.find_one(query)
		if empregado == None:
			print "O Empregado informado não foi encontrado!"
		else:
			new_doc = {
						"tp_documento" : "Copia de RG",
						"no_documento" : "/home/wanzeller/Documentos/teste.odt",
						"dh_updload" : datetime.datetime.now()
					}
			dbh.empregados.update({"matricula":matricula},
			{"$push":{"Documentos":new_doc}}, safe=True)
	else:
		print("Arquivo não encontrato.")
	
	
def listaOrgao(nome='',endereco='',cidade='',uf=''):
	dbh = conectaMongo()
	if nome == '' and endereco == '' and cidade == '' and uf == '':
		print "Favor inserir algum parametro para a consulta!"
	else:			
		orgaos = dbh.orgaos.find({"nome": {"$regex" : "Minist*"}})
		if orgaos.count() == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			for orgao in orgaos:
				print orgao.get("nome")
		

def listaEmpregados(nome='',dt_contratacao='',dt_desligamento='',dt_nascimento='',nu_matricula=''):
	dbh = conectaMongo()
	if nome == '' and dt_contratacao == '' and dt_desligamento == '' and dt_nascimento == '' and nu_matricula == '':
		print "Favor inserir algum parametro para a consulta!"
	else:			
		empregados = dbh.empregados.find({"nome": {"$regex" : "Empregsw*"}})
		if empregados.count() == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			for empregado in empregados:
				print empregado.get("nome")

			
if __name__=="__main__":
	main()
