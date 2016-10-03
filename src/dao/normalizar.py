import os.path, sys
import MySQLdb
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from dao.database import Database

## CREATED:Juan Carlos Suarez
## MAIL	  :jc.suarez.developer@gmail.com



def normalizacion():
	#------------------------------------------------------------------
	db = Database()
	query = """
		UPDATE segmento SET identificador = REPLACE(identificador, '-1', '') 
		WHERE tipo = 'ARTICULO' AND identificador LIKE '%-1';
		"""
	resp = db.cursor.execute(query)
	db.connection.commit()
	if resp == 1:
		print 'se termino de normalizar correctamente'
	else:
		print 'hubo algun problema con la normalizacion'