import psycopg2
import psycopg2.extras
import ConfigParser
import datetime
import os
from threading import Lock

class Model:

	def abreConexao(self):
		conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
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
			sql = "select * from tb002_orgao where nu_cnpj ="+cnpj
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			if cursor.rowcount != 0 :
				return "Orgao de cnpj '"+cnpj+"' ja existe."
			else:
				values = "("+str(cnpj)+",'"+nome.strip().upper()+"','"+endereco.strip().upper()+"','"+cidade.strip().upper()+"','"+uf.strip().upper()+"')"
				sql = "insert into tb002_orgao (nu_cnpj,no_orgao,no_endereco,no_cidade,no_uf) values "+values
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				resultado = cursor.execute(sql)
				conn.commit()
				#cursor.close()
				#return resultado
				return "Orgao inserido com sucesso."

	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao,documentos):
		if self.validaCampo(str(nome))  or self.validaCampo(str(dt_contratacao)) or self.validaCampo(str(dt_nascimento)) or self.validaCampo(str(nu_matricula)) or self.validaCampo(str(rg)) or self.validaCampo(str(cpf)) or self.validaCampo(str(cnpj_orgao)):
			return "Favor informar os seguintes campos: Nome, Data de Contratacao, Data de Nascimento, Matricula, RG, CPF e ID da Empresa."
		else:
			conn = self.abreConexao()
			sql = "select id_orgao from tb002_orgao where nu_cnpj ="+str(cnpj_orgao)
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			cursor.execute(sql)
			conn.commit()
			if cursor.rowcount == 0 :
				return "O orgao informando nao e valido."
			else:
				
				sql = "select * from tb004_empregado where nu_matricula ='"+nu_matricula.strip().upper()+"' or nu_rg="+str(rg)+" or nu_cpf="+str(cpf)
				cursorEmpregado = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursorEmpregado.execute(sql)
				conn.commit()
				
				if cursorEmpregado.rowcount != 0 :
					return "O empregado informado ja existe"
				else:
					orgao = cursor.fetchone()
					values = "('"+nome.strip().upper()+"','"+dt_contratacao+"','"+dt_nascimento+"','"+nu_matricula.strip().upper()+"',"+str(rg)+","+str(cpf)+","+str(orgao['id_orgao'])
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
				if cursor.rowcount != 0:
					resultado = cursor.fetchone()
					id_tipo_vinculo = resultado['id_tipo_vinculo']
					filtro = ''
					if not self.validaCampo(str(rg)):
						filtro += ' nu_rg = '+rg
					if not self.validaCampo(str(cpf)):
						if filtro == '':
							filtro += ' nu_cpf = '+cpf
						else:
							filtro += ' or nu_cpf = '+cpf
					if not self.validaCampo(str(certidao)):
						if filtro == '':
							filtro += ' nu_certidao = '+certidao
						else:
							filtro += ' or nu_certidao = '+certidao
					sql = "select id_empregado_dependente from tb005_empregado_dependente where 1=1 and ("+filtro+")"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					if cursor.rowcount == 0:
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
						return "Dependente ja existe!"
				else:
					return "Tipo de vinculo informado invalido!"
			else:
				return "O responsavel informado nao foi encontrado."
		
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
			if resultEmpregado.rowcount != 0:
				sql = "select id_tipo_documento from tb001_tipo_documento where id_tipo_documento = " + tp_documento
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursor.execute(sql)
				resultado = cursor #verificar
				if resultado.rowcount != 0:
					resultEmpregado = resultEmpregado.fetchone()
					config = ConfigParser.ConfigParser()
					config.read("config.conf")
					lock = Lock()
					lock.acquire()
					try:
						if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"]))
						elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"]))
						l = True
						while l == True:
							if os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])):
								l = False
								lock.release()
							else:
								l = True
						
					except OSError as ex:
						return "Erro na criacao dos diretorios: ", ex
						lock.release()
						
					else:
						no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+no_doc
						self.upload_file(file,no_doc)
						sql = "insert into tb006_documento_empregado (no_documento,id_tipo_documento,id_empregado,dh_upload) values ('"+no_doc+"',"+tp_documento+","+str(resultEmpregado['id_empregado'])+",'"+str(datetime.datetime.now())+"')"
						cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
						cursor.execute(sql)
						conn.commit()
						return "Documento inserido!"
				else:
					return "O tipo de documento informado nao existe"
			else:
				return "O Empregado informado nao foi encontrado!"
				
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
			if resultEmpregado.rowcount != 0:
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
				if resultDependente.rowcount != 0:
					sql = "select id_tipo_documento from tb001_tipo_documento where id_tipo_documento = "+str(tp_documento)
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					resultado = cursor
					if resultado.rowcount != 0:
						resultEmpregado = resultEmpregado.fetchone()
						resultDependente = resultDependente.fetchone()
						config = ConfigParser.ConfigParser()
						config.read("config.conf")
						lock = Lock()
						lock.acquire()
						try:
							if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
								os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
							elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])):
								os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
							elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"])):
								os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"]))
							l = True
							while l == True:
								if os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"])):
									l = False
									lock.release()
								else:
									l = True
						
						except OSError as ex:
							return "Erro na criacao dos diretorios: ", ex
							lock.release()

						else:
							no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["id_empregado"])+'/'+str(resultDependente["id_empregado_dependente"])+'/'+no_doc
							self.upload_file(file,no_doc)
							sql = "insert into tb007_documento_dependente (id_tipo_documento,id_empregado_dependente,no_documento,dh_upload) values("+str(tp_documento)+","+str(resultDependente["id_empregado_dependente"])+",'"+no_doc+"','"+str(datetime.datetime.now())+"')"
							cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
							cursor.execute(sql)
							conn.commit()
							return "Documento inserido!"
					else:
						return "Tipo de documento invalido!"
				else:
					return "O dependente informado nao foi encontrado!"
			else:
				return "O responsavel informado nao foi encontrado!"
					
	def listaOrgaos(self,cnpj="",nome='',endereco='',cidade='',uf=''):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(cnpj)):
			filtro += " and nu_cnpj::varchar like '%"+cnpj+"%'"
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

		if cursor.rowcount == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			orgaosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				orgaosDict.append(l)
			return orgaosDict
		
	def listaEmpregados(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf, cnpj_orgao):
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
			
		if not(self.validaCampo(rg)):
			filtro += " AND nu_rg ="+rg.strip()
			
		if not(self.validaCampo(cpf)):
			filtro += " AND nu_cpf ="+cpf.strip()
			
		if not(self.validaCampo(cnpj_orgao)):
			join = " join tb002_orgao on tb002_orgao.id_orgao = tb004_empregado.id_orgao "
			filtro += " AND tb002_orgao.nu_cnpj ="+cnpj_orgao.strip()
		else:
			join = ''
			
		sql = "select * from tb004_empregado "+join+"where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cursor.execute(sql)
		conn.commit()
		if cursor.rowcount == 0:
			return "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			empregadosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				empregadosDict.append(l)
			return empregadosDict
		
	def listaDependentes(self,nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo,rg,cpf,certidao):
		conn = self.abreConexao()
		filtro = ''
		if not(self.validaCampo(nomeDependente)):
			filtro += " AND no_empregado_dependente like '%"+nomeDependente.strip().upper()+"%'"
			
		if not(self.validaCampo(nomeEmpregado)):
			filtro += " AND no_empregado like '%"+nomeEmpregado.strip().upper()+"%'"
			
		if not(self.validaCampo(matricula)):
			filtro += " AND nu_matricula like '%"+matricula.strip().upper()+"%'"
			
		if not(self.validaCampo(dt_nascimento)):
			filtro += " AND tb005_empregado_dependente.dt_nascimento = '"+dt_nascimento.strip()+"'"
			
		if not(self.validaCampo(tp_vinculo)):
			filtro += " AND tb005_empregado_dependente.id_tipo_vinculo = "+tp_vinculo.strip()
			
		if not(self.validaCampo(rg)):
			filtro += " AND tb005_empregado_dependente.nu_rg ="+rg.strip()
			
		if not(self.validaCampo(cpf)):
			filtro += " AND tb005_empregado_dependente.nu_cpf ="+cpf.strip()
			
		if not(self.validaCampo(certidao)):
			filtro += " AND nu_certidao ="+certidao.strip()
			
		sql = "select tb005_empregado_dependente.* from tb005_empregado_dependente join tb004_empregado on tb004_empregado.id_empregado =  tb005_empregado_dependente.id_empregado where 1=1 "+filtro
		cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cursor.execute(sql)
		conn.commit()
		
		if cursor.rowcount == 0:
			return "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
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
			sql+=	"join tb006_documento_empregado on tb006_documento_empregado.id_empregado = tb004_empregado.id_empregado "
			sql+=	"join tb001_tipo_documento on tb001_tipo_documento.id_tipo_documento = tb006_documento_empregado.id_tipo_documento "
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
			sql+=	"join tb007_documento_dependente on tb007_documento_dependente.id_empregado_dependente = tb005_empregado_dependente.id_empregado_dependente "
			sql+=	"join tb001_tipo_documento on tb001_tipo_documento.id_tipo_documento = tb007_documento_dependente.id_tipo_documento "
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

		if cursor.rowcount == 0:
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

		if cursor.rowcount == 0:
			print "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			tipoDocumentosDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				tipoDocumentosDict.append(l)
			return tipoDocumentosDict
			
	def empregadosAtivos (self,cnpj_orgao):
		conn = self.abreConexao()
		if (not self.validaCampo(str(cnpj_orgao))):
			
			sql="select * from tb002_orgao where nu_cnpj="+str(cnpj_orgao)
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit
			if cursor.rowcount == 0:
				return 'O cnpj informado nao foi encontrado.'
			else:			
				sql="select"
				sql+="	tb002_orgao.id_orgao, "
				sql+="	count(id_empregado) as empregados_ativos "
				sql+="from tb002_orgao "
				sql+="	join tb004_empregado on tb004_empregado.id_orgao = tb002_orgao.id_orgao "
				sql+="	where dt_desligamento is null and nu_cnpj="+str(cnpj_orgao)
				sql+="	group by tb002_orgao.id_orgao, no_orgao "
				sql+="order by id_orgao "
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				resultado = cursor.execute(sql)
				conn.commit()
		else:
			sql="select"
			sql+="	tb002_orgao.id_orgao, "
			sql+="	count(id_empregado) as empregados_ativos "
			sql+="from tb002_orgao "
			sql+="	join tb004_empregado on tb004_empregado.id_orgao = tb002_orgao.id_orgao "
			sql+="	where dt_desligamento is null "
			sql+="	group by tb002_orgao.id_orgao, no_orgao "
			sql+="order by id_orgao "
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit()
			
			

			
		if cursor.rowcount == 0:
			return "Nenhum dado econtrado. Verifique os parametros de busca."
		else:
			estatisticaDict=[]
			for row in cursor:
				l = dict()
				for collumn in row:
					l[collumn]=row[collumn]
				estatisticaDict.append(l)
			return estatisticaDict
			
			
	def desligaEmpregado(self,nu_matricula,dt_desligamento):
		if self.validaCampo(nu_matricula) and self.validaCampo(dt_desligamento):
			return 'Favor informar a matricula do empregado e a data de desligamento.'
		else:
			conn = self.abreConexao()
			sql="select * from tb004_empregado where nu_matricula = '"+nu_matricula+"'"
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit()
			if cursor.rowcount == 0:
				return 'O empregado nao foi encontrado.'
			else:
				empregado = cursor.fetchone()
				if datetime.datetime.strptime(dt_desligamento,'%d-%m-%Y').date() < datetime.datetime.strptime(str(empregado['dt_contratacao']),'%Y-%m-%d').date():
					return 'Data de desligamento invalida. Informe no formato d-m-yyyy.'
				else:
					sql="update tb004_empregado set dt_desligamento ='"+datetime.datetime.strftime(datetime.datetime.strptime(dt_desligamento,'%d-%m-%Y').date(),'%Y-%m-%d')+"' where nu_matricula ='"+nu_matricula+"'"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					resultado = cursor.execute(sql)
					conn.commit()
					return 'Empregado desligado com sucesso.'
					
	def removeDependente(self,nu_cpf):
		if self.validaCampo(nu_cpf):
			return 'Favor informar o CPF do dependente'
		else:
			conn = self.abreConexao()
			sql= "select * from tb005_empregado_dependente "
			sql+="join tb007_documento_dependente on tb007_documento_dependente.id_empregado_dependente = tb005_empregado_dependente.id_empregado_dependente "
			sql+="where nu_cpf = "+nu_cpf
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			resultado = cursor.execute(sql)
			conn.commit()
			if cursor.rowcount == 0:
				return 'O dependente nao foi encontrado.'
			else:
				sql=""
				for row in cursor:
					sql+="delete from tb007_documento_dependente where id_empregado_dependente = "+str(row['id_empregado_dependente'])+";"
					os.remove(row['no_documento'])
				sql+="delete from tb005_empregado_dependente where nu_cpf = "+nu_cpf+";"
				cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cursor.execute(sql)
				conn.commit()
				return 'Dependente removido com sucesso.'
			
		
					
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
