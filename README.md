# simple_crud
# Notes App 📝

A simple **Flask + SQLite** web application for managing personal notes.  
Users can **sign up, log in, create, edit, and delete notes**.  
Built as a learning project to practice Flask, authentication, and CRUD operations.

---

## 🚀 Features
- 🔐 User authentication (signup & login with hashed passwords)  
- ✏️ Create and save notes  
- 📖 View your notes after login  
- 🔄 Edit existing notes  
- ❌ Delete notes  
- 💾 Data stored in SQLite (lightweight database)  

---

## 🛠 Tech Stack
- **Backend:** Flask (Python)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS  

---

## 📦 Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/notes-app.git
   cd notes-app

    (Optional but recommended) Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

If you don’t have a requirements.txt, you can install manually:

pip install flask

Run the app

python app.py

Open in your browser:

    http://127.0.0.1:5000

📂 Project Structure

Fixit/
├── backend/
│   └── app.py
├── frontend/
│   ├── signup.html
│   ├── notes.html
│   └── css/
│       └── signup.css
├── requirements.txt
└── README.md

🔮 Future Improvements

    🎨 Better UI (Tailwind / Bootstrap)

    ☁️ Deploy online (Heroku, Render, or PythonAnywhere)

    🌓 Dark mode support

    📱 Mobile-friendly layout

📖 Learning Goals

This project helped me practice:

    Setting up Flask routes

    Handling authentication with password hashing

    Working with SQLite databases

    Building CRUD functionality

    Connecting backend and frontend

