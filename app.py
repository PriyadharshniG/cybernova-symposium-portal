import csv
import io
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from werkzeug.security import check_password_hash
from config import Config
from models import db, Registration

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# --- Helpers ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Data ---

EVENTS = {
    'hackathon': {
        'id': 'hackathon',
        'name': 'Open Source Hackathon',
        'category': 'Flagship Event',
        'icon': 'code-2',
        'tagline': 'Build for the Community',
        'description': 'A 24-hour intense coding marathon where participants collaborate to build open-source solutions for real-world problems. Mentored by VGLUG Foundation experts.',
        'rules': ['Team size: 2-4 members', 'Open source tools only', 'Code must be pushed to GitHub', 'Hardware hacks allowed'],
        'skills': ['Teamwork', 'Open Source Contribution', 'Rapid Prototyping'],
        'poster': 'event_hackathon.png'
    },
    'paper-presentation': {
        'id': 'paper-presentation',
        'name': 'Paper Presentation',
        'category': 'Technical',
        'icon': 'file-text',
        'tagline': 'Innovate & articulate',
        'description': 'Present your research ideas on emerging technologies like AI, Blockchain, and Edge Computing. Best papers get published in our symposium journal.',
        'rules': ['Abstract submission deadline: 10th March', 'Time limit: 7 mins + 3 mins Q&A', 'Original work only'],
        'skills': ['Public Speaking', 'Research', 'Technical Writing'],
        'poster': 'event_paper_pres.png'
    },
    'web-dev': {
        'id': 'web-dev',
        'name': 'Web Dev Challenge',
        'category': 'Technical',
        'icon': 'layout',
        'tagline': 'Craft the digital future',
        'description': 'Design and build stunning, responsive web applications. Theme will be announced on the spot.',
        'rules': ['Individual participation', 'Frameworks allowed: React, Vue, Flask', ' judging based on UI/UX and Code Quality'],
        'skills': ['Frontend/Backend', 'UI/UX', 'Deployment'],
        'poster': 'event_web_dev.png'
    },
    'ai-ideathon': {
        'id': 'ai-ideathon',
        'name': 'AI & ML Ideathon',
        'category': 'Innovation',
        'icon': 'brain-circuit',
        'tagline': 'Think. Train. Deploy.',
        'description': 'Pitch your AI-driven startup ideas or solutions. Focus on ethical AI and social impact.',
        'rules': ['Presentation format: PPT/Prototype', 'Focus on feasibility and impact'],
        'skills': ['AI Strategy', 'Problem Solving', 'Pitching'],
        'poster': 'event_ai_ml.png'
    },
    'ui-ux': {
        'id': 'ui-ux',
        'name': 'UI/UX Design Sprint',
        'category': 'Design',
        'icon': 'pen-tool',
        'tagline': 'Design with empathy',
        'description': 'Create user-centric designs for mobile or web apps. Focus on accessibility and aesthetics.',
        'rules': ['Tools: Figma, Adobe XD', '3 hours duration'],
        'skills': ['Design Thinking', 'Prototyping', 'Wireframing'],
        'poster': 'event_ui_ux.png'
    },
    'git-bootcamp': {
        'id': 'git-bootcamp',
        'name': 'Git & GitHub Bootcamp',
        'category': 'Workshop',
        'icon': 'git-branch',
        'tagline': 'Master version control',
        'description': 'A hands-on workshop to master Git commands, branching, merging, and open source contribution workflows.',
        'rules': ['Laptop mandatory', 'Beginner friendly'],
        'skills': ['Version Control', 'Collaboration', 'Git CLI'],
        'poster': 'event_git.png'
    },
    'coding-marathon': {
        'id': 'coding-marathon',
        'name': 'Coding Marathon',
        'category': 'Technical',
        'icon': 'terminal',
        'tagline': 'Code against the clock',
        'description': 'Solve algorithmic challenges of increasing difficulty. Test your logic and speed.',
        'rules': ['Languages: C, C++, Python, Java', 'No internet for code snippets'],
        'skills': ['Algorithms', 'Data Structures', 'Logic'],
        'poster': 'event_coding.png'
    },
    'startup-pitch': {
        'id': 'startup-pitch',
        'name': 'Startup Pitch',
        'category': 'Business',
        'icon': 'rocket',
        'tagline': 'Ignite your venture',
        'description': 'Pitch your startup idea to a panel of investors and entrepreneurs.',
        'rules': ['5 minutes pitch', 'Business model canvas required'],
        'skills': ['Entrepreneurship', 'Market Analysis', 'Presentation'],
        'poster': 'event_startup.png'
    },
    'tech-quiz': {
        'id': 'tech-quiz',
        'name': 'Tech Quiz',
        'category': 'Fun & Tech',
        'icon': 'help-circle',
        'tagline': 'Test your tech trivia',
        'description': 'A fun and competitive quiz covering latest tech trends, history, and gadgets.',
        'rules': ['Teams of 2', 'Buzzer round finals'],
        'skills': ['General Tech Knowledge', 'Quick Thinking'],
        'poster': 'event_quiz.png'
    },
    'contribution-drive': {
        'id': 'contribution-drive',
        'name': 'OS Contribution Drive',
        'category': 'Open Source',
        'icon': 'heart-handshake',
        'tagline': 'Give back to code',
        'description': 'Live contribution to popular open source repositories. Get your first PR merged!',
        'rules': ['Valid PRs only', 'Mentors will assist'],
        'skills': ['Open Source', 'Communication', 'Legacy Code'],
        'poster': 'event_contribution.png'
    }
}

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html', events=EVENTS)

@app.route('/event/<event_id>')
def event_detail(event_id):
    event = EVENTS.get(event_id)
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('index'))
    return render_template('event_detail.html', event=event)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            register_number = request.form['register_number']
            department = request.form['department']
            year = request.form['year']
            college_name = request.form['college_name']
            event_id = request.form['event'] # Updated to receive ID
            email = request.form['email']
            phone = request.form['phone']
            
            event_name = EVENTS.get(event_id, {}).get('name', event_id)

            if not all([full_name, register_number, department, year, college_name, event_id, email, phone]):
                flash('All fields are required!', 'error')
                return redirect(url_for('register'))

            new_reg = Registration(
                full_name=full_name,
                register_number=register_number,
                department=department,
                year=year,
                college_name=college_name,
                event=event_name, # Storing name for now
                email=email,
                phone=phone
            )
            
            db.session.add(new_reg)
            db.session.commit()
            
            return redirect(url_for('success'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('register'))

    return render_template('register.html', events=EVENTS)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid password', 'error')
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    return render_template('admin.html', registrations=registrations)

@app.route('/download_csv')
@login_required
def download_csv():
    registrations = Registration.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['ID', 'Full Name', 'Register Number', 'Department', 'Year', 'College Name', 'Event', 'Email', 'Phone', 'Created At'])
    
    # Data
    for reg in registrations:
        writer.writerow([
            reg.id, 
            reg.full_name, 
            reg.register_number, 
            reg.department, 
            reg.year, 
            reg.college_name, 
            reg.event, 
            reg.email, 
            reg.phone, 
            reg.created_at
        ])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=registrations.csv"}
    )

# --- CLI & Init ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Auto-create tables
    app.run(debug=True)
