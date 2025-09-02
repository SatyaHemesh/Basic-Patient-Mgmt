from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, RegisterForm, PatientForm, VisitForm
from models import db, User, Patient, Visit
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- AUTH -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

# ---------------- PATIENT CRUD -----------------
@app.route("/patients")
@login_required
def list_patients():
    patients = Patient.query.order_by(Patient.name).all()
    return render_template("patients_list.html", patients=patients)

@app.route("/patients/add", methods=["GET", "POST"])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(patient)
        db.session.commit()
        flash("Patient added successfully!", "success")
        return redirect(url_for("list_patients"))
    return render_template("patient_form.html", form=form, title="Add Patient")

@app.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash("Patient updated successfully!", "success")
        return redirect(url_for("list_patients"))
    return render_template("patient_form.html", form=form, title="Edit Patient")

@app.route("/patients/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted successfully!", "success")
    return redirect(url_for("list_patients"))

# ---------------- VISIT CRUD -----------------
@app.route("/patients/<int:patient_id>/visits")
@login_required
def patient_visits(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("visits_list.html", patient=patient, visits=patient.visits)

@app.route("/patients/<int:patient_id>/visits/add", methods=["GET", "POST"])
@login_required
def add_visit(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(
            patient_id=patient.id,
            reason=form.reason.data,
            diagnosis=form.diagnosis.data,
            treatment=form.treatment.data,
            fees_paid=form.fees_paid.data or 0.0
        )
        db.session.add(visit)
        db.session.commit()
        flash("Visit added successfully!", "success")
        return redirect(url_for("patient_visits", patient_id=patient.id))
    return render_template("visit_form.html", form=form, title="Add Visit", patient=patient)

@app.route("/visits/<int:visit_id>/edit", methods=["GET", "POST"])
@login_required
def edit_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    form = VisitForm(obj=visit)
    if form.validate_on_submit():
        form.populate_obj(visit)
        db.session.commit()
        flash("Visit updated successfully!", "success")
        return redirect(url_for("patient_visits", patient_id=visit.patient_id))
    return render_template("visit_form.html", form=form, title="Edit Visit", patient=visit.patient)

@app.route("/visits/<int:visit_id>/delete", methods=["POST"])
@login_required
def delete_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient_id = visit.patient_id
    db.session.delete(visit)
    db.session.commit()
    flash("Visit deleted successfully!", "success")
    return redirect(url_for("patient_visits", patient_id=patient_id))

if __name__ == "__main__":
    app.run(debug=True)
