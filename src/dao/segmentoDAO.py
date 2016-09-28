import os.path, sys
import MySQLdb
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from dao.database import Database
from MySQLdb import OperationalError
import params
import scrapers.hard_code_util

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com

#TIPO_LEY = 'LEY'
TIPO_TITULO_LEY='TITULO_LEY'
TIPO_PARTE = 'PARTE'
TIPO_LIBRO = 'LIBRO'
TIPO_TITULO = 'TITULO'
TIPO_SUBTITULO = 'SUBTITULO'
TIPO_CAPITULO = 'CAPITULO'
TIPO_SECCION = 'SECCION'
TIPO_SUBSECCION = 'SUBSECCION'
TIPO_ARTICULO = 'ARTICULO'
TIPO_ITEM_ARTICULO = 'ITEM_ARTICULO'
TIPO_FOOTER = 'FOOTER'
TIPO_HEADER = 'HEADER'


def insert(contenido, tipo, id_ley, id_parent=None, identificador=None):
	#------seccion en la que seteamos los link al segmento ------------
	contenido=scrapers.hard_code_util.set_link_segmento(contenido)
	if identificador is not None:
		identificador=identificador.replace('.','')
	#------------------------------------------------------------------
	db = Database()
	try:
		
		query = """
			INSERT INTO segmento
			(`contenido`, `tipo`, `id_parent`, `id_ley`, `identificador`)
			VALUES
			(%s, %s, %s, %s, %s)
			"""
		resp = db.cursor.execute(query, (contenido, tipo, id_parent, id_ley,identificador ))#cambiamos el decode a ignore para obiar unos caracteres q  no decodidfica
		db.connection.commit()
		if resp == 1:
			print 'segmento se inserto con el Resgistro:',db.cursor.lastrowid
			return db.cursor.lastrowid
	except OperationalError as e:
		if 'MySQL server has gone away' in str(e):
			#do what you want to do on the error
			db = Database()
			resp = db.cursor.execute(query, (contenido.decode('utf-8', errors='ignore'), tipo, id_parent, id_ley, identificador))#cambiamos el decode a ignore para obiar unos caracteres q  no decodidfica
			db.connection.commit()
			if resp == 1:
				print 'segmento se inserto con el Resgistro:',db.cursor.lastrowid
				return db.cursor.lastrowid
			print e
		else:
			raise
	return None

def deleteSegmentos(id_ley):
	try:
		db = Database()
		query = """
			DELETE FROM segmento
			WHERE id = %s OR id_ley = %s
			"""
		db.cursor.execute(query, (id_ley, id_ley))
		db.connection.commit()
	except Exception, e:
		raise