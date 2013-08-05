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
@service.soap('AddStrings',returns={'AddResult':str},args={'a':str, 'b':str})
@service.soap('AddIntegers',returns={'AddResult':int},args={'a':int, 'b':int})
def add(a,b):
    "Add two values"
    return a+b

@service.xmlrpc
@service.soap('SubIntegers',returns={'SubResult':int},args={'a':int, 'b':int})
def sub(a,b):
    "Substract two values"
    return a-b
    
@service.xmlrpc
@service.soap('insereOrgao',returns={'s':str},args={'cnpj':str, 'nome':str, 'endereco':str, 'cidade':str, 'uf':str})
def insereOrgao(cnpj,nome,endereco,cidade,uf):
    s = Model.insereOrgao(cnpj,nome,endereco,cidade,uf)
    return s
    
@service.xmlrpc
@service.soap('insereEmpregado',returns={'s':str},args={'nome':str, 'dt_contratacao':str, 'dt_desligamento':str, 'dt_nascimento':str, 'nu_matricula':str, 'rg':str, 'cpf':str, 'id_orgao':str, 'documentos':str, 'dependentes':str})
def insereEmpregado(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos,dependentes):
    s = Model.insereEmpregado(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula,rg,cpf,id_orgao,documentos,dependentes)
    return s
    
@service.xmlrpc
@service.soap('insereDependente',returns={'s':str},args={'nome':str, 'rg':str, 'cpf':str, 'certidao':str, 'dt_nascimento':str, 'tp_vinculo':str, 'documentos':str, 'idEmpregado':str})
def insereDependente(nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,idEmpregado):
    s = Model.insereDependente(nome,rg,cpf,certidao,dt_nascimento,tp_vinculo,documentos,idEmpregado)
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
@service.soap('listaOrgao',returns={ 'orgaos': [{'id':str},{'nu_cnpj':str},{'no_orgao':str},{'no_endereco':str},{'no_cidade':str},{'no_uf':str}]},
args={'nome':str, 'endereco':str, 'cidade':str, 'uf':str})
def listaOrgao(nome,endereco,cidade,uf):
	orgaos = Model.listaOrgaos(nome,endereco,cidade,uf)
	return orgaos

@service.xmlrpc
@service.soap('listaEmpregados',returns={ 'empregados': [{'id':str},{'no_empregado':str},{'dt_contratacao':str},{'dt_desligamento':str},{'dt_nascimento':str},{'nu_matricula':str},{'nu_rg':str},{'nu_cpf':str},{'id_orgao':str},{'Documentos':str},{'Dependentes':str}]},
args={'nome':str, 'dt_contratacao':str, 'dt_desligamento':str, 'dt_nascimento':str, 'nu_matricula':str})
def listaEmpregados(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula):
	empregados = Model.listaEmpregados(nome,dt_contratacao,dt_desligamento,dt_nascimento,nu_matricula)
	return empregados 

@service.xmlrpc
@service.soap('listaDependentes',returns={ 'empregados': [{'id':str},{'no_empregado_dependente':str},{'nu_rg':str},{'nu_cpf':str},{'nu_certidao':str},{'dt_nascimento':str},{'tp_vinculo':str},{'Documentos':str}]},
args={'nomeEmpregado':str, 'nomeDependente':str, 'matricula':str, 'dt_nascimento':str, 'tp_vinculo':str})
def listaDependentes(nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo):
	dependentes = Model.listaDependentes(nomeEmpregado,nomeDependente,matricula,dt_nascimento,tp_vinculo)
	return dependentes 

def call():
    return service()
