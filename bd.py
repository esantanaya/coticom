from sqlalchemy import create_engine


class Conexion:
    def __init__(self, host='localhost', user='postgres', password='4cP#4j9R92'):
        self.engine = create_engine('postgresql+psycopg2://' + user + ':' +
        password + '@' + host + ':5432/pruebas')
        self.connection = self.engine.connect()
