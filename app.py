from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
import os
import time

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def create_table():
    while True:
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                );
            """)

            conn.commit()
            cur.close()
            conn.close()

            print("Tabla creada correctamente")
            break

        except Exception as e:
            print("Esperando PostgreSQL...", e)
            time.sleep(5)


create_table()


@app.route('/')
def home():
    return {"msg": "ok"}


@app.route('/todos', methods=['POST'])
def create_todo():

    data = request.get_json()

    title = data.get("title")

    if not title:
        return jsonify({
            "error": "title es obligatorio"
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO todos (title) VALUES (%s)",
        (title,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Tarea creada"
    }), 201


@app.route('/todos', methods=['GET'])
def get_todos():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title FROM todos"
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "title": row[1]
        })

    return jsonify(todos)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )