# coding: utf8
# tente algo como

import copy
import sys
import os
import re
import datetime

from pymongo import Connection
from pymongo.bson import ObjectId 
from pymongo.errors import ConnectionFailure

class Model:
		
	def conectaMongo(self):
		try:
			
			c = Connection(host="localhost",port=27017)
			print "Conectado!"
			
		except ConnectionFailure, e:
			sys.stderr.write("Nao foi possivel conectar: %s" % e)
			sys.exit(1)

		dbh = c["rhdb001"]
		
		assert dbh.connection == c
		return dbh
		
		
	def insereOrgao(self,cnpj,nome,endereco,cidade,uf):
		
		dbh = self.conectaMongo()
		
		orgao = {
			"nu_cnpj" : cnpj,
			"no_orgao" : nome,
			"no_endereco" : endereco,
			"no_cidade" : cidade,
			"no_uf" : uf
		}
		
		dbh.orgaos.insert(orgao,safe=True)
		return "orgao inserido com sucesso"
		
	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos,dependentes):
		
		dbh = self.conectaMongo()
		
		idorgao = ObjectId(id_orgao)
		orgao = dbh.orgaos.find_one({'_id': idorgao})
		
		empregado = {
			"no_empregado" : nome,
			"dt_contratacao" : dt_contratacao,
			"dt_desligamento" : dt_desligamento,
			"dt_nascimento" : dt_nascimento,
			"nu_matricula" : nu_matricula,
			"nu_rg" : rg,
			"nu_cpf" : cpf,
			"id_orgao" : orgao.get('_id'),
			"Documentos" : documentos,
			"Dependentes": dependentes
		}
		
		dbh.empregados.insert(empregado,safe=True)
		return "empregado inserido com sucesso"
		
	def insereDependente(self,nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,idEmpregado):
		dbh = self.conectaMongo()
		
		dependente = {
			"no_empregado_dependente" : nome,
			"nu_rg" : rg,
			"nu_cpf" : cpf,
			"nu_certidao" : certidao,
			"dt_nascimento" : dt_nascimento,
			"tp_vinculo" : tp_vinculo,
			"Documentos" : documentos
		}
		dbh.dependentes.insert(dependente,safe=True)
		newDependente = dbh.dependentes.find_one(dependente)
		idEmpregado = ObjectId(idEmpregado)
		empregado = dbh.empregados.find_one({'_id': idEmpregado})
		if empregado.get('Dependentes') == None:
			dbh.empregados.update({"_id":idEmpregado},{"$set":{"Dependentes":[newDependente.get('_id')]}},safe=True)
		else:
			dbh.empregados.update({"_id":idEmpregado},
				{"$push":{"Dependentes":newDependente.get('_id')}}, safe=True)
		return "Dependente inserido com sucesso!"	
		
	def insereDocEmpregado(self,matricula,tp_documento, no_doc,file):
		dbh = self.conectaMongo()
		query = {
			'nu_matricula' : matricula
		}
		empregado = dbh.empregados.find_one(query)
		
		if empregado == None:
			print "O Empregado informado nao foi encontrado!"
		else:
			if not os.path.exists("/var/mongoDocs/"+str(empregado.get("id_orgao"))):
				os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula")))
			elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))):
				os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula")))
			no_doc = '/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+no_doc
			upload_file(file,no_doc)
			new_doc = {
						"tp_documento" : tp_documento,
						"no_documento" : no_doc,
						"dh_updload" : datetime.datetime.now()
					}
			if empregado.get('Documentos') == None:
				dbh.empregados.update({"nu_matricula":matricula},{"$set":{"Documentos":[new_doc]}},safe=True)
			else:
				dbh.empregados.update({"nu_matricula":matricula},
			{"$push":{"Documentos":new_doc}}, safe=True)
			return 'Documento inserido com sucesso!'
			
	def insereDocDependente(self,empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
		dbh = self.conectaMongo()
		if empreg_matricula != None and empreg_matricula != '':
			queryEmpregado = {
				'nu_matricula' : empreg_matricula
			}
			if rg_dependente != None and rg_dependente != '':
				query = {
					'nu_rg' : rg_dependente
				}
			elif cpf_dependente != None and cpf_dependente != '':
				query = {
					'nu_cpf' : cpf_dependente
				}
			elif certidao_dependente != None and certidao_dependente != '':
				query = {
					'nu_certidao' : certidao_dependente
				}
			else:
				print 'Insira os dados do dependente'
		else:
			print 'Insira a matricula do empregado.'
		empregado = dbh.empregados.find_one(queryEmpregado)
		print empregado.get('no_empregado')
		dependente = dbh.dependentes.find_one(query)
		print dependente.get('no_empregado_dependente')
		
		if empregado == None:
			print "O Empregado informado nao foi encontrado!"
		else:
			if not os.path.exists("/var/mongoDocs/"+str(empregado.get("id_orgao"))):
				os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+str(dependente.get("_id")))
			elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))):
				os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+str(dependente.get("_id")))
			elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+str(dependente.get("_id"))):
				os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+str(dependente.get("_id")))
			no_doc = '/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("nu_matricula"))+'/'+str(dependente.get("_id"))+'/'+no_doc
			upload_file(file,no_doc)
			new_doc = {
						"tp_documento" : tp_documento,
						"no_documento" : no_doc,
						"dh_updload" : datetime.datetime.now()
					}
			if dependente.get('Documentos') == None:
				dbh.dependentes.update({"_id":dependente.get('_id')},{"$set":{"Documentos":[new_doc]}},safe=True)
			else:
				dbh.depententes.update({"_id":dependente.get('_id')},
			{"$push":{"Documentos":new_doc}}, safe=True)
			return 'Documento inserido com sucesso!'
		
		
	def listaOrgaos(self,nome='',endereco='',cidade='',uf=''):
		dbh = self.conectaMongo()
		if nome == '' and endereco == '' and cidade == '' and uf == '':
			print "Favor inserir algum parametro para a consulta!"
		else:
			query = dict()
			if nome != '' and nome != None:
				query['no_orgao'] = {"$regex" : '(^|\w)'+nome+'*'}
			if endereco != '' and endereco != None:
				query['no_endereco'] = {"$regex": '(^|\w)'+endereco+'*'}
			if cidade != '' and cidade != None:
				query['no_cidade'] = {"$regex": '(^|\w)'+cidade+'*'}
			if uf != '' and uf != None:
				query['no_uf'] = {"$regex": '(^|\w)'+uf+'*'}
			orgaos = dbh.orgaos.find(query)

			if orgaos.count() == 0:
				print "Nenhum dado econtrado. Verifique os parametros de busca."
			else:
				orgaosDict=[]
				for row in orgaos:
					l = dict()
					for column in row:
						l[str(column.replace("_",''))] = str(row[column])
					orgaosDict.append(l)
				return orgaosDict
			

	def listaEmpregados(self,nome='',dt_contratacao='',dt_desligamento='',dt_nascimento='',nu_matricula=''):
		dbh = self.conectaMongo()
		if nome == '' and dt_contratacao == '' and dt_desligamento == '' and dt_nascimento == '' and nu_matricula == '':
			print "Favor inserir algum parametro para a consulta!"
		else:
			
			query = dict()
			if nome != '' and nome != None:
				query['no_nome'] = {"$regex" : '(^|\w)'+nome+'*'}
			if dt_contratacao != '' and dt_contratacao != None:
				query['dt_contratacao'] = {"$regex": '(^|\w)'+dt_contratacao+'*'}
			if dt_desligamento != '' and dt_desligamento != None:
				query['dt_desligamento'] = {"$regex": '(^|\w)'+dt_desligamento+'*'}
			if dt_nascimento != '' and dt_nascimento != None:
				query['dt_nascimento'] = {"$regex": '(^|\w)'+dt_nascimento+'*'}
			if nu_matricula != '' and nu_matricula != None:
				query['nu_matricula'] = {"$regex": '(^|\w)'+nu_matricula+'*'}
				
			empregados = dbh.empregados.find(query)
			
			if empregados.count() == 0:
				print "Nenhum dado econtrado. Verifique os parametros de busca."
			else:
				empregadoDict=[]
				for row in empregados:
					l = dict()
					for column in row:
						l[str(column.replace("_",''))] = str(row[column])
					empregadoDict.append(l)
				return empregadoDict
					
	def listaDependentes(self,nomeEmpregado='',nomeDependente='',matricula='',dt_nascimento='',tp_vinculo=''):
		dbh = self.conectaMongo()
		if nomeEmpregado == '' and nomeDependente == '' and matricula == '' and dt_nascimento == '' and tp_vinculo == '':
			print "Favor inserir algum parametro para a consulta!"
		else:			
			query = dict()
			if nomeDependente != '' and nomeDependente != None:
				query['no_empregado_dependente'] = {"$regex" : '(^|\w)'+nomeDependente+'*'}
			if dt_nascimento != '' and dt_nascimento != None:
				query['dt_nascimento'] = {"$regex": '(^|\w)'+dt_nascimento+'*'}
			if tp_vinculo != '' and tp_vinculo != None:
				query['tp_vinculo'] = {"$regex": '(^|\w)'+tp_vinculo+'*'}
			dependentes = dbh.dependentes.find(query)
			if dependentes.count() == 0:
				print "Nenhum dado econtrado. Verifique os parametros de busca."
			else:
				dependenteDict=[]
				for row in dependentes:
					l = dict()
					for column in row:
						l[str(column.replace("_",''))] = str(row[column])
					dependenteDict.append(l)
				return dependenteDict
					
	def retornaDocEmpregado (self,matricula,id_empregado):
		print 'Temporario'
		
	def retornaDocDependente (self,id_dependente,rg,cpf,certidao):
		print 'Temporario'
					
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
