from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import db, Patient

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return redirect(url_for("main.patients_list"))

@bp.route("/patients")
def patients_list():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template("patients_list.html", patients=patients)

@bp.route("/patients/new", methods=["GET", "POST"])
def patient_create():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        species = request.form.get("species")
        breed = request.form.get("breed")
        birth_date = request.form.get("birth_date")
        owner_name = request.form.get("owner_name")
        owner_phone = request.form.get("owner_phone")

        if not full_name or not species:
            flash("Имя пациента и вид обязательны")
            return redirect(url_for("main.patient_create"))

        birth_date_obj = None
        if birth_date:
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

        patient = Patient(
            full_name=full_name,
            species=species,
            breed=breed,
            birth_date=birth_date_obj,
            owner_name=owner_name,
            owner_phone=owner_phone,
        )
        db.session.add(patient)
        db.session.commit()
        flash("Пациент успешно создан")
        return redirect(url_for("main.patients_list"))

    return render_template("patient_form.html", patient=None)

@bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
def patient_edit(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        patient.full_name = request.form.get("full_name")
        patient.species = request.form.get("species")
        patient.breed = request.form.get("breed")
        birth_date = request.form.get("birth_date")
        patient.birth_date = (
            datetime.strptime(birth_date, "%Y-%m-%d").date() if birth_date else None
        )
        patient.owner_name = request.form.get("owner_name")
        patient.owner_phone = request.form.get("owner_phone")

        db.session.commit()
        flash("Данные пациента обновлены")
        return redirect(url_for("main.patients_list"))

    return render_template("patient_form.html", patient=patient)

@bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
def patient_delete(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Пациент удалён")
    return redirect(url_for("main.patients_list"))
