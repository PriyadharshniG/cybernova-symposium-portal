import os
from flask import Flask
from config import Config
from .models import db

def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    app.config.from_object(Config)

    # Required for SQLite on Render
    os.makedirs("instance", exist_ok=True)

    db.init_app(app)

    with app.app_context():
        # Register Blueprints
        from .routes.main import main_bp
        from .routes.admin import admin_bp
        from .routes.user import user_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(user_bp, url_prefix='/user')

        db.create_all()
        seed_data()

    return app

def seed_data():
    from .models import Sponsor, Announcement, Leaderboard
    if not Sponsor.query.first():
        sponsors = [
            Sponsor(name="TechCorp", logo_url="circuit-board", tier="platinum", website="#"),
            Sponsor(name="InnovateX", logo_url="atom", tier="gold", website="#"),
            Sponsor(name="DevStudio", logo_url="binary", tier="silver", website="#"),
            Sponsor(name="CloudSystems", logo_url="server", tier="platinum", website="#"),
            Sponsor(name="CyberDefense", logo_url="fingerprint", tier="gold", website="#"),
        ]
        db.session.bulk_save_objects(sponsors)
        
        announcements = [
            Announcement(title="Hackathon Registration Open!", content="Register now for the 24-hour hackathon. limited seats available.", priority="critical", is_alert=True),
            Announcement(title="Guest Speaker: Dr. AI", content="Join us for a session on the future of AI at 10:00 AM.", priority="event"),
            Announcement(title="Lunch Break", content="Lunch will be served at the cafeteria from 1:00 PM to 2:00 PM.", priority="info"),
        ]
        db.session.bulk_save_objects(announcements)

        leaderboard = [
            Leaderboard(event_id="hackathon", team_name="CodeWizards", score=95, college="MIT", rank=1),
            Leaderboard(event_id="hackathon", team_name="BinaryBosses", score=90, college="Stanford", rank=2),
            Leaderboard(event_id="hackathon", team_name="PyThons", score=85, college="Harvard", rank=3),
            Leaderboard(event_id="hackathon", team_name="ScriptKiddies", score=80, college="IIT", rank=4),
            Leaderboard(event_id="web-dev", team_name="PixelPerfect", score=98, college="Anna Univ", rank=1),
        ]
        db.session.bulk_save_objects(leaderboard)
        
        db.session.commit()
