# CyberNova Symposium Portal

A premium, visually stunning event registration portal built with Flask.

## Features
- **Futuristic Design:** Neon gradients, Glassmorphism, and Animations.
- **Landing Page:** One-page scroll layout for About, Themes, and Events.
- **Registration:** Clean, validated form for student registration.
- **Admin Dashboard:** Secure area to view and export registrations to CSV.

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, SQLite
- **Frontend:** HTML5, CSS3 (Custom Glassmorphism), Vanilla JS
- **Icons:** Lucide Icons

## Setup & Run

1.  **Create/Activate Virtual Environment:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

3.  **Run Application:**
    ```powershell
    python app.py
    ```
    The app will run at `http://127.0.0.1:5000`.

## Admin Access
- **Login URL:** `/admin/login`
- **Default Password:** `admin123` (Change in `.env` or `config.py` for production)
