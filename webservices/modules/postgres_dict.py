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

	def insereOrgao(self,cnpj,nome,endereco,cidade,uf):
		conn = self.abreConexao()
		values = "("+str(cnpj)+",'"+nome+"','"+endereco+"','"+cidade+"','"+uf+"')"
		sql = "insert into tb002_orgao (nu_cnpj,no_orgao,no_endereco,no_cidade,no_uf) values "+values
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		resultado = cursor.execute(sql)
		conn.commit()
		#cursor.close()
		#return resultado
		return "Orgao inserido com sucesso!"

	def insereEmpregado(self,nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos,dependentes):
		conn = self.abreConexao()
		#values = "('"+nome+"','"+dt_contratacao+"','"+dt_nascimento+"','"+nu_matricula+"',"+str(rg)+","+str(cpf)+","+str(id_orgao)+",NULL)"
		#if dt_desligamento == None or dt_desligamento == '':
		#	values = values +",NULL)"
		#	dt_desligamento = 'Null'
		#if documentos == None:
		#	documentos = 'Null'
		#if dependentes == None:
		#	dependentes = 'Null'
		#sql = "insert into tb004_empregado (no_empregado, dt_contratacao,dt_nascimento,nu_matricula,nu_rg,nu_cpf,id_orgao,dt_desligamento) values "+values
		sql = "insert into tb004_empregado (no_empregado, dt_contratacao,id_orgao) values ('Empregado WEB','18/07/2013',2)"
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		resultado = cursor.execute(sql)
		conn.commit()
		#cursor.close()
		#return resultado
		return "empregado inserido com sucesso!"
		#return sql
		
	def insereDependente(self,nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,idEmpregado):
		conn = self.abreConexao()
		sql = "select id_empregado from tb004_empregado where id_empregado ="+str(idEmpregado)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		conn.commit()
		cursor.execute(sql)
		resultado = cursor
		if resultado.arraysize != 0:
			sql = "select id_tipo_vinculo from tb003_tipo_vinculo where id_tipo_vinculo ="+str(tp_vinculo)
			cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			cursor.execute(sql)
			conn.commit()
			if resultado.arraysize != 0:
				if rg == None and cpf == None and certidao == None:
					return "Insira um dos campos a seguir: rg, cpf,certidao"
				else:
					resultado = cursor.fetchone()
					id_tipo_vinculo = resultado['id_tipo_vinculo']
					values = "('"+nome+"','"+dt_nascimento+"',"+str(id_tipo_vinculo)+","+str(idEmpregado)
					if rg == None:
						values = values +",NULL"
					else:
						values = values +","+str(rg) 
					if cpf == None:
						values = values +",NULL"
					else:
						values = values +","+str(cpf) 
					if certidao == None:
						values = values +",NULL"
					else:
						values = values +","+str(certidao)
					values = values +")"
					sql = "insert into tb005_empregado_dependente (no_empregado_dependente,dt_nascimento,id_tipo_vinculo,id_empregado,nu_rg,nu_cpf,nu_certidao) values "+values
					cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
					cursor.execute(sql)
					conn.commit()
					return "Dependente inserido com sucesso!"
			else:
				return "Tipo de vinculo informado invalido!"
		else:
			return "Empregado invalido"
		
	def insereDocEmpregado(self,matricula,tp_documento, no_doc,file):
		conn = self.abreConexao()
		sql = "select * from tb004_empregado where nu_matricula = '"+matricula+"'"
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(sql)
		conn.commit()
		resultEmpregado = cursor
		if resultEmpregado.arraysize != 0:
			sql = "select id_tipo_documento from tb001_tipo_documento where no_tipo_documento = '"+tp_documento+"'"
			cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			cursor.execute(sql)
			resultado = cursor #verificar
			if resultado.arraysize != 0:
				resultEmpregado = resultEmpregado.fetchone()
				config = ConfigParser.ConfigParser()
				config.read("config.conf")
				if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
					os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"]))
				elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"])):
					os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"]))
				no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"])+'/'+no_doc
				self.upload_file(file,no_doc)
				sql = "insert into tb006_documento (no_documento,id_tipo_documento,id_empregado,dh_upload) values ('"+no_doc+"',"+1+","+str(resultEmpregado['id_empregado'])+",'"+str(datetime.datetime.now())+"')"
				cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
				cursor.execute(sql)
				conn.commit()
				return "Documento inserido!"
			else:
				return "Tipo de documento invalido!"
		else:
			return "Matricula invalida!"
				
	def insereDocDependente(self,empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
		conn = self.abreConexao()
		sql = "select * from tb004_empregado where nu_matricula = '"+empreg_matricula+"'"
		cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor1.execute(sql)
		conn.commit()
		resultEmpregado = cursor1
		if resultEmpregado.arraysize != 0:
			if rg_dependente == None and cpf_dependente == None and certidao_dependente == None:
					return "Insira um dos campos a seguir: rg, cpf,certidao"
			else:
				filtro = ''
				if rg_dependente == None:
					pass
				else:
					filtro = filtro + "and nu_rg = "+str(rg_dependente) 
				if cpf_dependente == None:
					pass
				else:
					filtro = filtro + "and nu_cpf = "+str(cpf_dependente) 
				if certidao_dependente == None:
					pass
				else:
					filtro = filtro + "and nu_certidao = "+str(certidao_dependente) 
				sql = "select * from tb005_empregado_dependente where 1=1 "+filtro
				cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
				cursor2.execute(sql)
				conn.commit()
				resultDependente = cursor2
				if resultDependente.arraysize != 0:
					sql = "select id_tipo_documento from tb001_tipo_documento where id_tipo_documento = '"+tp_documento+"'"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
					cursor.execute(sql)
					conn.commit()
					resultado = cursor
					if resultado.arraysize != 0:
						resultEmpregado = resultEmpregado.fetchone()
						resultDependente = resultDependente.fetchone()
						config = ConfigParser.ConfigParser()
						config.read("config.conf")
						if not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"]))
						elif not os.path.exists(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"])):
							os.makedirs(config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"]))
						no_doc = config.get("path", "filePath")+str(resultEmpregado["id_orgao"])+'/'+str(resultEmpregado["nu_matricula"])+'/'+no_doc
						self.upload_file(file,no_doc)
						sql = "insert into tb006_documento (id_tipo_documento,id_empregado,id_empregado_dependente,no_documento,dh_upload) values("+str(tp_documento)+","+str(resultEmpregado["id_empregado"])+","+str(resultDependente["id_empregado_dependente"])+",'"+no_doc+"','"+str(datetime.datetime.now())+"')"
						cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
		if nome == '' and endereco == '' and cidade == '' and uf == '':
			print "Favor inserir algum parametro para a consulta!"
		else:
			filtro = ''
			if nome != '' and nome != None:
				filtro = "and no_orgao like '%"+nome+"%'"
			if endereco != '' and endereco != None:
				filtro = "and no_endereco like '%"+endereco+"%'"
			if cidade != '' and cidade != None:
				filtro = "and no_cidade like '%"+cidade+"%'"
			if uf != '' and uf != None:
				filtro = "and no_uf like '%"+uf+"%'"
			sql = "select * from tb002_orgao where 1=1 "+filtro
			print sql
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
			
		if nome != '':
			nome = "AND no_empregado = '"+nome+"'"
			
		if dt_contratacao != '':
			dt_contratacao = "AND dt_contratacao = '"+dt_contratacao+"'"
			
		if dt_desligamento != '':
			dt_desligamento = "AND dt_desligamento = '"+dt_desligamento+"'"
			
		if dt_nascimento != '':
			dt_nascimento = "AND dt_nascimento = '"+dt_nascimento+"'"
			
		if nu_matricula != '':
			nu_matricula = "AND nu_matricula = '"+nu_matricula+"'"
			
		sql = "select * from tb004_empregado where 1=1 "+nome+dt_contratacao+dt_desligamento+dt_nascimento+nu_matricula
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
		if nomeDependente != '':
			nomeDependente = "AND no_empregado_dependente = '"+nomeDependente+"'"
			
		if nomeEmpregado != '':
			nomeEmpregado = "AND no_empregado = '"+nomeEmpregado+"'"
			
		if matricula != '':
			nome = "AND nu_matricula = '"+matricula+"'"
			
		if dt_nascimento != '':
			dt_nascimento = "AND dt_nascimento = '"+dt_nascimento+"'"
			
		if tp_vinculo != '':
			tp_vinculo = "AND tp_vinculo = '"+tp_vinculo+"'"
		sql = "select * from tb005_empregado_dependente join tb004_empregado on tb004_empregado.id_empregado =  tb005_empregado_dependente.id_empregado where 1=1 "+nomeDependente+nomeEmpregado+matricula+dt_nascimento+tp_vinculo
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
		
	def retornaDocEmpregado (matricula,id_empregado):
		print 'Temporario'
		
	def retornaDocDependente (id_dependente,rg,cpf,certidao):
		print 'Temporario'
					
	def upload_file(self,file, name):
		out = open(name, 'wb')
		out.write(str(file.decode('base64')))
		out.close()
		

	#insereOrgao()
	#dict_cur.close()
	#insereEmpregado()
	#insereEmpregado()
	#servidores = listaEmpregados(id_empregado = 7)

	#for servidor in servidores:
	#	print servidor['no_empregado']

	#dict_cur.close()
	#conn.close()
