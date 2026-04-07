from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # receptionist or doctor
    hospital = db.Column(db.String(200), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)  # For doctors: Cardiologist, Neurologist, etc.
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, foreign_keys='Appointment.doctor_user_id')
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True, foreign_keys='Prescription.doctor_user_id')

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hospital = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.String(300), nullable=False)  # Chief complaint/problem
    admitted_datetime = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True, cascade='all, delete-orphan')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_time = db.Column(db.String(100), nullable=False)  # Store as string for simplicity
    status = db.Column(db.String(50), default='admitted')  # admitted, treated, discharged
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships are auto-created by backref in User and Patient

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships are auto-created by backref in User and Patient