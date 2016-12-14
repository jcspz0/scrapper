import os.path, sys
import MySQLdb
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import params
from dao.database import Database

def insert(titulo, url_ley, id_segmento, fecha, id_legislacion):
	try:
		db = Database()
		date = datetime.now()
		query = """
			INSERT INTO ley
			(`titulo`, `url_ley`, `id_segmento`, `fecha`, `id_legislacion`)
			VALUES
			(%s, %s, %s, %s, %s)
			"""
		resp = db.cursor.execute(query, (titulo.decode('utf-8'), url_ley, id_segmento, fecha, id_legislacion))
		db.connection.commit()
	except Exception, e:
		raise

def insert_con_codLey(titulo, url_ley, id_segmento, fecha, id_legislacion,codigo_ley,size_ley,alias):
	try:
		db = Database()
		date = datetime.now()

		#print 'titulo:'+titulo.decode('utf-8') + 'descrip:'+url_ley+ 'id_segmento:'+str(id_segmento)+'id_legislacion:'+str(id_legislacion)+'codLey:'+codLey
		query = """
			INSERT INTO ley
			(`titulo`, `url_ley`, `id_segmento`, `fecha`, `id_legislacion`,`codigo_ley`,`size_ley`,`alias`)
			VALUES
			(%s, %s, %s, %s, %s, %s,%s,%s)
			"""
		resp = db.cursor.execute(query, (titulo.decode('utf-8'), url_ley, id_segmento, fecha, id_legislacion,codigo_ley,size_ley,alias))
		db.connection.commit()
	except Exception, e:
		raise


def selectIDSegmento(id_legislacion):
	try:
		db = Database()
		query = """
			SELECT id_segmento FROM ley
			WHERE id_legislacion = %s
			"""
		db.cursor.execute(query, (id_legislacion,))
		resp = db.cursor.fetchone()
		db.connection.commit()
		if resp is None:
			return 0
		for item in resp:
			return item
		return 0
	except Exception, e:
		raise

def deleteLey(id_legislacion):
	try:
		db = Database()
		query = """
			DELETE FROM ley
			WHERE id_legislacion = %s
			"""
		db.cursor.execute(query, (id_legislacion,))
		db.connection.commit()
	except Exception, e:
		raise

def deleteLey_by_id(id):
	try:
		db = Database()
		query = """
			DELETE FROM ley
			WHERE id = %s
			"""
		db.cursor.execute(query, (id,))
		db.connection.commit()
	except Exception, e:
		raise


def insert_legislacion(url_ley,titulo_ley,tipoScrap):
	try:
		db = Database()
		query = """
			INSERT INTO legislacion
			(`url`, `tipo`, `tipo_scrap`)
			VALUES
			(%s, %s, %s)
			"""
		resp=db.cursor.execute(query, (url_ley,titulo_ley,tipoScrap))
		db.connection.commit()
		if resp == 1:
			#print '###  Legislacion Insertada  ####:',db.cursor.lastrowid
			return db.cursor.lastrowid
	except Exception, e:
		raise


def clean_db():
	clean_segmento()
	clean_ley()
	clean_legislacion()

def clean_segmento():
	try:
		db = Database()
		query = """
			DELETE FROM segmento			
			"""
		db.cursor.execute(query)
		db.connection.commit()
	except Exception, e:
		raise	

def clean_ley():
	try:
		db = Database()
		query = """
			DELETE FROM ley			
			"""
		db.cursor.execute(query)
		db.connection.commit()
	except Exception, e:
		raise	
def clean_legislacion():
	try:
		db = Database()
		query = """
			DELETE FROM legislacion			
			"""
		db.cursor.execute(query)
		db.connection.commit()
	except Exception, e:
		raise	

def get_nroUrl_for_leves(id_legislacion):
	try:
		db = Database()
		query = """
			SELECT cant_url_lv1,cant_url_lv2 FROM legislacion
			WHERE id= %s
			"""
		db.cursor.execute(query, (id_legislacion,))
		resp = db.cursor.fetchone()
		db.connection.commit()		
		if resp is not None:
			#print '### VALOR DE LOS NIVELES',resp
			return resp

		return None
	except Exception, e:
		raise

def set_nroUrl_level_1(id_legislacion,cantUrl):
	try:
		db = Database()
		query = """
			UPDATE legislacion SET cant_url_lv1=%s			
			WHERE id= %s
			"""
		db.cursor.execute(query, (cantUrl,id_legislacion,))		
		db.connection.commit()	

	except Exception, e:
		raise	

def set_nroUrl_level_2(id_legislacion,cantUrl):
	try:
		db = Database()
		query = """
			UPDATE legislacion SET cant_url_lv2=%s			
			WHERE id= %s
			"""
		db.cursor.execute(query, (cantUrl,id_legislacion,))		
		db.connection.commit()	
		
	except Exception, e:
		raise

def get_legislaciones():
	try:
		db = Database()
		query = """
			SELECT id,url,cant_url_lv1,cant_url_lv2,tipo_scrap,tipo FROM legislacion			
			"""
		db.cursor.execute(query)		
		db.connection.commit()	
		arrLegis=[]			
		if db.cursor is not None:
			for tupla in db.cursor:				
				#print '### VALOR DE LOS NIVELES',tupla
				arrLegis.append(tupla)
			return arrLegis

		return None
	except Exception, e:
		raise	

def exists_ley(codigo_ley):
	try:
		db = Database()
		query = """
			SELECT id,id_segmento,size_ley,alias 
			FROM ley 
			WHERE codigo_ley= %s			
			"""
		db.cursor.execute(query, (codigo_ley,))
		resp = db.cursor.fetchone()
		db.connection.commit()
		if resp is None:
			return None
		else:
			return resp	

	except Exception, e:
		raise	

#rep=exists_ley('DELhy5452')					
#print 'ley',rep
#res=get_legislaciones()
#print 'Respuesta',len(res)
#set_nroUrl_level_1(1,1885)
#resp=get_nroUrl_for_leves(1)
#print 'item obtenido',resp[0]													