import mysql.connector as connector
from Config.CONFIG import Connection


class DBConnect(object):

    ''' MySQL DB decorator '''

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = self._connect()
        self.cursor = self.connection.cursor()

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            try:
                self.cursor.execute('BEGIN')
                result = func(self.cursor, *args, **kwargs)
                self.cursor.execute('COMMIT')
            except:
                self.cursor.execute('ROLLBACK')
                raise
            finally:
                self.cursor.close()

            return result

        return wrapped

    def __del__(self):
        self.connection.close()

    def _connect(self):
        connection = connector.connect(
                host=Connection.DB_HOST.value,
                user=Connection.DB_USER.value,
                passwd=Connection.DB_PASSWORD.value,
                database=self.db_name)

        return connection

    
