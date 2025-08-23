from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash , check_password_hash
import os
import sqlite3
from flask import session


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
app.secret_key = "supersecretkey"  # required to use sessions

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




@app.route("/login", methods=["GET", "POST"])
def login():
    print("METHOD RECEIVED:", request.method)   # debug
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("Form data:", email, password) 

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, password FROM users WHERE email=?", (email,))
            user = cursor.fetchone()

        if user:
            name, hashed_password = user
            if check_password_hash(hashed_password, password):
                session["username"] = name
                return "loggin babe"
            else:
                return "INVALID PASSWORD"
        else:
            return "NO SUCH USER"

    # return render_template("homepage.html")
    return "fuck offwwww"





@app.route("/success/<username>")
def success(username):
    return render_template("success.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)
