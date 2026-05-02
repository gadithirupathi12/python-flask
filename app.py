from flask import Flask, request, jsonify, render_template
import sqlite3, os

app = Flask(__name__)

DB = os.environ.get("DB_PATH", "employees.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
        )
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

# ✅ Health endpoint (important for CI)
@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json() or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Name required"}), 400

    with get_db() as conn:
        conn.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()

    return jsonify({"message": "Added"}), 201

@app.route("/employees", methods=["GET"])
def get_employees():
    with get_db() as conn:
        rows = conn.execute("SELECT id, name FROM employees").fetchall()

    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host=host, port=port)
