import os
import psycopg

from dotenv import load_dotenv
from pgvector.psycopg import register_vector

load_dotenv()


def get_connection():

    # Establish a connection with a timeout
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        dbname=os.getenv("POSTGRES_DB", "codepilot"),
        user=os.getenv("POSTGRES_USER", "codepilot"),
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5
    )

    # Register pgvector data types
    try:
        register_vector(conn)
    except Exception:
        conn.close()
        raise

    return conn