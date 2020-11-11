from shops_scraper.util.database import Database


class ProxyDB(Database):
    protocols = {
        1: 'http',
        2: 'https',
        0: 'http'
    }

    def __init__(self):
        super().__init__("PARSING_")

    def get_all_proxy(self):
        query = "SELECT type, host, port FROM `proxy`.`proxy_checked` WHERE type < 3"
        return self.__get_proxy(query)

    @staticmethod
    def get_proxy_list():
        with ProxyDB() as db:
            return db.get_all_proxy()

    def __get_proxy(self, query):
        self._cursor.execute(query)
        data = self._cursor.fetchall()
        return ["{}://{}:{}".format(self.protocols[p['type']], p['host'], p['port']) for p in data]