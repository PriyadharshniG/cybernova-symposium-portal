import os
import csv
import io
from functools import wraps
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session, Response
)
from config import Config
from models import db, Registration

# -------------------------------------------------
# App Setup
# -------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

# REQUIRED for sessions (ADMIN LOGIN)
app.secret_key = app.config["SECRET_KEY"]

# REQUIRED for SQLite on Render
os.makedirs("instance", exist_ok=True)

# Initialize database
db.init_app(app)

# Create tables on startup (WORKS ON RENDER)
with app.app_context():
    db.create_all()

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------
# Event Data
# -------------------------------------------------

EVENTS = {
    "hackathon": {
        "id": "hackathon",
        "name": "Open Source Hackathon",
        "category": "Flagship Event",
        "icon": "code-2",
        "tagline": "Build for the Community",
        "description": "A 24-hour intense coding marathon where participants collaborate to build open-source solutions for real-world problems.",
        "rules": ["Team size: 2-4 members", "Open source tools only", "Code must be pushed to GitHub"],
        "skills": ["Teamwork", "Open Source", "Rapid Prototyping"],
        "poster": "event_hackathon.png",
    },
    "paper-presentation": {
        "id": "paper-presentation",
        "name": "Paper Presentation",
        "category": "Technical",
        "icon": "file-text",
        "tagline": "Innovate & articulate",
        "description": "Present your research ideas on emerging technologies.",
        "rules": ["7 mins + 3 mins Q&A", "Original work only"],
        "skills": ["Public Speaking", "Research"],
        "poster": "event_paper_pres.png",
    },
    "web-dev": {
        "id": "web-dev",
        "name": "Web Dev Challenge",
        "category": "Technical",
        "icon": "layout",
        "tagline": "Craft the digital future",
        "description": "Design and build stunning web applications.",
        "rules": ["Individual participation", "Any framework allowed"],
        "skills": ["Frontend", "Backend", "Deployment"],
        "poster": "event_web_dev.png",
    },
    "ai-ideathon": {
        "id": "ai-ideathon",
        "name": "AI & ML Ideathon",
        "category": "Innovation",
        "icon": "brain-circuit",
        "tagline": "Think. Train. Deploy.",
        "description": "Pitch AI-driven ideas focusing on social impact.",
        "rules": ["PPT or prototype"],
        "skills": ["AI Strategy", "Problem Solving"],
        "poster": "event_ai_ml.png",
    },
    "ui-ux": {
        "id": "ui-ux",
        "name": "UI/UX Design Sprint",
        "category": "Design",
        "icon": "pen-tool",
        "tagline": "Design with empathy",
        "description": "Create user-centric designs.",
        "rules": ["Figma / Adobe XD"],
        "skills": ["Design Thinking"],
        "poster": "event_ui_ux.png",
    },
    "git-bootcamp": {
        "id": "git-bootcamp",
        "name": "Git & GitHub Bootcamp",
        "category": "Workshop",
        "icon": "git-branch",
        "tagline": "Master version control",
        "description": "Hands-on Git workshop.",
        "rules": ["Laptop mandatory"],
        "skills": ["Version Control"],
        "poster": "event_git.png",
    },
    "coding-marathon": {
        "id": "coding-marathon",
        "name": "Coding Marathon",
        "category": "Technical",
        "icon": "terminal",
        "tagline": "Code against the clock",
        "description": "Solve algorithmic challenges.",
        "rules": ["No internet"],
        "skills": ["Algorithms"],
        "poster": "event_coding.png",
    },
    "startup-pitch": {
        "id": "startup-pitch",
        "name": "Startup Pitch",
        "category": "Business",
        "icon": "rocket",
        "tagline": "Ignite your venture",
        "description": "Pitch your startup idea.",
        "rules": ["5-minute pitch"],
        "skills": ["Entrepreneurship"],
        "poster": "event_startup.png",
    },
    "tech-quiz": {
        "id": "tech-quiz",
        "name": "Tech Quiz",
        "category": "Fun & Tech",
        "icon": "help-circle",
        "tagline": "Test your tech trivia",
        "description": "Competitive tech quiz.",
        "rules": ["Teams of 2"],
        "skills": ["Quick Thinking"],
        "poster": "event_quiz.png",
    },
    "contribution-drive": {
        "id": "contribution-drive",
        "name": "OS Contribution Drive",
        "category": "Open Source",
        "icon": "heart-handshake",
        "tagline": "Give back to code",
        "description": "Make your first open-source PR.",
        "rules": ["Valid PRs only"],
        "skills": ["Open Source"],
        "poster": "event_contribution.png",
    },
}

# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", events=EVENTS)

@app.route("/event/<event_id>")
def event_detail(event_id):
    event = EVENTS.get(event_id)
    if not event:
        flash("Event not found!", "error")
        return redirect(url_for("index"))
    return render_template("event_detail.html", event=event)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            full_name = request.form.get("full_name")
            register_number = request.form.get("register_number")
            department = request.form.get("department")
            year = request.form.get("year")
            college_name = request.form.get("college_name")
            event_id = request.form.get("event")
            email = request.form.get("email")
            phone = request.form.get("phone")

            if not all([full_name, register_number, department, year, college_name, event_id, email, phone]):
                flash("All fields are required!", "error")
                return redirect(url_for("register"))

            event_name = EVENTS.get(event_id, {}).get("name", event_id)

            new_reg = Registration(
                full_name=full_name,
                register_number=register_number,
                department=department,
                year=year,
                college_name=college_name,
                event=event_name,
                email=email,
                phone=phone,
            )

            db.session.add(new_reg)
            db.session.commit()
            return redirect(url_for("success"))

        except Exception:
            db.session.rollback()
            flash("Registration failed. Try again.", "error")
            return redirect(url_for("register"))

    return render_template("register.html", events=EVENTS)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        flash("Invalid password", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
@login_required
def admin():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    return render_template("admin.html", registrations=registrations)

@app.route("/download_csv")
@login_required
def download_csv():
    registrations = Registration.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Full Name", "Register Number", "Department", "Year",
                     "College Name", "Event", "Email", "Phone", "Created At"])

    for r in registrations:
        writer.writerow([
            r.id, r.full_name, r.register_number, r.department,
            r.year, r.college_name, r.event, r.email, r.phone, r.created_at
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=registrations.csv"},
    )

# -------------------------------------------------
# Local Run (NOT USED BY RENDER)
# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
