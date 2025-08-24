import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change for production
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------- DB Setup ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT,
            profilepic TEXT
        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS NOTES(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
                       )
                       """)



        conn.commit()

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("cp")
        
        if password != confirm_password:
            return "PASSWORDS DO NOT MATCH"
        
        hashed_password = generate_password_hash(password)
        
        # Handle file upload
        file = request.files.get("profilepic")
        if not file or file.filename == "":
            return "NO FILE UPLOADED"
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Save user in DB (store filename, not full path)
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name,email,phone,password,profilepic) VALUES (?,?,?,?,?)",
                    (name, email, phone, hashed_password, filename)
                )
                userid = cursor.lastrowid
                session["user_id"]=userid
                conn.commit()
            
            session["username"] = name
            session["email"] = email
            session["profilepic"] = filename
            return redirect(url_for("profile"))
            
        except sqlite3.IntegrityError:
            return "EMAIL ALREADY REGISTERED"
    
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, password, profilepic FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()


        
        if user and check_password_hash(user[2], password):
            session["username"] = user[1]
            session["email"] = email
            session["profilepic"] = user[3]
            session["user_id"] = user[0]

            return redirect(url_for("profile"))
        else:
            return "INVALID CREDENTIALS - Check your email and password"
    
    return render_template("homepage.html")

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    userid = session["user_id"]

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, created_at FROM NOTES WHERE user_id = ? ORDER BY created_at DESC",
            (userid,)
        )
        notes = cursor.fetchall()

    return render_template(
        "profile.html",
        username=session["username"],
        email=session.get("email"),
        profilepic=url_for("uploaded_file", filename=session.get("profilepic")),
        notes=notes
    )



#NOTES

# @app.route("/notes")
# def notes():
#     if "user_id" not in session:
#         return redirect(url_for("home"))
#     userid=session["user_id"]



#     with sqlite3.connect(DB_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT id,title,content,Created_at FROM NOTES WHERE user_id = ? ORDER BY created_at DESC",(userid,))
#         notes=cursor.fetchall()

#     return render_template("profile.html",notes=notes)


@app.route("/addnotes" , methods = ["POST"])
def addnotes():
    if "user_id" not in session:
        return redirect(url_for("home"))
    title = request.form.get("title")
    content = request.form.get("content")
    user_id = session["user_id"]

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO NOTES (title, content, user_id, created_at) VALUES (?, ?, ?, datetime('now'))",
            (title, content, user_id)
        )
        conn.commit()

    return redirect(url_for("profile"))
# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)