from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# DATABASE SETUP
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT
        )
        """)
        conn.commit()

# Call it before Flask starts
init_db()


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]
    hashed_password = generate_password_hash(password)

    try: 
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name,email,phone,password) VALUES (?,?,?,?)",
                (name, email, phone, hashed_password)
            )

        return redirect(url_for("success", username=name))
    except sqlite3.IntegrityError:
        return "EMAIL ALREADY REGISTERED"

@app.route("/success/<username>")
def success(username):
    return render_template("success.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)
