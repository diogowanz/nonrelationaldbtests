import copy
import sys
import os
import re
import datetime

from pymongo import Connection
#from pymongo.bson import ObjectId
from bson import ObjectId 
from pymongo.errors import ConnectionFailure

class Model:
		
	def conectaMongo(self):
		try:
			
			c = Connection(host="localhost",port=27017)
			
		except ConnectionFailure, e:
			sys.stderr.write("Nao foi possivel conectar: %s" % e)
			sys.exit(1)

		dbh = c["rhdb001"]
		
		assert dbh.connection == c
		return dbh
		
	def validaCampo(self, txt):
		if txt == 'None' or txt.strip() == '':
			return True
		else:
			return False
		
		
	def insereOrgao(self,cnpj,nome,endereco,cidade,uf):
		if self.validaCampo(str(cnpj))  or self.validaCampo(str(nome)) or self.validaCampo(str(endereco)) or self.validaCampo(str(cidade)) or self.validaCampo(str(uf)):
			return "Favor informar todos os campos."
		else:
			dbh = self.conectaMongo()
			orgao = {
				"nu_cnpj" : cnpj,
				"no_orgao" : nome.strip().upper(),
				"no_endereco" : endereco.strip().upper(),
				"no_cidade" : cidade.strip().upper(),
				"no_uf" : uf.strip().upper()
			}
			
			dbh.orgaos.insert(orgao,safe=True)
			return "Orgao inserido com sucesso."
		
	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos,dependentes):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_contratacao)) or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(nu_matricula)) or self.validaCampo(str(rg)) or self.validaCampo(str(cpf)) or self.validaCampo(str(id_orgao)):
			return "Favor informar os seguintes campos: Nome, Data de Contratacao, Data de Nascimento, Matricula, RG, CPF e ID da Empresa."
		else:
			dbh = self.conectaMongo()
			
			idorgao = ObjectId(id_orgao)
			orgao = dbh.orgaos.find_one({'_id': idorgao})
			
			empregado = {
				"no_empregado" : nome.strip().upper(),
				"dt_contratacao" : dt_contratacao,
				"dt_desligamento" : dt_desligamento,
				"dt_nascimento" : dt_nascimento,
				"nu_matricula" : nu_matricula.strip().upper(),
				"nu_rg" : rg,
				"nu_cpf" : cpf,
				"id_orgao" : orgao.get('_id'),
				"Documentos" : documentos,
				"Dependentes": dependentes
			}
			
			dbh.empregados.insert(empregado,safe=True)
			return "empregado inserido com sucesso!"
		
	def insereDependente(self,nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,idEmpregado):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(tp_vinculo)) or self.validaCampo(str(nu_matricula_responsavel)):
			return "Favor informar os seguintes campos: Nome, Tipo de Vinculo, Matricula do Responsavel."
		elif self.validaCampo(str(rg)) and self.validaCampo(str(cpf)) and self.validaCampo(str(certidao)):
			return "Informar pelo menos um dos seguintes campos: RG, CPF, CERTIDAO."
		else:
			dbh = self.conectaMongo()
			tp_vinculo = ObjectId(tp_vinculo)
			vinculo = dbh.vinculos.find_one({"_id":tp_vinculo})
			if vinculo.count() == 0:
				return "Vinculo informado não existe."
			else:
				dependente = {
					"no_empregado_dependente" : nome.strip().upper(),
					"nu_rg" : rg,
					"nu_cpf" : cpf,
					"nu_certidao" : certidao,
					"dt_nascimento" : dt_nascimento,
					"tp_vinculo" : vinculo.get("_id"),
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
		if self.validaCampo(str(matricula))  or self.validaCampo(str(tp_documento)) or self.validaCampo(str(no_doc)):
			return "Favor informar todos os campos."
		else:
			dbh = self.conectaMongo()
			query = {
				'nu_matricula' : matricula
			}
			empregado = dbh.empregados.find_one(query)
			
			if empregado == None:
				print "O Empregado informado nao foi encontrado!"
			else:
				tp_documento = ObjectId(tp_documento)
				tipo_documento = dbh.tp_documentos.find_one({"_id":tp_documento})
				if tipo_documento.count() == 0:
					return "O tipo de documento informado não existe"
				else:
					if not os.path.exists("/var/mongoDocs/"+str(empregado.get("id_orgao"))):
						os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id")))
					elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))):
						os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id")))
					no_doc = '/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+no_doc
					upload_file(file,no_doc)
					new_doc = {
								"tp_documento" : tp_documento,
								"no_documento" : no_doc.strip().upper(),
								"dh_updload" : datetime.datetime.now()
							}
					if empregado.get('Documentos') == None:
						dbh.empregados.update({"nu_matricula":matricula},{"$set":{"Documentos":[new_doc]}},safe=True)
					else:
						dbh.empregados.update({"nu_matricula":matricula},
					{"$push":{"Documentos":new_doc}}, safe=True)
					return "Documento inserido!"
			
	def insereDocDependente(self,empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
		if self.validaCampo(str(empreg_matricula)) or self.validaCampo(str(tp_documento)) or self.validaCampo(str(no_doc)):
			return "Favor informar os seguintes campos: Matricula do Responsavel, Tipo de Documento, Nome do Documento."
		elif self.validaCampo(str(rg_dependente)) and self.validaCampo(str(cpf_dependente)) and self.validaCampo(str(certidao_dependente)):
			return "Favor informar pelo menos um dos seguintes campos: RG do Dependente, CPF do Dependente, Certidao do Dependente."
		else:
			dbh = self.conectaMongo()
			tp_documento = ObjectId(tp_documento)
			tipo_documento = dbh.tp_documentos.find_one({"_id":tp_documento})
			if tipo_documento.count() == 0:
				return "O tipo de documento informado não existe"
			else:
				if self.validaCampo(empreg_matricula):
					queryEmpregado = {
						'nu_matricula' : empreg_matricula.strip().upper()
					}
					if not (self.validaCampo(rg_dependente)):
						query = {
							'nu_rg' : rg_dependente
						}
					elif not (self.validaCampo(cpf_dependente)):
						query = {
							'nu_cpf' : cpf_dependente
						}
					elif not (self.validaCampo(certidao_dependente)):
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
						os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))):
						os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					elif not os.path.exists('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id"))):
						os.makedirs('/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					no_doc = '/var/mongoDocs/'+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id"))+'/'+no_doc
					upload_file(file,no_doc)
					new_doc = {
								"tp_documento" : tp_documento,
								"no_documento" : no_doc.strip().upper(),
								"dh_updload" : datetime.datetime.now()
							}
					if dependente.get('Documentos') == None:
						dbh.dependentes.update({"_id":dependente.get('_id')},{"$set":{"Documentos":[new_doc]}},safe=True)
					else:
						dbh.depententes.update({"_id":dependente.get('_id')},
					{"$push":{"Documentos":new_doc}}, safe=True)
					return "Documento inserido!"
		
		
	def listaOrgaos(self,nome='',endereco='',cidade='',uf=''):
		dbh = self.conectaMongo()
		query = dict()
		if not(self.validaCampo(nome)):
			query['no_orgao'] = {"$regex" : '(^|\w)'+nome.strip().upper()+'*'}
		if not(self.validaCampo(endereco)):
			query['no_endereco'] = {"$regex": '(^|\w)'+endereco.strip().upper()+'*'}
		if not(self.validaCampo(cidade)):
			query['no_cidade'] = {"$regex": '(^|\w)'+cidade.strip().upper()+'*'}
		if not(self.validaCampo(uf)):
			query['no_uf'] = {"$regex": '(^|\w)'+uf.strip().upper()+'*'}
		orgaos = dbh.orgaos.find(query)

		if orgaos.count() == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			orgaosDict=[]
			for row in orgaos:
				l = dict()
				for column in row:
					l[str(column.replace("_id",'id_orgao'))] = str(row[column])
				orgaosDict.append(l)
			return orgaosDict
			

	def listaEmpregados(self,nome='',dt_contratacao='',dt_desligamento='',dt_nascimento='',nu_matricula=''):
		dbh = self.conectaMongo()
		query = dict()
		if not(self.validaCampo(nome)):
			query['no_empregado'] = {"$regex" : '(^|\w)'+nome.strip().upper()+'*'}
		if not(self.validaCampo(dt_contratacao)):
			query['dt_contratacao'] = {"$regex": '(^|\w)'+dt_contratacao+'*'}
		if not(self.validaCampo(dt_desligamento)):
			query['dt_desligamento'] = {"$regex": '(^|\w)'+dt_desligamento+'*'}
		if not(self.validaCampo(dt_nascimento)):
			query['dt_nascimento'] = {"$regex": '(^|\w)'+dt_nascimento+'*'}
		if not(self.validaCampo(nu_matricula)):
			query['nu_matricula'] = {"$regex": '(^|\w)'+nu_matricula.strip().upper()+'*'}
			
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
		query = dict()
		if not(self.validaCampo(nomeDependente)):
			query['no_empregado_dependente'] = {"$regex" : '(^|\w)'+nomeDependente.strip().upper()+'*'}
		if not(self.validaCampo(dt_nascimento)):
			query['dt_nascimento'] = {"$regex": '(^|\w)'+dt_nascimento+'*'}
		if not(self.validaCampo(tp_vinculo)):
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
					
	def retornaDocEmpregado (self,nu_matricula,no_documento,tp_documento):
		if self.validaCampo(nu_matricula):
			return 'Favor informar a matricula do empregado.'
		else:
			dbh = self.conectaMongo()		
			query = dict()
			query['Documentos.nu_matricula'] = {"$regex" : '(^|\w)'+nu_matricula.strip().upper()+'*'}
			if not(self.validaCampo(no_documento)):
				query['Documentos.no_documento'] = {"$regex" : '(^|\w)'+no_documento.strip().upper()+'*'}
			if not(self.validaCampo(tp_documento)):
				query['Documentos.tp_documento'] = {"$regex" : '(^|\w)'+tp_documento+'*'}
			
			documentos_empregado = dbh.empregados.find(query)

			docsEmpregadoDict=[]
			for row in documentos_empregado:
				l = dict()
				file=open(row['no_documento'], 'rb')
				data=file.read()
				l['file'] = data.encode('base64')
				for collumn in row:
					l[collumn]=row[collumn]
				docsEmpregadoDict.append(l)

		return docsEmpregadoDict
			
		
	def retornaDocDependente (self,nu_rg,nu_cpf,nu_certidao, no_documento, tp_documento):
		if self.validaCampo(nu_rg) and self.validaCampo(nu_cpf) and self.validaCampo(nu_certidao):
			return 'Favor informar um dos campos a seguir: RG, CPF, Certidao.'
		else:
			dbh = self.conectaMongo()		
			query = dict()
			if not(self.validaCampo(no_documento)):
				query['Documentos.no_documento'] = {"$regex" : '(^|\w)'+no_documento.strip().upper()+'*'}
			if not(self.validaCampo(tp_documento)):
				query['Documentos.tp_documento'] = {"$regex" : '(^|\w)'+tp_documento+'*'}
			if not(self.validaCampo(nu_rg)):
				query['Documentos.nu_rg'] = {"$regex" : '(^|\w)'+nu_rg+'*'}
			if not(self.validaCampo(nu_cpf)):
				query['Documentos.nu_cpf'] = {"$regex" : '(^|\w)'+nu_cpf+'*'}
			if not(self.validaCampo(nu_certidao)):
				query['Documentos.nu_certidao'] = {"$regex" : '(^|\w)'+nu_certidao+'*'}

			documentos_dependente = dbh.dependente.find(query)

			docsDependenteDict=[]
			for row in documentos_dependente:
				l = dict()
				file=open(row['no_documento'], 'rb')
				data=file.read()
				l['file'] = data.encode('base64')
				for collumn in row:
					l[collumn]=row[collumn]
				docsDependenteDict.append(l)

		return docsDependenteDict
					
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
