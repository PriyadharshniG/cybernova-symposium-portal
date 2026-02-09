from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Sponsor, Announcement, Leaderboard

main_bp = Blueprint('main', __name__)

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

@main_bp.route("/")
def index():
    sponsors_list = Sponsor.query.all()
    # Sanitize logos: if they are URLs, fallback to a tech icon
    for s in sponsors_list:
        if s.logo_url.startswith("http"):
            s.logo_url = "activity"
    return render_template("index.html", events=EVENTS, sponsors=sponsors_list)

@main_bp.route("/event/<event_id>")
def event_detail(event_id):
    event = EVENTS.get(event_id)
    if not event:
        flash("Event not found!", "error")
        return redirect(url_for("main.index"))
    return render_template("event_detail.html", event=event)

@main_bp.route("/leaderboard")
def leaderboard():
    entries = Leaderboard.query.order_by(Leaderboard.score.desc()).all()
    return render_template("leaderboard.html", entries=entries)

@main_bp.route("/sponsors")
def sponsors():
    sponsors_list = Sponsor.query.all()
    for s in sponsors_list:
        if s.logo_url.startswith("http"):
            s.logo_url = "activity"
    return render_template("sponsors.html", sponsors=sponsors_list)

@main_bp.route("/announcements")
def announcements():
    ann = Announcement.query.order_by(Announcement.priority, Announcement.created_at.desc()).all()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.rank).all()
    return render_template("announcements.html", announcements=ann, leaderboard=leaderboard_data)

@main_bp.route("/success")
def success():
    reg_id = request.args.get('reg_id')
    return render_template("success.html", reg_id=reg_id)

@main_bp.route("/chat", methods=["POST"])
def chat():
    from ..chatbot import engine
    from flask import jsonify
    
    data = request.json
    user_msg = data.get("message", "")
    
    response = engine.get_response(user_msg)
    return jsonify({"response": response})
