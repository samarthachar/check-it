# 📝 *Check-It* : A To-Do App

A sleek, user-authenticated to-do list web application built with Flask, SQLAlchemy, and Bootstrap. Users can sign up, log in, create multiple to-do lists, add tasks, mark them as complete, and delete them — all in a clean, responsive interface.

---

## 🚀 Features

- 🔐 User authentication (Sign Up, Log In, Log Out)
- 🧾 Create and manage multiple to-do lists
- ✅ Add, check/uncheck, and delete tasks
- 👤 Guest mode with temporary data
- 💾 SQLite database integration
- 🎨 Responsive UI with Bootstrap styling
- ⚠️ Flash messages for feedback and validation

---

## 🧰 Tech Stack

- **Backend:** Flask, Flask-Login, Flask-WTF, SQLAlchemy
- **Frontend:** HTML, Bootstrap via Flask-Bootstrap
- **Database:** SQLite

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/samarthachar/check-it.git
cd check-it
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the application
```bash
python server.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
├── server.py
├── forms.py
├── templates/
│   ├── homepage.html
│   ├── login.html
│   ├── signup.html
│   ├── todo.html
│   ├── pricing.html
│   └── about.html
├── static/
│   └── (optional CSS/JS files)
├── data.db
└── requirements.txt
```

---

## 🛡️ Security Notes

- Passwords are hashed using `werkzeug.security`.
- CSRF protection is enabled via Flask-WTF.
- Guest users are auto-created with placeholder credentials and cleared on login/signup.

---

## 🧪 Future Improvements

- Add Multiple To-Dos per User

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
# check-it
