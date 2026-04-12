import os
import requests
import psycopg
from flask import Flask, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
RAPIDAPI_KEY = os.getenv("FUNFACT_API_KEY")

RAPIDAPI_HOST = "world-fun-facts-all-languages-support.p.rapidapi.com"

FUN_FACTS_URL = (
    "https://world-fun-facts-all-languages-support.p.rapidapi.com/fact.php"
)


def get_db_connection():
    return psycopg.connect(DATABASE_URL, sslmode="require")

def init_db():
    with get_db_connection() as conn:
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

with app.app_context():
    init_db()


def fetch_and_store_fact():

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    params = {
        "lang": "en"
    }

    try:
        response = requests.get(
            FUN_FACTS_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        data = response.json()

        fact_data = {
            "uuid": data.get("uuid"),
            "lang_code": data.get("lang_code"),
            "lang_name": data.get("lang_name"),
            "text": data.get("text")
        }

        if not fact_data["uuid"]:
            return {"error": f"Invalid response: {data}"}

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO facts (uuid, lang_code, lang_name, text)
                    VALUES (%(uuid)s, %(lang_code)s, %(lang_name)s, %(text)s)
                    ON CONFLICT (uuid) DO NOTHING;
                """, fact_data)

            conn.commit()

        return fact_data

    except requests.RequestException as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"Database or parsing error: {str(e)}"}


def get_latest_fact():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT uuid, lang_code, lang_name, text, retrieved_at
                FROM facts
                ORDER BY retrieved_at DESC
                LIMIT 1;
            """)

            row = cur.fetchone()

            if row:
                return {
                    "uuid": row[0],
                    "lang_code": row[1],
                    "lang_name": row[2],
                    "text": row[3],
                    "retrieved_at": row[4]
                }

            return None


@app.route("/")
def index():

    fact = get_latest_fact()

    if not fact:
        fact = fetch_and_store_fact()

        if "error" in fact:
            return render_template(
                "index.html",
                error=fact["error"],
                fact=None
            )

    return render_template(
        "index.html",
        fact=fact,
        error=None
    )

@app.route("/new-fact")
def new_fact():

    fact = fetch_and_store_fact()

    if "error" in fact:
        return render_template(
            "index.html",
            error=fact["error"],
            fact=None
        )

    return render_template(
        "index.html",
        fact=fact,
        error=None
    )

@app.route("/fact")
def fact_json():

    fact = get_latest_fact()

    if not fact:
        fact = fetch_and_store_fact()

    return jsonify(fact)

@app.route("/health")
def health():

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }

        params = {
            "lang": "en"
        }

        requests.get(
            FUN_FACTS_URL,
            headers=headers,
            params=params,
            timeout=5
        )

        return {"status": "ok"}

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 500


if __name__ == "__main__":
    app.run(debug=True)
