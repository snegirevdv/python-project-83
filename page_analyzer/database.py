import psycopg2


class Database:
    def __init__(self, database_url):
        print('Создание БД')
        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()
        print('БД создана.')

    def execute_query(self, query_text):
        try:
            print('Выполняется запрос.')
            self.cursor.execute(query_text)
            if self.does_change(query_text):
                self.connection.commit()
            print('Запрос выполнен.')
        except Exception as e:
            print(f"PostgreSQL Error: {e}")
            self.connection.rollback()
            raise

    def execute_query_with_args(self, query_text, *args):
        try:
            print('Выполняется запрос')
            self.cursor.execute(query_text, args)
            if self.does_change(query_text):
                self.connection.commit()
            print('Запрос выполнен.')
        except Exception as e:
            print(f"PostgreSQL Error: {e}")
            self.connection.rollback()
            raise

    def migrate(self, file_name):
        print('Миграция начата.')
        try:
            with open(file_name) as file:
                query_text = file.read()
            self.execute_query(query_text)
            print('Миграция завершена.')
        except Exception as e:
            print(f"Migration error: {e}")
            self.connection.rollback()
            raise

    def fetch_description(self):
        print('Fetching description')
        return self.cursor.description

    def fetch_all(self):
        print('Fetching all rows')
        return self.cursor.fetchall()

    def fetch_one(self):
        print('Fetching one row')
        return self.cursor.fetchone()

    def commit(self):
        print('Committing transaction')
        self.connection.commit()

    def close(self):
        print('Closing connection')
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def does_change(query_text):
        return (
            "INSERT" in query_text
            or "UPDATE" in query_text
            or "DELETE" in query_text
        )