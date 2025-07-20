# 🎓 Learning Management System (LMS)

A full-stack Learning Management System built with **Django** (Backend) and **React** (Frontend). The system includes user management, data population scripts, and a custom frontend hosted inside the backend directory.

---

## 🚀 Getting Started

Follow these steps to run the LMS project on your local machine.

### 🧰 Prerequisites

- Python 3.x
- Node.js and npm
- Virtualenv (optional but recommended)

---

## ⚙️ Setup Instructions

### ✅ Step 1: Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate   # On Linux/macOS
env\Scripts\activate      # On Windows
```

✅ Step 2: Install backend dependencies

cd backend
pip install -r requirements.txt

✅ Step 3: Set up the database

python manage.py makemigrations
python manage.py migrate

✅ Step 4: Populate database with sample data

python populate.py

✅ Step 5: Create a superuser

python manage.py createsuperuser

✅ Step 6: Run Django development server

python manage.py runserver

The backend will now be live at http://127.0.0.1:8000/
