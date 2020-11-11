import os

import pymysql
from pymysql.cursors import DictCursor


# noinspection SqlNoDataSourceInspection
class Database:
    _connection = None
    _cursor = None

    def __init__(self, env_prefix=""):
        self._env_prefix = "" if not env_prefix else env_prefix

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if self._connection is None:
            self._connection = self.get_conn()
            self._cursor = self._connection.cursor()

    def disconnect(self):
        if self._connection is not None:
            self._connection.commit()
            self._connection.close()

    def auth_data(self):
        return {
            'host': os.getenv(self._env_prefix + 'HOST'),
            'port': int(os.getenv(self._env_prefix + 'PORT')),
            'database': os.getenv(self._env_prefix + 'DB'),
            'user': os.getenv(self._env_prefix + 'USER'),
            'password': os.getenv(self._env_prefix + 'PASS'),
        }

    def get_conn(self):
        return pymysql.connect(cursorclass=DictCursor, **self.auth_data())

    def execute_query(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    # noinspection PyBroadException
    def save_all(self, items, database, table, pk):
        queries = []
        try:
            for item in items:
                table = item.__class__.__name__
                it = self.__clean_dict(item)
                columns = ', '.join(it.keys())
                values = ", ".join("'{}'".format(k) for k in it.values())
                upd_info = ", ".join(str(k[0]) + "='" + str(k[1])
                                     + "'" for k in it.items() if k[0] != pk)
                sql = """INSERT INTO {}.{} ({})VALUES ({})ON DUPLICATE KEY UPDATE {}"""\
                    .format(database, table, columns, values, upd_info)
                queries.append(sql)
                self._cursor.execute(sql)
            self._connection.commit()
            print("Saved {} items.".format(len(items)))
            print(queries)
        except Exception:
            with open('error.log', '+a') as file:
                for query in queries:
                    file.write(query)

    @staticmethod
    def __clean_dict(item_dict):
        current_dict = dict()
        for k, v in item_dict.items():
            if isinstance(v, (list, set)):
                current_dict[k] = ", ".join(v)
            else:
                current_dict[k] = v
        return dict((k, v) for k, v in current_dict.items() if v)