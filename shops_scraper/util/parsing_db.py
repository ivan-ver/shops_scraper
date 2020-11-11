from shops_scraper.util.database import Database


# noinspection SqlNoDataSourceInspection
class ParsingDB(Database):
    # def __init__(self):
    #     super().__init__("PARSING_")

    def save_all(self, items, database='shops_scraper', table='', pk='url'):
        super().save_all(items, database, table, pk)

    def get_all(self, query):
        return super().execute_query(query)

    @staticmethod
    def get_all_url(schema, table_title):
        with ParsingDB() as db:
            query = """SELECT url FROM {}.{}""".format(schema, table_title)
            list_ = db.get_all(query)
            res = [u['url'] for u in list_]
            return res
