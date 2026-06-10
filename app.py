import os
import random
import string
from flask import Flask, request, redirect, render_template
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

@app.before_request
def setup():
    init_db()

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            short_code VARCHAR(10) UNIQUE NOT NULL,
            original_url TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        original_url = request.form["url"]
        code = generate_code()
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
                    (code, original_url))
        conn.commit()
        cur.close()
        conn.close()
        short_url = request.host_url + code
    return render_template("index.html", short_url=short_url)

@app.route("/<code>")
def redirect_url(code):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT original_url FROM urls WHERE short_code = %s", (code,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return redirect(row[0])
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)