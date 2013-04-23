import psycopg2
import psycopg2.extras

def abreConexao():
	conn = psycopg2.connect(host='localhost', database="rhdb001", user="postgres", password="123456")
	return conn
	
def fechaConexao():
	dict_cur.close()	

#print cur.fetchone()

#print cur.fetchall()

def insereOrgao():
	sql = "insert into tb002_orgao (no_orgao) values ('Ministerio Teste')"
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	conn.commit()
	resultado = cursor.execute(sql)
	#cursor.close()
	return resultado

def insereEmpregado():
	conn = abreConexao()
	sql = "insert into tb004_empregado (no_empregado, dt_contratacao,dt_nascimento,nu_matricula,id_orgao) values ('Empregado T','01/01/1998','12/02/1970','E000001',9)"
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	conn.commit()
	resultado = cursor.execute(sql)
	#cursor.close()
	return resultado
	
def listaEmpregados(id_empregado='',no_empregado='',dt_contratacao='',dt_desligamento='',dt_nascimento='',nu_matricula='',id_orgao=''):
	conn = abreConexao()
	if id_empregado != '':
		id_empregado = "AND id_empregado = "+str(id_empregado)
		
	if no_empregado != '':
		no_empregado = "AND no_empregado = '"+no_empregado+"'"
		
	if dt_contratacao != '':
		dt_contratacao = "AND dt_contratacao = '"+dt_contratacao+"'"
		
	if dt_desligamento != '':
		dt_desligamento = "AND dt_desligamento = '"+dt_desligamento+"'"
		
	if dt_nascimento != '':
		dt_nascimento = "AND dt_nascimento = '"+dt_nascimento+"'"
		
	if nu_matricula != '':
		nu_matricula = "AND nu_matricula = '"+nu_matricula+"'"
		
	if id_orgao != '':
		id_orgao = "AND id_empregado = "+str(id_orgao)
		
	sql = "select * from tb004_empregado where 1=1 "+id_empregado+no_empregado+dt_contratacao+dt_desligamento+dt_nascimento+nu_matricula+id_orgao
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	resultado = cursor
	conn.commit()
	cursor.execute(sql)
	resultado = cursor
	#cursor.close()
	return resultado
	
def listaOrgaos(id_orgao,no_orgao):
	conn = abreConexao()
	sql = "select * from tb002_orgao"
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	conn.commit()
	resultado = cursor.execute(sql)
	#cursor.close()
	return resultado
	
#insereOrgao()
#dict_cur.close()
#insereEmpregado()
#insereEmpregado()
#servidores = listaEmpregados(id_empregado = 7)

#for servidor in servidores:
#	print servidor['no_empregado']

#dict_cur.close()
#conn.close()
