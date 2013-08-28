import psycopg2
import psycopg2.extras
import ConfigParser
import datetime
import os

class Model:

	def abreConexao(self):
		conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="123456")
		return conn
		
	def fechaConexao(self):
		dict_cur.close()
		
	def validaCampo(self, txt):
		if txt == 'None' or txt.strip() == '':
			return True
		else:
			return False

	def insereOrgao(self,cnpj,nome,endereco,cidade,uf):
		if self.validaCampo(str(cnpj))  or self.validaCampo(str(nome)) or self.validaCampo(str(endereco)) or self.validaCampo(str(cidade)) or self.validaCampo(str(uf)):
			return "Favor informar todos os campos."
		else:
			conn = self.abreConexao()
			values = "("+str(cnpj)+",'"+nome.strip().upper()+"','"+endereco.strip().upper()+"','"+cidade.strip().upper()+"','"+uf.strip().upper()+"')"
			sql = "insert into tb002_orgao (nu_cnpj,no_orgao,no_endereco,no_cidade,no_uf) values "+values
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit()
			#cursor.close()
			#return resultado
			return "Orgao inserido com sucesso."

	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_contratacao)) or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(nu_matricula)) or self.validaCampo(str(rg)) or self.validaCampo(str(cpf)) or self.validaCampo(str(id_orgao)):
			return "Favor informar os seguintes campos: Nome, Data de Contratacao, Data de Nascimento, Matricula, RG, CPF e ID da Empresa."
		else:
			conn = self.abreConexao()
			values = "('"+nome.strip().upper()+"','"+dt_contratacao+"','"+dt_nascimento+"','"+nu_matricula.strip().upper()+"',"+str(rg)+","+str(cpf)+","+str(id_orgao)
			if self.validaCampo(dt_desligamento):
				values += ",NULL)"
			else:
				values += ",'"+dt_desligamento+"')"
			if documentos == None:
				documentos = 'Null'
			sql = "insert into tb004_empregado (no_empregado, dt_contratacao,dt_nascimento,nu_matricula,nu_rg,nu_cpf,id_orgao,dt_desligamento) values "+values
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit()
			#cursor.close()
			#return resultado
			return "empregado inserido com sucesso!"
		
	def insereDependente(self,nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,nu_matricula_responsavel):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(tp_vinculo)) or self.validaCampo(str(nu_matricula_responsavel)):
			return "Favor informar os seguintes campos: Nome, Tipo de Vinculo, Matricula do Responsavel."
		elif self.validaCampo(str(rg)) and self.validaCampo(str(cpf)) and self.validaCampo(str(certidao)):
			return "Informar pelo menos um dos seguintes campos: RG, CPF, CERTIDAO."
		else:			
			conn = self.abreConexao()
			sql = "select id_empregado from tb004_empregado where nu_matricula ='"+str(nu_matricula_responsavel).strip().upper()+"'"
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			responsavel = cursor.fetchone()
			if len(responsavel) != 0:
				sql = "select id_tipo_vinculo from tb003_tipo_vinculo where id_tipo_vinculo ="+str(tp_vinculo)
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursor.execute(sql)
				conn.commit()
				if cursor.arraysize != 0:
					resultado = cursor.fetchone()
					id_tipo_vinculo = resultado['id_tipo_vinculo']
					values = "('"+nome.strip().upper()+"','"+dt_nascimento+"',"+str(id_tipo_vinculo)+","+str(responsavel['id_empregado'])
					if self.validaCampo(rg):
						values += ",NULL"
					else:
						values = values +","+str(rg).strip()
					if self.validaCampo(cpf):
						values += ",NULL"
					else:
						values += ","+str(cpf).strip()
					if self.validaCampo(rg):
						values += ",NULL"
					else:
						values += ","+str(certidao).strip()
					values += ")"
					sql = "insert into tb005_empregado_dependente (no_empregado_dependente,dt_nascimento,id_tipo_vinculo,id_empregado,nu_rg,nu_cpf,nu_certidao) values "+values
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					return "Dependente inserido com sucesso!"
				else:
					return "Tipo de vinculo informado invalido!"
			else:
				return "Empregado invalido"
		
	def insereDocEmpregado(self,matricula,tp_documento, no_doc,file):
		if self.validaCampo(str(matricula))  or self.validaCampo(str(tp_documento)) or self.validaCampo(str(no_doc)):
			return "Favor informar todos os campos."
		else:
			conn = self.abreConexao()
			sql = "select * from tb004_empregado where nu_matricula = '"+matricula.strip().upper()+"'"
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			resultEmpregado = cursor
			if resultEmpregado.arraysize != 0:
				sql = "select id_tipo_documento from tb001_tipo_documento where id_tipo_documento = " + tp_documento
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursor.execute(sql)
				resultado = cursor #verificar
				if resultado.arraysize != 0:
					resultEmpregado = resultEmpregado.fetchone()
					config = ConfigParser.ConfigParser()
					config.read("config.conf")
					if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
						os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"]))
					elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])):
						os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"]))
					no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+no_doc
					self.upload_file(file,no_doc)
					sql = "insert into tb006_documento (no_documento,id_tipo_documento,id_empregado,dh_upload) values ('"+no_doc+"',"+tp_documento+","+str(resultEmpregado['id_empregado'])+",'"+str(datetime.datetime.now())+"')"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					return "Documento inserido!"
				else:
					return "Tipo de documento invalido!"
			else:
				return "Matricula invalida!"
				
	def insereDocDependente(self,empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
		#Ver caminho onde sera salvo o arquivo
		#ver tipo de documento
		if self.validaCampo(str(empreg_matricula)) or self.validaCampo(str(tp_documento)) or self.validaCampo(str(no_doc)):
			return "Favor informar os seguintes campos: Matricula do Responsavel, Tipo de Documento, Nome do Documento."
		elif self.validaCampo(str(rg_dependente)) and self.validaCampo(str(cpf_dependente)) and self.validaCampo(str(certidao_dependente)):
			return "Favor informar pelo menos um dos seguintes campos: RG do Dependente, CPF do Dependente, Certidao do Dependente."
		else:
			conn = self.abreConexao()
			sql = "select * from tb004_empregado where nu_matricula = '"+empreg_matricula.strip().upper()+"'"
			cursor1 = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor1.execute(sql)
			conn.commit()
			resultEmpregado = cursor1
			if resultEmpregado.arraysize != 0:
				filtro = ''
				if self.validaCampo(str(rg_dependente)):
					pass
				else:
					filtro +=" and nu_rg = "+str(rg_dependente).strip() 
				if self.validaCampo(str(cpf_dependente)):
					pass
				else:
					filtro +=" and nu_cpf = "+str(cpf_dependente).strip()
				if self.validaCampo(certidao_dependente):
					pass
				else:
					filtro +=" and nu_certidao = "+str(certidao_dependente).strip()
				sql = "select * from tb005_empregado_dependente where 1=1 "+filtro
				cursor2 = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursor2.execute(sql)
				conn.commit()
				resultDependente = cursor2
				if resultDependente.arraysize != 0:
					sql = "select id_tipo_documento from tb001_tipo_documento where id_tipo_documento = "+str(tp_documento)
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					resultado = cursor
					if resultado.arraysize != 0:
						resultEmpregado = resultEmpregado.fetchone()
						resultDependente = resultDependente.fetchone()
						config = ConfigParser.ConfigParser()
						config.read("config.conf")
						if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
						elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
						elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
						no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"])+'/'+no_doc
						self.upload_file(file,no_doc)
						sql = "insert into tb006_documento (id_tipo_documento,id_empregado,id_empregado_dependente,no_documento,dh_upload) values("+str(tp_documento)+","+str(resultEmpregado["id_empregado"])+","+str(resultDependente["id_empregado_dependente"])+",'"+no_doc+"','"+str(datetime.datetime.now())+"')"
						cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
						cursor.execute(sql)
						conn.commit()
						return "Documento inserido!"
					else:
						return "Tipo de documento invalido!"
				else:
					return "Dependente nao encontrado!"
			else:
				return "Empregado nao encontrado!"
					
	def listaOrgaos(self,nome='',endereco='',cidade='',uf=''):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nome)):
			filtro += " and no_orgao like '%"+nome.strip().upper()+"%'"
		if not(self.validaCampo(endereco)):
			filtro += " and no_endereco like '%"+endereco.strip().upper()+"%'"
		if not(self.validaCampo(cidade)):
			filtro += " and no_cidade like '%"+cidade.strip().upper()+"%'"
		if not(self.validaCampo(uf)):
			filtro += " and no_uf like '%"+uf.strip().upper()+"%'"
		sql = "select * from tb002_orgao where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		resultado = cursor.execute(sql)
		conn.commit()

		if cursor.arraysize == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			orgaosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				orgaosDict.append(l)
			return orgaosDict
		
	def listaEmpregados(self,nome='',dt_contratacao='',dt_desligamento='',dt_nascimento='',nu_matricula=''):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nome)):
			filtro += " AND no_empregado like '%"+nome.strip().upper()+"%'"
			
		if not(self.validaCampo(dt_contratacao)):
			filtro += " AND dt_contratacao = '"+dt_contratacao.strip()+"'"
			
		if not(self.validaCampo(dt_desligamento)):
			filtro += " AND dt_desligamento = '"+dt_desligamento.strip()+"'"
			
		if not(self.validaCampo(dt_nascimento)):
			filtro += " AND dt_nascimento = '"+dt_nascimento.strip()+"'"
			
		if not(self.validaCampo(nu_matricula)):
			filtro += " AND nu_matricula like '%"+nu_matricula.strip().upper()+"%'"
			
		sql = "select * from tb004_empregado where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cursor.execute(sql)
		conn.commit()
		empregadosDict=[]
		for row in cursor:
			l = dict()
			for collumn in row:
				l[collumn]=row[collumn]
			empregadosDict.append(l)
		return empregadosDict
		
	def listaDependentes(self,nomeEmpregado='',nomeDependente='',matricula='',dt_nascimento='',tp_vinculo=''):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nomeDependente)):
			filtro += " AND no_empregado_dependente like '%"+nomeDependente.strip().upper()+"%'"
			
		if not(self.validaCampo(nomeEmpregado)):
			filtro += " AND no_empregado like '%"+nomeEmpregado.strip().upper()+"%'"
			
		if not(self.validaCampo(matricula)):
			filtro += " AND nu_matricula like '%"+matricula.strip().upper()+"%'"
			
		if not(self.validaCampo(dt_nascimento)):
			filtro += " AND dt_nascimento = '"+dt_nascimento.strip()+"'"
			
		if not(self.validaCampo(tp_vinculo)):
			filtro += " AND tb005_empregado_dependente.id_tipo_vinculo = "+tp_vinculo.strip()
		sql = "select tb005_empregado_dependente.* from tb005_empregado_dependente join tb004_empregado on tb004_empregado.id_empregado =  tb005_empregado_dependente.id_empregado where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cursor.execute(sql)
		conn.commit()
		dependentesDict=[]
		for row in cursor:
			l = dict()
			for collumn in row:
				l[collumn]=row[collumn]
			dependentesDict.append(l)
		return dependentesDict
		
	def retornaDocEmpregado (self,nu_matricula,no_documento,tp_documento):
		if self.validaCampo(nu_matricula):
			return 'Favor informar a matricula do empregado.'
		else:
			sql = "select no_documento from tb004_empregado "
			sql+=	"join tb006_documento on tb006_documento.id_empregado = tb004_empregado.id_empregado and id_empregado_dependente is null "
			sql+=	"join tb001_tipo_documento on tb001_tipo_documento.id_tipo_documento = tb006_documento.id_tipo_documento "
			sql+= "where 1=1 and nu_matricula = '"+nu_matricula+"'"
			
			filtro = ''
			if not(self.validaCampo(no_documento)):
				filtro += "and no_documento ='"+no_documento+"'"
			if not(self.validaCampo(tp_documento)):
				filtro += "and id_tipo_documento ="+tp_documento
			
			sql += filtro
			conn = self.abreConexao()
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			docsEmpregadoDict=[]
			for row in cursor:
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
			sql = "select no_documento from tb005_empregado_dependente "
			sql+=	"join tb006_documento on tb006_documento.id_empregado_dependente = tb005_empregado_dependente.id_empregado_dependente /*and tb006_documento.id_empregado is null*/ "
			sql+=	"join tb001_tipo_documento on tb001_tipo_documento.id_tipo_documento = tb006_documento.id_tipo_documento "
			sql+= "where 1=1 "
			
			filtro = ''
			if not(self.validaCampo(no_documento)):
				filtro += "and no_documento ='"+no_documento+"'"
			if not(self.validaCampo(tp_documento)):
				filtro += "and id_tipo_documento ="+str(tp_documento)
			if not(self.validaCampo(nu_rg)):
				filtro += "and nu_rg ="+str(nu_rg)
			if not(self.validaCampo(nu_cpf)):
				filtro += "and nu_cpf ="+str(nu_cpf)
			if not(self.validaCampo(nu_certidao)):
				filtro += "and nu_certidao ="+str(nu_certidao)
			
			sql += filtro
			print sql
			conn = self.abreConexao()
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			docsDependenteDict=[]
			for row in cursor:
				l = dict()
				file=open(row['no_documento'], 'rb')
				data=file.read()
				l['file'] = data.encode('base64')
				for collumn in row:
					l[collumn]=row[collumn]
				docsDependenteDict.append(l)

		return docsDependenteDict
		
	def listaVinculos (self,nu_tipo_vinculo,no_tipo_vinculo):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nu_tipo_vinculo)):
			filtro += " and nu_tipo_vinculo ="+nu_tipo_vinculo.strip()+"%'"
		if not(self.validaCampo(no_tipo_vinculo)):
			filtro += " and no_tipo_vinculo like '%"+no_tipo_vinculo.strip()+"%'"
		sql = "select * from tb003_tipo_vinculo where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		resultado = cursor.execute(sql)
		conn.commit()

		if cursor.arraysize == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			vinculosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				vinculosDict.append(l)
			return vinculosDict
			
	def listaTipoDocumentos (self,nu_tipo_documento,no_tipo_documento):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nu_tipo_documento)):
			filtro += " and nu_tipo_documento ="+nu_tipo_documento.strip()
		if not(self.validaCampo(no_tipo_documento)):
			filtro += " and no_tipo_documento like '%"+no_tipo_documento.strip().upper()+"%'"
		sql = "select * from tb001_tipo_documento where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		resultado = cursor.execute(sql)
		conn.commit()

		if cursor.arraysize == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			tipoDocumentosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				tipoDocumentosDict.append(l)
			return tipoDocumentosDict
					
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
