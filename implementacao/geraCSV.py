import sys
import os
import commands
from random import *
import datetime
from array import array
import csv
import psycopg2
import psycopg2.extras
from pymongo import Connection
from bson import ObjectId
import shutil, errno
import mongo

Model = mongo.Model()

path_docs = '/home/eu/documentos_carga'
orgaos = 10
empregados_por_orgao = 100
dependente_por_empregado = 2
documento_por_empregado = 5
documento_por_dependente = 2
path_csv_p = '/home/eu/jmeter test plans/cargaPostgres'
path_csv = '/home/eu/jmeter test plans/cargaMongo'

def copyanything (src, dst):
	try:
		shutil.copytree(src,dst)
	except OSError as exc:
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src,dst)
		else: raise

def geraNum (l):
	n=0
	s=[]
	while n < l:
		s.append(str(randint(0,9)))
		n+=1
	return ''.join(s)
	
def geraDataContratacao (dt_nascimento):
	dt_minima = datetime.date.toordinal(dt_nascimento) + 6570
	dt_maxima = datetime.date.toordinal(dt_nascimento) + 21900
	n = randint(dt_minima,dt_maxima)
	while datetime.date.fromordinal(n) > datetime.date.today():
		n = randint(dt_minima,dt_maxima)
	s = datetime.date.fromordinal(n)
	return s
	
def geraDataNascimento ():
	n = randint(6570,21900)
	s = datetime.date.fromordinal(datetime.date.toordinal(datetime.date.today()) - n)
	return s
	
def geraDataDesligamento (dt_contratacao,dt_nascimento):

	dt_minima = datetime.date.toordinal(dt_contratacao)
	dt_maxima = datetime.date.toordinal(dt_contratacao) + 10950
	n = randint(dt_minima,dt_maxima)
	while (n > datetime.date.today().toordinal()) or ((n - datetime.date.toordinal(dt_nascimento)) > 21900):
		n = randint(dt_minima,dt_maxima)
	x = []
	x.append(0)
	s = datetime.date.fromordinal(n)
	x.append(s)
	s = choice(x)
	if s == 0:
		return ''
	else:
		return str(s)

def carregaOrgaos():
	n = 0
	with open (path_csv + '/orgaos.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		while n < orgaos:
			cnpj = geraNum(14)
			spamwriter.writerow([cnpj,'orgao '+str(n),'endereco orgao '+str(n),'cidade orgao '+str(n),'df'])
			Model.insereOrgao(cnpj,'orgao '+str(n),'endereco orgao '+str(n),'cidade orgao '+str(n),'df')
			n+=1
	copyanything(path_csv + '/orgaos.csv',path_csv_p + '/orgaos.csv')

def carregaEmpregados():
	orgaos = Model.listaOrgaos('','','','','')
	with open (path_csv + '/empregados.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for orgao in orgaos:
			n=0	
			while n < empregados_por_orgao:
				dt_nascimento = geraDataNascimento()
				dt_contratacao = geraDataContratacao(dt_nascimento)
				dt_desligamento = geraDataDesligamento(dt_contratacao,dt_nascimento)
				nome = 'nome empregado '+str(n)
				matricula = 'M'+geraNum(6)
				rg = geraNum(7)
				cpf = geraNum(11)
				spamwriter.writerow([nome,str(dt_contratacao),str(dt_desligamento),str(dt_nascimento),matricula,rg,cpf,orgao['nu_cnpj'],''])
				Model.insereEmpregado(nome,str(dt_contratacao),str(dt_desligamento),str(dt_nascimento),matricula,rg,cpf,orgao['nu_cnpj'],'')
				n+=1
	copyanything(path_csv + '/empregados.csv',path_csv_p + '/empregados.csv')
	
def carregaDependentes():
	empregados = Model.listaEmpregados('','','','','','','','')
	with open (path_csv + '/dependentes.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		with open (path_csv_p + '/dependentes.csv', 'wb') as csvfilep:
			spamwriterp = csv.writer(csvfilep,delimiter=';', quoting=csv.QUOTE_MINIMAL)
			for empregado in empregados:
				n=0
				while n < dependente_por_empregado:
					vinculos = Model.listaVinculos('','')
					conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
					sql="select * from tb003_tipo_vinculo where no_tipo_vinculo = '"+vinculos[n]["no_tipo_vinculo"]+"'"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					x = cursor.fetchone()
					dt_nascimento = geraDataNascimento()
					nome = 'nome dependente'+str(n)+' empregado '+str(empregado['id_empregado'])
					rg = geraNum(7)
					cpf = geraNum(11)
					certidao = geraNum(11)
					spamwriter.writerow([nome,rg,cpf,certidao,str(dt_nascimento),vinculos[n]["id_tipo_vinculo"],'',empregado['nu_matricula']])
					spamwriterp.writerow([nome,rg,cpf,certidao,str(dt_nascimento),x["id_tipo_vinculo"],'',empregado['nu_matricula']])
					Model.insereDependente(nome,rg,cpf,certidao,str(dt_nascimento),vinculos[n]["id_tipo_vinculo"],'',empregado['nu_matricula'])
					n+=1
					#copyanything(path_csv + '/dependentes.csv',path_csv_p + '/dependentes.csv')

def carregaDocEmpregado():
	empregados = Model.listaEmpregados('','','','','','','','')
	docs = os.listdir(path_docs)
	len_docs = len(docs)
	with open (path_csv + '/docEmpregados.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		with open (path_csv_p + '/docEmpregados.csv', 'wb') as csvfilep:
			spamwriterp = csv.writer(csvfilep,delimiter=';', quoting=csv.QUOTE_MINIMAL)
			for empregado in empregados:
				l = 0
				n=0
				while n < documento_por_empregado:
					if l < len_docs:
						l+=1
					else:
						l = 0
					file=open(path_docs+'/'+docs[l], 'rb')
					data=file.read()
					tipo_documentos = Model.listaTipoDocumentos('','')
					conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
					sql="select * from tb001_tipo_documento where no_tipo_documento = '"+tipo_documentos[n]['no_tipo_documento']+"'"
					cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
					cursor.execute(sql)
					conn.commit()
					x = cursor.fetchone()
					spamwriter.writerow([empregado['nu_matricula'],str(tipo_documentos[n]['id_tipo_documento']), str(n)+docs[l],''+data.encode('base64')+''])
					spamwriterp.writerow([empregado['nu_matricula'],str(x['id_tipo_documento']), str(n)+docs[l],''+data.encode('base64')+''])
					#Model.insereDocEmpregado(empregado['nu_matricula'],str(tipo_documentos[n]['id_tipo_documento']), str(n)+docs[l],data.encode('base64'))
					file.close()
					n+=1

def carregaDocDependente():
	empregados = Model.listaEmpregados('','','','','','','','')
	docs = os.listdir(path_docs)
	len_docs = len(docs)
	with open (path_csv + '/docDependentes.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		with open (path_csv_p + '/docDependentes.csv', 'wb') as csvfilep:
			spamwriterp = csv.writer(csvfilep,delimiter=';', quoting=csv.QUOTE_MINIMAL)
			for empregado in empregados:
				dependentes = Model.listaDependentes('','',empregado['nu_matricula'],'','','','','')
				for dependente in dependentes:
					l = 0
					n=0	
					while n < documento_por_dependente:
						if l < len_docs:
							l+=1
						else:
							l = 0
						file=open(path_docs+'/'+docs[l], 'rb')
						data=file.read()
						tipo_documentos = Model.listaTipoDocumentos('','')
						conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
						sql="select * from tb001_tipo_documento where no_tipo_documento = '"+tipo_documentos[n]['no_tipo_documento']+"'"
						cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
						cursor.execute(sql)
						conn.commit()
						x = cursor.fetchone()
						spamwriter.writerow([empregado['nu_matricula'], dependente['nu_rg'],dependente['nu_cpf'],'',tipo_documentos[n]['id_tipo_documento'], str(n)+docs[l],''+data.encode('base64')+''])
						spamwriterp.writerow([empregado['nu_matricula'], dependente['nu_rg'],dependente['nu_cpf'],'',x['id_tipo_documento'], str(n)+docs[l],''+data.encode('base64')+''])
						#Model.insereDocDependente(empregado['nu_matricula'], dependente['nu_rg'],dependente['nu_cpf'],'',tipo_documentos[n]['id_tipo_documento'], str(n)+docs[l],data.encode('base64'))
						file.close()
						n+=1
					
def geraListaDesligamento():
	conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
	sql = "select nu_matricula, now()::date as dt_desligamento from tb004_empregado where dt_desligamento is null limit 250; "
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute(sql)
	conn.commit()
	with open (path_csv + '/lista_desligamento.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for row in cursor:
			spamwriter.writerow([row['nu_matricula'], row['dt_desligamento']])
	copyanything(path_csv + '/lista_desligamento.csv',path_csv_p + '/lista_desligamento.csv')
	

def geraListaRemoveDependente():
	conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
	sql = "select nu_cpf from tb005_empregado_dependente limit 250; "
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute(sql)
	conn.commit()
	with open (path_csv + '/remove_dependente.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for row in cursor:
			spamwriter.writerow([row['nu_cpf']])
	copyanything(path_csv + '/remove_dependente.csv',path_csv_p + '/remove_dependente.csv')
					
def main():
	conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="31061210")
	db = Model.conectaMongo()
	db.drop_collection('empregados')
	db.drop_collection('dependentes')
	db.drop_collection('orgaos')
	sql = "delete from tb007_documento_dependente; "
	sql += "delete from tb006_documento_empregado; "
	sql += "delete from tb005_empregado_dependente; "
	sql += "delete from tb004_empregado; "
	sql += "delete from tb002_orgao; "
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute(sql)
	conn.commit()
	carregaOrgaos()
	carregaEmpregados()
	carregaDependentes()
	carregaDocEmpregado()
	carregaDocDependente()
	#consultaOrgaos()
	db.drop_collection('empregados')
	db.drop_collection('dependentes')
	db.drop_collection('orgaos')
	sql = "delete from tb007_documento_dependente; "
	sql += "delete from tb006_documento_empregado; "
	sql += "delete from tb005_empregado_dependente; "
	sql += "delete from tb004_empregado; "
	sql += "delete from tb002_orgao; "
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute(sql)
	conn.commit()
	print "Os arquivos csv foram criados."

		
if __name__=="__main__":
	main()
