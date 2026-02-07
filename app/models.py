from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    owner_name = db.Column(db.String(255))
    owner_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    medical_records = db.relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    specialty = db.Column(db.String(100))

    appointments = db.relationship("Appointment", back_populates="doctor")

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="scheduled")

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    medical_record = db.relationship("MedicalRecord", back_populates="appointment", uselist=False)

class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    notes = db.Column(db.Text)

    patient = db.relationship("Patient", back_populates="medical_records")
    appointment = db.relationship("Appointment", back_populates="medical_record")