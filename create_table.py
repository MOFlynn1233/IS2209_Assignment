import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_table():
    # Make sure DATABASE_URL is not None
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not found in environment variables. Check your .env file.")

    # Connect using the DATABASE_URL
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id SERIAL PRIMARY KEY,
                    uuid VARCHAR(255) UNIQUE NOT NULL,
                    lang_code VARCHAR(10),
                    lang_name VARCHAR(50),
                    text TEXT NOT NULL,
                    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
        print("Table 'facts' created successfully (or already exists).")

if __name__ == "__main__":
    create_table()