from typing import List, Any

import mysql.connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def _get_connection():
    connection = mysql.connector.connect(
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        database=getenv("DB_NAME"),
        port=int(getenv("DB_PORT"))
    )

    return connection

def select(query, parameters):
    with _get_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, parameters)
        return cursor.fetchall()

def write_many(queries: List[dict[str, str | tuple[Any, Any]]]):
    with _get_connection() as connection:
        cursor = connection.cursor()

        for query in queries:
            cursor.execute(query.get("query"), query.get("parameters"))

        connection.commit()
