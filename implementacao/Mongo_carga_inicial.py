from mongo import *

m = Model()
db = m.conectaMongo()
db.connection.drop_database("rhdb001")

vinculo_1 = {"no_tipo_vinculo":"CONJUGE"}
vinculo_2 = {"no_tipo_vinculo":"FILHO"}
vinculo_3 = {"no_tipo_vinculo":"PAI"}
vinculo_4 = {"no_tipo_vinculo":"MAE"}
vinculo_5 = {"no_tipo_vinculo":"SOGRO"}
vinculo_6 = {"no_tipo_vinculo":"SOGRA"}
vinculo_7 = {"no_tipo_vinculo":"ENTEADO"}

db.vinculos.insert(vinculo_1)
db.vinculos.insert(vinculo_2)
db.vinculos.insert(vinculo_3)
db.vinculos.insert(vinculo_4)
db.vinculos.insert(vinculo_5)
db.vinculos.insert(vinculo_6)
db.vinculos.insert(vinculo_7)

tipo_1 = {"no_tipo_documento":"RG","ic_ativo": True}
tipo_2 = {"no_tipo_documento":"CPF","ic_ativo": True}
tipo_3 = {"no_tipo_documento":"CERTIDAO DE CASAMENTO","ic_ativo": True}
tipo_4 = {"no_tipo_documento":"CERTIDAO DE NASCIMENTO","ic_ativo": True}
tipo_5 = {"no_tipo_documento":"COMPROVANTE DE RESIDENCIA","ic_ativo": True}
tipo_6 = {"no_tipo_documento":"DIPLOMA","ic_ativo": True}
tipo_7 = {"no_tipo_documento":"CERTIFICADO","ic_ativo": True}

db.tp_documentos.insert(tipo_1)
db.tp_documentos.insert(tipo_2)
db.tp_documentos.insert(tipo_3)
db.tp_documentos.insert(tipo_4)
db.tp_documentos.insert(tipo_5)
db.tp_documentos.insert(tipo_6)
db.tp_documentos.insert(tipo_7)
