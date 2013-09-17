import copy
import sys
import os
import re
import datetime
import ConfigParser

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
			orgao = dbh.orgaos.find_one({'nu_cnpj': cnpj})
			if orgao != None:
				if len(orgao) == 0:
					orgao = {
						"nu_cnpj" : cnpj,
						"no_orgao" : nome.strip().upper(),
						"no_endereco" : endereco.strip().upper(),
						"no_cidade" : cidade.strip().upper(),
						"no_uf" : uf.strip().upper()
					}
					
					dbh.orgaos.insert(orgao,safe=True)
					return "Orgao inserido com sucesso."
				else:
					return "Orgao de cnpj '"+cnpj+"' ja existe."
			else:
					orgao = {
						"nu_cnpj" : cnpj,
						"no_orgao" : nome.strip().upper(),
						"no_endereco" : endereco.strip().upper(),
						"no_cidade" : cidade.strip().upper(),
						"no_uf" : uf.strip().upper()
					}
					
					dbh.orgaos.insert(orgao,safe=True)
					return "Orgao inserido com sucesso."
		
	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao,documentos):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_contratacao)) or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(nu_matricula)) or self.validaCampo(str(rg)) or self.validaCampo(str(cpf)) or self.validaCampo(str(cnpj_orgao)):
			return "Favor informar os seguintes campos: Nome, Data de Contratacao, Data de Nascimento, Matricula, RG, CPF e ID da Empresa."
		else:
			dbh = self.conectaMongo()
			orgao = dbh.orgaos.find_one({'nu_cnpj': cnpj_orgao})
			if orgao != None:
				if len(orgao) == 0:
					return "O orgao informado nao e valido."
				else:
					empregado = dbh.empregados.find_one({'$or' : [{'nu_rg': rg},{'nu_cpf' : cpf},{'nu_matricula':nu_matricula.strip().upper()}]})
					if empregado != None:
						if len(empregado) == 0:
							empregado = {
								"no_empregado" : nome.strip().upper(),
								"dt_contratacao" : dt_contratacao,
								"dt_desligamento" : dt_desligamento,
								"dt_nascimento" : dt_nascimento,
								"nu_matricula" : nu_matricula.strip().upper(),
								"nu_rg" : rg,
								"nu_cpf" : cpf,
								"id_orgao" : orgao.get('_id'),
								"Documentos" : documentos
							}
							
							dbh.empregados.insert(empregado,safe=True)
							return "empregado inserido com sucesso!"
						else:
							return "O empregado informado ja existe"
					else:
						empregado = {
							"no_empregado" : nome.strip().upper(),
							"dt_contratacao" : dt_contratacao,
							"dt_desligamento" : dt_desligamento,
							"dt_nascimento" : dt_nascimento,
							"nu_matricula" : nu_matricula.strip().upper(),
							"nu_rg" : rg,
							"nu_cpf" : cpf,
							"id_orgao" : orgao.get('_id'),
							"Documentos" : documentos
						}
						
						dbh.empregados.insert(empregado,safe=True)
						return "empregado inserido com sucesso!"
			else:
				return "O orgao informado nao e valido."
		
	def insereDependente(self,nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,nu_matricula_responsavel):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(tp_vinculo)) or self.validaCampo(str(nu_matricula_responsavel)):
			return "Favor informar os seguintes campos: Nome, Tipo de Vinculo, Matricula do Responsavel."
		elif self.validaCampo(str(rg)) and self.validaCampo(str(cpf)) and self.validaCampo(str(certidao)):
			return "Informar pelo menos um dos seguintes campos: RG, CPF, CERTIDAO."
		else:
			dbh = self.conectaMongo()
			tp_vinculo = ObjectId(tp_vinculo)
			vinculo = dbh.vinculos.find_one({"_id":tp_vinculo})
			if len(vinculo) == 0:
				return "Vinculo informado nao existe."
			else:
				empregado = dbh.empregados.find_one({'nu_matricula': nu_matricula_responsavel})
				if empregado != None:
					if len(empregado) != 0:
						dependente = dbh.dependentes.find_one({'$or' : [{'nu_rg': rg},{'nu_cpf' : cpf},{'nu_certidao':certidao}]})
						if dependente != None:
							if len(dependente) == 0:
								dependente = {
									"id_empregado" : empregado.get('_id'),
									"no_empregado_dependente" : nome.strip().upper(),
									"nu_rg" : rg,
									"nu_cpf" : cpf,
									"nu_certidao" : certidao,
									"dt_nascimento" : dt_nascimento,
									"tp_vinculo" : vinculo.get("_id"),
									"Documentos" : documentos
								}
								dbh.dependentes.insert(dependente,safe=True)
								return "Dependente inserido com sucesso!"
							else:
								return "O dependente informado ja existe."
						else:
							dependente = {
								"id_empregado" : empregado.get('_id'),
								"no_empregado_dependente" : nome.strip().upper(),
								"nu_rg" : rg,
								"nu_cpf" : cpf,
								"nu_certidao" : certidao,
								"dt_nascimento" : dt_nascimento,
								"tp_vinculo" : vinculo.get("_id"),
								"Documentos" : documentos
							}
							dbh.dependentes.insert(dependente,safe=True)
							return "Dependente inserido com sucesso!"
					else:
						return "O responsavel informado nao foi encontrado."
				else:
					return "O responsavel informado nao foi encontrado."
		
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
				if len(tipo_documento) == 0:
					return "O tipo de documento informado nao existe"
				else:
					config = ConfigParser.ConfigParser()
					config.read("./config.conf")
					if not os.path.exists(config.get("path", "filePath")+str(empregado.get("id_orgao"))):
						os.makedirs(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id")))
					elif not os.path.exists(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))):
						os.makedirs(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id")))
					no_doc = config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+no_doc
					self.upload_file(file,no_doc)
					new_doc = {
								"tp_documento" : tp_documento,
								"no_documento" : no_doc.strip(),
								"dh_updload" : datetime.datetime.now()
							}
					if empregado.get('Documentos') == None or empregado.get('Documentos') == '':
						dbh.empregados.update({"nu_matricula":matricula},{"$set":{"Documentos":[new_doc]}},safe=True)
					else:
						dbh.empregados.update({"nu_matricula":matricula},{"$push":{"Documentos":new_doc}}, safe=True)
					return "Documento inserido!"
		
	def insereDocDependente(self,empreg_matricula,rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
		if self.validaCampo(str(empreg_matricula)) or self.validaCampo(str(tp_documento)) or self.validaCampo(str(no_doc)):
			return "Favor informar os seguintes campos: Matricula do Responsavel, Tipo de Documento, Nome do Documento."
		elif self.validaCampo(str(rg_dependente)) and self.validaCampo(str(cpf_dependente)) and self.validaCampo(str(certidao_dependente)):
			return "Favor informar pelo menos um dos seguintes campos: RG do Dependente, CPF do Dependente, Certidao do Dependente."
		else:
			if not self.validaCampo(empreg_matricula):
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
					return 'Insira os dados do dependente'
				dbh = self.conectaMongo()
				empregado = dbh.empregados.find_one(queryEmpregado)
				dependente = dbh.dependentes.find_one(query)
			
			if empregado == None:
				print "O Empregado informado nao foi encontrado!"
			elif dependente == None:
				return "O dependente informado nao foi encontrado!"
			else:
				tp_documento = ObjectId(tp_documento)
				tipo_documento = dbh.tp_documentos.find_one({"_id":tp_documento})
				if len(tipo_documento) == 0:
					return "O tipo de documento informado nao existe"
				else:
					config = ConfigParser.ConfigParser()
					config.read("config.conf")
					if not os.path.exists(config.get("path", "filePath")+str(empregado.get("id_orgao"))):
						os.makedirs(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					elif not os.path.exists(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))):
						os.makedirs(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					elif not os.path.exists(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id"))):
						os.makedirs(config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id")))
					no_doc = config.get("path", "filePath")+str(empregado.get("id_orgao"))+'/'+str(empregado.get("_id"))+'/'+str(dependente.get("_id"))+'/'+no_doc
					self.upload_file(file,no_doc)
					new_doc = {
								"tp_documento" : tp_documento,
								"no_documento" : no_doc.strip(),
								"dh_updload" : datetime.datetime.now()
							}
					if dependente.get('Documentos') == None or dependente.get('Documentos') == '':
						dbh.dependentes.update({"_id":dependente.get('_id')},{"$set":{"Documentos":[new_doc]}},safe=True)
						return "Documento inserido!"
					else:
						dbh.dependentes.update({"_id":dependente.get('_id')},{"$push":{"Documentos":new_doc}}, safe=True)
						return "Documento inserido!"
					
	def listaOrgaos(self,cnpj='',nome='',endereco='',cidade='',uf=''):
		dbh = self.conectaMongo()
		query = dict()
		if not(self.validaCampo(cnpj)):
			query['nu_cnpj'] = {"$regex" : str(cnpj)}
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
			

	def listaEmpregados(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf, cnpj_orgao):
		dbh = self.conectaMongo()
		query = []
		if not(self.validaCampo(nome)):
			query.append({'no_empregado' : {"$regex" : nome.strip().upper()}})
		if not(self.validaCampo(dt_contratacao)):
			query.append({'dt_contratacao' : dt_contratacao})
		if not(self.validaCampo(dt_desligamento)):
			query.append({'dt_desligamento' : dt_desligamento})
		if not(self.validaCampo(dt_nascimento)):
			query.append({'dt_nascimento' : dt_nascimento})
		if not(self.validaCampo(nu_matricula)):
			query.append({'nu_matricula' : {"$regex": nu_matricula.strip().upper()}})
			
		if len(query) != 0:
			empregados = dbh.empregados.find({'$and' : query})
		else:
			empregados = dbh.empregados.find()
		
		if empregados.count() == 0:
			return "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			empregadoDict=[]
			for row in empregados:
				l = dict()
				for column in row:
					l[str(column.replace("_id",'id_empregado'))] = str(row[column])
				empregadoDict.append(l)
			return empregadoDict
					
	def listaDependentes(self,nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo,rg,cpf,certidao):
		dbh = self.conectaMongo()
		x = []
		if not(self.validaCampo(nomeEmpregado)):
			x.append({'no_empregado' : {"$regex" : '(^|\w)'+nomeEmpregado.strip().upper()+'*'}})
		if not(self.validaCampo(matricula)):
			x.append({'nu_matricula' : matricula.strip().upper()})
		empregado = dbh.empregados.find_one({'$and' : x})
		id_empregado = empregado.get('_id')
		query = []
		if not(self.validaCampo(nomeDependente)):
			query.append({'no_empregado_dependente' : {"$regex" : '(^|\w)'+nomeDependente.strip().upper()+'*'}})
		if not(self.validaCampo(dt_nascimento)):
			query.append({'dt_nascimento' : {"$regex": '(^|\w)'+dt_nascimento+'*'}})
		if not(self.validaCampo(tp_vinculo)):
			query.append({'tp_vinculo' : {"$regex": '(^|\w)'+tp_vinculo+'*'}})
		if not(self.validaCampo(str(id_empregado))):
			query.append({'id_empregado' : id_empregado})
		dependentes = dbh.dependentes.find({'$and' : query})
		if dependentes.count() == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			dependenteDict=[]
			for row in dependentes:
				l = dict()
				for column in row:
					l[str(column.replace("_id",'id_empregado_dependente'))] = str(row[column])
				dependenteDict.append(l)
			return dependenteDict
					
	def retornaDocEmpregado (self,nu_matricula,no_documento,tp_documento):
		if self.validaCampo(nu_matricula):
			return 'Favor informar a matricula do empregado.'
		else:
			dbh = self.conectaMongo()
			x = []
			x.append({'nu_matricula' : nu_matricula.strip().upper()})
			if not(self.validaCampo(no_documento)):
				x.append({'Documentos.no_documento' : {"$regex" : '(^|\w)'+no_documento.strip().upper()+'*'}})
			if not(self.validaCampo(tp_documento)):
				x.append({'Documentos.tp_documento': {"$regex" : '(^|\w)'+tp_documento+'*'}})
			documentos_empregado = dbh.empregados.find_one({'$and' : x})
			documentos_empregado = documentos_empregado.get('Documentos')
			docsEmpregadoDict=[]
			for row in documentos_empregado:
				l = dict()
				file=open(str(row['no_documento']), 'rb')
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
		
	def listaVinculos (self,nu_tipo_vinculo,no_tipo_vinculo):
		dbh = self.conectaMongo()
		query = dict()
		if not(self.validaCampo(nu_tipo_vinculo)):
			nu_tipo_vinculo = ObjectId(nu_tipo_vinculo)
			query['_id'] = {"_id" : +nu_tipo_vinculo.strip()}
		if not(self.validaCampo(no_tipo_vinculo)):
			query['no_tipo_vinculo'] = {"$regex" : '(^|\w)'+no_tipo_vinculo.strip().upper()+'*'}
		
		vinculos = dbh.vinculos.find(query)
		docsVinculosDict=[]
		for row in vinculos:
			l = dict()
			for column in row:
				l[str(column.replace("_id",'id_tipo_vinculo'))] = str(row[column])
			docsVinculosDict.append(l)

		return docsVinculosDict
		
	def listaTipoDocumentos (self,nu_tipo_documento,no_tipo_documento):
		dbh = self.conectaMongo()
		query = dict()
		if not(self.validaCampo(nu_tipo_documento)):
			nu_tipo_documento = ObjectId(nu_tipo_documento)
			query['_id'] = {"_id" : +nu_tipo_documento.strip()}
		if not(self.validaCampo(no_tipo_documento)):
			query['no_tipo_documento'] = {"$regex" : '(^|\w)'+no_tipo_documento.strip().upper()+'*'}
		
		TipoDocumentos = dbh.tp_documentos.find(query)
		docsDocumentosDict=[]
		for row in TipoDocumentos:
			l = dict()
			for column in row:
				l[str(column.replace("_id",'id_tipo_documento'))] = str(row[column])
			docsDocumentosDict.append(l)

		return docsDocumentosDict
				
								
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
