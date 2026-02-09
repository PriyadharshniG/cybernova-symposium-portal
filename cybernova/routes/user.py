from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Registration
from .main import EVENTS

user_bp = Blueprint('user', __name__)

@user_bp.route("/register", methods=["GET", "POST"])
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
                return redirect(url_for("user.register"))

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
            return redirect(url_for("main.success", reg_id=new_reg.id))

        except Exception:
            db.session.rollback()
            flash("Registration failed. Try again.", "error")
            return redirect(url_for("user.register"))

    return render_template("register.html", events=EVENTS)

@user_bp.route("/id-card/<int:reg_id>")
def id_card(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    return render_template("id_card.html", reg=reg)

@user_bp.route("/certificate/<int:reg_id>")
def certificate(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    return render_template("certificate.html", reg=reg)

@user_bp.route("/submit", methods=["GET", "POST"])
def submit_abstract():
    from werkzeug.utils import secure_filename
    from ..models import AbstractSubmission
    import os
    from flask import current_app

    if request.method == "POST":
        reg_id = request.form.get("registration_id")
        file = request.files.get("abstract_file")

        if not reg_id or not file:
            flash("All fields are required!", "error")
            return redirect(url_for("user.submit_abstract"))

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(f"abstract_{reg_id}_{file.filename}")
            upload_dir = os.path.join(current_app.root_path, '../uploads/abstracts')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            new_submission = AbstractSubmission(
                registration_id=reg_id,
                file_path=filename
            )
            db.session.add(new_submission)
            db.session.commit()
            flash("Abstract submitted successfully!", "success")
            return redirect(url_for("main.success", reg_id=reg_id))
        else:
            flash("Only PDF files are allowed!", "error")

    return render_template("submit_abstract.html")

@user_bp.route("/portal", methods=["GET", "POST"])
def portal():
    if request.method == "POST":
        reg_id = request.form.get("reg_id")
        reg = Registration.query.get(reg_id)
        if reg:
            return redirect(url_for("user.dashboard", reg_id=reg.id))
        else:
            flash("Invalid Registration ID. Please check your ID.", "error")
            return redirect(url_for("user.portal"))
    return render_template("participant_portal.html")

@user_bp.route("/dashboard/<int:reg_id>")
def dashboard(reg_id):
    reg = Registration.query.get_or_404(reg_id)
    return render_template("participant_dashboard.html", reg=reg)
