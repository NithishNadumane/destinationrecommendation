import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    database_url = os.getenv("DATABASE_URL")

    # Production / Render / Neon
    if database_url:
        return psycopg2.connect(database_url)

    # Local PostgreSQL fallback
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="beliketraveller",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )