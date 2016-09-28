import MySQLdb
import params
from dao.database import Database
from datetime import datetime

def info(detail):
	__log(detail, 'INFO')

def debug(detail):
	__log(detail, 'DEBUG')

def warn(detail):
	__log(detail, 'WARN')

def error(detail):
	__log(detail, 'ERROR')

def __log(detail, level):
	try:
		db = Database()
		date = datetime.now()
		query = """
			INSERT INTO scraper_log
			(`fecha`, `tipo_log`, `detalle`)
			VALUES
			(%s, %s, %s)
			"""
		resp = db.cursor.execute(query, (date, level, detail))
		db.connection.commit()
	except Exception, e:
		raise