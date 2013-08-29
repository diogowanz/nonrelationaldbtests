import sys
import os
import commands
from random import *
import datetime
from array import array
import csv

#db = __import__(sys.argv[1])
#import postgres_dict
import mongo

#Model = db.Model()
#Model = postgres_dict.Model()
Model = mongo.Model()

path_docs = '/home/wanzeller/documentos_carga'
orgaos = 10
empregados_por_orgao = 1
dependente_por_empregado = 1
documento_por_empregado = 2
documento_por_dependente = 2


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
	with open ('orgaos.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		while n < orgaos:
			spamwriter.writerow([geraNum(14),'orgao '+str(n),'endereco orgao '+str(n),'cidade orgao '+str(n),'df'])
			Model.insereOrgao(geraNum(14),'orgao '+str(n),'endereco orgao '+str(n),'cidade orgao '+str(n),'df')
			n+=1

def carregaEmpregados():
	orgaos = Model.listaOrgaos(nome='orgao')
	with open ('empregados.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for orgao in orgaos:
			n=0	
			while n < empregados_por_orgao:
				dt_nascimento = geraDataNascimento()
				dt_contratacao = geraDataContratacao(dt_nascimento)
				dt_desligamento = geraDataDesligamento(dt_contratacao,dt_nascimento)
				spamwriter.writerow(['nome empregado '+str(n),str(dt_contratacao),str(dt_desligamento),str(dt_nascimento),'M'+geraNum(6),geraNum(7),geraNum(11),orgao['id_orgao'],''])
				Model.insereEmpregado('nome empregado '+str(n),str(dt_contratacao),str(dt_desligamento),str(dt_nascimento),'M'+geraNum(6),geraNum(7),geraNum(11),orgao['id_orgao'],'')
				n+=1
	
def carregaDependentes():
	empregados = Model.listaEmpregados()
	with open ('dependentes.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for empregado in empregados:
			n=0
			while n < dependente_por_empregado:
				vinculos = Model.listaVinculos('','')
				dt_nascimento = geraDataNascimento()
				spamwriter.writerow(['nome dependente'+str(n)+' empregado '+str(empregado['id_empregado']),geraNum(7),geraNum(11),geraNum(11),str(dt_nascimento),vinculos[n]["id_tipo_vinculo"],'',empregado['nu_matricula']])
				Model.insereDependente('nome dependente'+str(n)+' empregado '+str(empregado['id_empregado']),geraNum(7),geraNum(11),geraNum(11),str(dt_nascimento),vinculos[n]["id_tipo_vinculo"],'',empregado['nu_matricula'])
				n+=1

def carregaDocEmpregado():
	empregados = Model.listaEmpregados()
	docs = os.listdir(path_docs)
	len_docs = len(docs)
	with open ('docEmpregados.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
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
				spamwriter.writerow([empregado['nu_matricula'],str(tipo_documentos[n]['id_tipo_documento']), str(n)+docs[l],data.encode('base64')])
				Model.insereDocEmpregado(empregado['nu_matricula'],str(tipo_documentos[n]['id_tipo_documento']), str(n)+docs[l],data.encode('base64'))
				file.close()
				n+=1

def carregaDocDependente():
	empregados = Model.listaEmpregados()
	docs = os.listdir(path_docs)
	len_docs = len(docs)
	with open ('docDependentes.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,delimiter=';', quoting=csv.QUOTE_MINIMAL)
		for empregado in empregados:
			dependentes = Model.listaDependentes('','',empregado['nu_matricula'],'','')
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
					spamwriter.writerow([empregado['nu_matricula'], dependente['nu_rg'],dependente['nu_cpf'],'',tipo_documentos[n]['id_tipo_documento'], str(n)+docs[l],data.encode('base64')])
					Model.insereDocDependente(empregado['nu_matricula'], dependente['nu_rg'],dependente['nu_cpf'],'',tipo_documentos[n]['id_tipo_documento'], str(n)+docs[l],data.encode('base64'))
					file.close()
					n+=1
