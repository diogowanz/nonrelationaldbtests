# coding: utf8
# tente algo como
def index(): return dict(message="hello from sample.py")

#import mongo
#model = local_import('mongo')
model = local_import('postgres_dict')


from gluon.tools import Service
service = Service(globals())

Model = model.Model()
    
@service.xmlrpc
@service.soap('insereOrgao',returns={'s':str},args={'cnpj':str, 'nome':str, 'endereco':str, 'cidade':str, 'uf':str})
def insereOrgao(cnpj,nome,endereco,cidade,uf):
    s = Model.insereOrgao(cnpj,nome,endereco,cidade,uf)
    return s
    
@service.xmlrpc
@service.soap('insereEmpregado',returns={'s':str},args={'nome':str, 'dt_contratacao':str, 'dt_desligamento':str, 'dt_nascimento':str, 'nu_matricula':str, 'rg':str, 'cpf':str, 'cnpj_orgao':str, 'documentos':str})
def insereEmpregado(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao,documentos):
    s = Model.insereEmpregado(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao,documentos)
    return s
    
@service.xmlrpc
@service.soap('insereDependente',returns={'s':str},args={'nome':str, 'rg':str, 'cpf':str, 'certidao':str, 'dt_nascimento':str, 'tp_vinculo':str, 'documentos':str, 'nu_matricula_responsavel':str})
def insereDependente(nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,nu_matricula_responsavel):
    s = Model.insereDependente(nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,nu_matricula_responsavel)
    return s
    
@service.xmlrpc
@service.soap('insereDocEmpregado',returns={'s':str},args={'matricula':str, 'tp_documento':str, 'no_doc':str, 'file':str})
def insereDocEmpregado(matricula,tp_documento, no_doc,file):
    s = Model.insereDocEmpregado(matricula,tp_documento, no_doc,file)
    return s

@service.xmlrpc
@service.soap('insereDocDependente',returns={'s':str},args={'empreg_matricula':str, 'rg_dependente':str, 'cpf_dependente':str, 'certidao_dependente':str,'tp_documento':str,'no_doc':str,'file':str})
def insereDocDependente(empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file):
    s = Model.insereDocDependente(empreg_matricula, rg_dependente,cpf_dependente,certidao_dependente,tp_documento, no_doc,file)
    return s

@service.xmlrpc
@service.soap('listaOrgao',returns={ 'orgaos': [{'orgao': {'id_orgao':str,'nu_cnpj':str,'no_orgao':str,'no_endereco': str,'no_cidade':str,'no_uf':str}}]},
args={'cnpj':str, 'nome':str, 'endereco':str, 'cidade':str, 'uf':str})
def listaOrgaos(cnpj,nome,endereco,cidade,uf):
	orgaos = Model.listaOrgaos(cnpj,nome,endereco,cidade,uf)
	y = []
	for orgao in orgaos:
		x = dict()
		x['orgao'] = orgao
		y.append(x)
	orgaos = y
	return orgaos

@service.xmlrpc
@service.soap('listaEmpregados',returns={ 'empregados': [{'empregado': {'id_empregado':str,'no_empregado':str,'dt_contratacao':str,'dt_desligamento':str,'dt_nascimento':str,'nu_matricula':str,'nu_rg':str,'nu_cpf':str,'id_orgao':str,'Documentos':str,'Dependentes':str}}]},
args={'nome':str, 'dt_contratacao':str, 'dt_desligamento':str, 'dt_nascimento':str, 'nu_matricula':str,'rg':str,'cpf':str,'cnpj_orgao':str})
def listaEmpregados(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao):
	empregados = Model.listaEmpregados(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,cnpj_orgao)
	y = []
	for empregado in empregados:
		x = dict()
		x['empregado'] = empregado
		y.append(x)
	empregados = y
	return empregados

@service.xmlrpc
@service.soap('listaDependentes',returns={ 'dependentes': [{'dependente': {'id_empregado_dependente':str,'no_empregado_dependente':str,'nu_rg':str,'nu_cpf':str,'nu_certidao':str,'dt_nascimento':str,'tp_vinculo':str,'Documentos':str}}]},
args={'nomeEmpregado':str, 'nomeDependente':str, 'matricula':str, 'dt_nascimento':str, 'tp_vinculo':str,'rg':str,'cpf':str,'certidao':str})
def listaDependentes(nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo,rg,cpf,certidao):
	dependentes = Model.listaDependentes(nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo,rg,cpf,certidao)
	y = []
	for dependente in dependentes:
		x = dict()
		x['dependente'] = dependente
		y.append(x)
	dependentes = y
	return dependentes
	
@service.xmlrpc
@service.soap('retornaDocEmpregado',returns={ 'documentos': [{'documento': {'tp_documento':str, 'dh_updload':str,'no_documento':str,'file':str}}]},
args={'nu_matricula':str, 'no_documento':str, 'tp_documento':str})
def retornaDocEmpregado (nu_matricula,no_documento,tp_documento):
	documentos = Model.retornaDocEmpregado(nu_matricula,no_documento,tp_documento)
	y = []
	for documento in documentos:
		x = dict()
		x['documento'] = documento
		y.append(x)
	documentos = y
	return documentos
	
@service.xmlrpc
@service.soap('retornaDocDependente',returns={ 'documentos': [{'documento': {'tp_documento':str, 'dh_updload':str,'no_documento':str,'file':str}}]},
args={'nu_rg':str, 'nu_cpf':str, 'nu_certidao':str, 'no_documento':str, 'tp_documento':str})
def retornaDocDependente (nu_rg,nu_cpf,nu_certidao, no_documento, tp_documento):
	documentos = Model.retornaDocDependente(nu_rg,nu_cpf,nu_certidao, no_documento, tp_documento)
	y = []
	for documento in documentos:
		x = dict()
		x['documento'] = documento
		y.append(x)
	documentos = y
	return documentos	

@service.xmlrpc
@service.soap('listaVinculos',returns={ 'vinculos': [{'vinculo': {'id_tipo_vinculo':str,'no_tipo_vinculo':str}}]},
args={'nu_tipo_vinculo':str, 'no_tipo_vinculo':str})
def listaVinculos (nu_tipo_vinculo,no_tipo_vinculo):
	vinculos = Model.listaVinculos(nu_tipo_vinculo,no_tipo_vinculo)
	y = []
	for vinculo in vinculos:
		x = dict()
		x['vinculo'] = vinculo
		y.append(x)
	vinculos = y
	return vinculos
	
@service.xmlrpc
@service.soap('listaTipoDocumentos',returns={ 'tipos': [{'tipo': {'id_tipo_documento':str,'no_tipo_documento':str}}]},
args={'nu_tipo_documento':str, 'no_tipo_documento':str})
def listaTipoDocumentos (nu_tipo_documento,no_tipo_documento):
	tipos = Model.listaTipoDocumentos(nu_tipo_documento,no_tipo_documento)
	y = []
	for tipo in tipos:
		x = dict()
		x['tipo'] = tipo
		y.append(x)
	tipos = y
	return tipos

@service.xmlrpc
@service.soap('empregadosAtivos',returns={ 'empregadosAtivos': [{'orgao': {'id_orgao':str,'qt_empregados_ativos':str}}]},
args={'cnpj_orgao':str})
def empregadosAtivos (cnpj_orgao):
	empregadosAtivos = Model.empregadosAtivos(cnpj_orgao)
	y = []
	for orgao in empregadosAtivos:
		x = dict()
		x['orgao'] = orgao
		y.append(x)
	empregadosAtivos = y
	return empregadosAtivos
	
@service.xmlrpc
@service.soap('desligaEmpregado',returns={'s':str},args={'nu_matricula':str, 'dt_desligamento':str})
def desligaEmpregado(nu_matricula,dt_desligamento):
    s = Model.desligaEmpregado(nu_matricula,dt_desligamento)
    return s
    
@service.xmlrpc
@service.soap('removeDependente',returns={'s':str},args={'nu_cpf':str})
def removeDependente(nu_cpf):
    s = Model.removeDependente(nu_cpf)
    return s

def call():
    return service()
