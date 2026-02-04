📌 README.md
# 📍 Cybernova Symposium Portal

**Live Site:** https://cybernova-symposium-portal.onrender.com/

Cybernova is a modern, visually appealing **symposium event website** built with **Flask**.  
It features a rich UI with a glassmorphism theme, interactive event details, registration forms, an admin dashboard, and CSV export functionality — all designed for a seamless user experience across devices.

---

## 🧠 Overview

This project is a complete web application for managing registrations for a college symposium event called **Cybernova**.  
It is backed by **SQLite** for data storage, deployed on **Render**, and built using **Python + Flask + HTML/CSS/JS**.

**Key features include:**
- Beautiful glassmorphism UI with gradient themes
- Dynamic event listing with dedicated detail pages
- Responsive design (mobile & desktop)
- Multi-event registration form with validation
- Admin dashboard for viewing registrations
- CSV export of registration data
- Mounted with user-experience enhancements

---

## 📌 Features

### 🎯 User Experience
✔ Personalized success page showing the registered event  
✔ Smooth confetti animation on successful registration  
✔ Share buttons (WhatsApp, LinkedIn) for social sharing

### 📝 Registration
✔ Full name, register number, department, year selection  
✔ Event selection & validation  
✔ Client-side and server-side validation

### 🛠️ Admin Dashboard
✔ Password-protected admin login  
✔ Shows all registrations in a sortable table  
✔ Export registrations to CSV

---

## 📦 Tech Stack

| Feature | Technology |
|---------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| UI Style | Glassmorphism + Gradient Theme |
| Database | SQLite (with SQLAlchemy) |
| Deployment | Render |
| Templates | Jinja2 |

---

## 🗂️ Project Structure



cybernova-symposium-portal/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── runtime.txt
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── event_detail.html
│ ├── register.html
│ ├── success.html
│ ├── admin.html
│ └── login.html
├── static/
│ ├── css/
│ ├── js/
│ └── images/
├── instance/ # SQLite database goes here
├── .gitignore
└── README.md


---

## 🚀 Live Demo

Visit the deployed application here:

👉 https://cybernova-symposium-portal.onrender.com/

Explore the homepage, navigate events, register, and visit the admin panel (login required).

---

## 👩‍💻 Getting Started (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/PriyadharshniG/cybernova-symposium-portal.git
cd cybernova-symposium-portal

2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables

Create a .env file:

SECRET_KEY=your_secret_key_here
ADMIN_PASSWORD=your_admin_password

5. Run the app locally
python app.py


Open the browser:
👉 http://127.0.0.1:5000/

🧠 How It Works
✔ User Registration

Users can register for events with complete details.
Data is saved using SQLAlchemy in an SQLite database.

✔ Admin Panel

The admin panel is protected by a password stored as an environment variable.
Admins can view all registrations and export them.

🛡 Environment Variables

Make sure these exist in your deployment platform (like Render):

Key	Purpose
SECRET_KEY	Session security key
ADMIN_PASSWORD	Admin login password
📈 Deployment (Render)

This project includes:

✔ runtime.txt — pins Python 3.12.x
✔ requirements.txt — includes all packages (including gunicorn)
✔ Auto-creation of database tables on startup

When deploying on Render:

Select Python 3

Add environment variables (SECRET_KEY, ADMIN_PASSWORD)

Build command: pip install -r requirements.txt

Start command: gunicorn app:app

💡 Contributions

This project is a personal / academic project.
Feel free to open issues or propose enhancements!

📜 License

MIT License © 2026
