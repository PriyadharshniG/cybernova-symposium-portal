from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registration(db.Model):
    """
    Registration model for storing user details.
    """
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    register_number = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    college_name = db.Column(db.String(100), nullable=False)
    event = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Registration {self.full_name}>'
