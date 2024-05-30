import os

import dotenv
import psycopg2

dotenv.load_dotenv(".env.development")


class Database:
    def __enter__(self):
        self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query_text, *args):
        if args:
            self.cursor.execute(query_text, args)
        else:
            self.cursor.execute(query_text)

    def execute_file(self, file_name):
        with open(file_name) as file:
            query_text = file.read()
            self.execute_query(query_text)

    def fetch_description(self):
        return self.cursor.description

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()
