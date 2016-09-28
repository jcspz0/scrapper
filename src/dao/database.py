import os.path, sys
import MySQLdb
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import params
from MySQLdb import OperationalError

class Database:

    host = params.db_host
    user = params.db_username
    password = params.db_password
    db = params.db_name
    port = params.db_port

    connection=None

    def __init__(self):
       
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,charset='utf8', 
                                db=self.db, port=self.port)
      
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection=MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,charset='utf8', 
                                db=self.db, port=self.port)

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except OperationalError as e:
            if 'MySQL server has gone away' in str(e):
                self.connect()
            else:                
                self.connection.rollback()



    def query(self, query):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()