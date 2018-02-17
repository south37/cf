from dotenv import load_dotenv, find_dotenv
import os
import psycopg2

# NOTE: Read from dotenv
env_path = find_dotenv()
if env_path != '':
    load_dotenv(env_path)
env = os.environ

class Database:
    # NOTE: Connecion is cached
    connection = None

    @staticmethod
    def get_connection():
        if Database.connection:
            return Database.connection

        Database.connection =  psycopg2.connect(database=env['DATABASE_NAME'],
            user=env['DATABASE_USER'],
            password=env['DATABASE_PASSWORD'],
            host=env['DATABASE_HOST'],
            port=env['DATABASE_PORT'])
        return Database.connection
