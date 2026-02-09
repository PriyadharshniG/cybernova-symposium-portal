import io
import csv
from functools import wraps
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, Response
)
from ..models import Registration

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    from flask import current_app
    if request.method == "POST":
        if request.form.get("password") == current_app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Invalid password", "error")
    return render_template("login.html")

@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))

@admin_bp.route("/")
@login_required
def dashboard():
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    return render_template("admin.html", registrations=registrations)

@admin_bp.route("/download_csv")
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

@admin_bp.route("/submissions")
@login_required
def submissions():
    from ..models import AbstractSubmission
    sub_list = AbstractSubmission.query.order_by(AbstractSubmission.submitted_at.desc()).all()
    return render_template("admin_submissions.html", submissions=sub_list)

@admin_bp.route("/analytics")
@login_required
def analytics():
    from ..models import db
    from sqlalchemy import func
    
    # Registration counts by event
    event_counts = db.session.query(Registration.event, func.count(Registration.id)).group_by(Registration.event).all()
    
    # Registration counts by department
    dept_counts = db.session.query(Registration.department, func.count(Registration.id)).group_by(Registration.department).all()
    
    total_regs = Registration.query.count()
    
    return render_template("admin_analytics.html", 
                           event_counts=event_counts, 
                           dept_counts=dept_counts, 
                           total_regs=total_regs)

@admin_bp.route("/scanner")
@login_required
def scanner():
    return render_template("admin_scanner.html")

@admin_bp.route("/scan/<int:reg_id>")
@login_required
def scan(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    # Success check-in logic
    flash(f"Check-in Successful for {reg.full_name}! (ID: {reg_id})", "success")
    return redirect(url_for("admin.scanner"))

