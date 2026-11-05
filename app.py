from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("donors.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Home page
@app.route("/")
def home():
    blood_group = request.args.get("blood_group", "")
    location = request.args.get("location", "")

    conn = get_db_connection()

    query = "SELECT * FROM donors WHERE 1=1"
    values = []

    if blood_group:
        query += " AND blood_group = ?"
        values.append(blood_group)

    if location:
        query += " AND location LIKE ?"
        values.append("%" + location + "%")

    donors = conn.execute(query, values).fetchall()
    conn.close()

    return render_template("index.html", donors=donors)

# Register donor
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    blood_group = request.form["blood_group"]
    phone = request.form["phone"]
    location = request.form["location"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO donors (name, blood_group, phone, location)
        VALUES (?, ?, ?, ?)
    """, (name, blood_group, phone, location))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)