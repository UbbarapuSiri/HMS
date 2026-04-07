from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, date
from database import db, User, Patient, Appointment, Prescription

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    # Add default users if none exist
    if User.query.count() == 0:
        default_users = [
            User(username='reception1', password='pass123', role='receptionist', hospital='City Hospital'),
            User(username='reception2', password='pass123', role='receptionist', hospital='Memorial Medical Center'),
            User(username='doctor1', password='doc123', role='doctor', hospital='City Hospital', specialization='Cardiologist'),
            User(username='doctor2', password='doc123', role='doctor', hospital='City Hospital', specialization='Neurologist'),
            User(username='doctor3', password='doc123', role='doctor', hospital='Memorial Medical Center', specialization='Orthopedic'),
            User(username='doctor4', password='doc123', role='doctor', hospital='Memorial Medical Center', specialization='Pediatrician'),
        ]
        for user in default_users:
            db.session.add(user)
        db.session.commit()

# Hospitals list for dropdown
HOSPITALS = ['City Hospital', 'Memorial Medical Center', 'St. Mary\'s Hospital', 'General Hospital']

# Doctor specializations
SPECIALIZATIONS = ['Cardiologist', 'Neurologist', 'Orthopedic', 'Pediatrician', 'General Practitioner', 'Dermatologist']

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'receptionist':
            return redirect(url_for('receptionist_dashboard'))
        else:
            return redirect(url_for('doctor_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hospital = request.form['hospital']
        
        user = User.query.filter_by(username=username, password=password, hospital=hospital).first()
        
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['hospital'] = user.hospital
            
            if user.role == 'receptionist':
                return redirect(url_for('receptionist_dashboard'))
            else:
                return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid credentials! Check username, password, or hospital.', 'error')
    
    return render_template('login.html', hospitals=HOSPITALS)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/receptionist')
def receptionist_dashboard():
    if 'user_id' not in session or session['role'] != 'receptionist':
        flash('Please login as receptionist.', 'error')
        return redirect(url_for('login'))
    
    # Get all patients for this hospital
    patients = Patient.query.filter_by(hospital=session['hospital']).order_by(Patient.admitted_datetime.desc()).all()
    
    # Get all available doctors for this hospital
    doctors_objs = User.query.filter_by(role='doctor', hospital=session['hospital']).all()
    
    # Serialize doctors for JSON
    doctors = [{'id': d.id, 'username': d.username, 'specialization': d.specialization} for d in doctors_objs]
    
    # Get available time slots (next 7 days, hourly slots)
    time_slots = []
    from datetime import timedelta
    current = datetime.now()
    for i in range(168):  # 7 days * 24 hours
        slot_time = current + timedelta(hours=i)
        if slot_time.hour >= 8 and slot_time.hour <= 17:  # Only working hours
            time_slots.append(slot_time.strftime('%Y-%m-%dT%H:00'))
    
    return render_template('receptionist_dashboard.html', patients=patients, doctors=doctors, 
                          hospital=session['hospital'], time_slots=time_slots, specializations=SPECIALIZATIONS)

@app.route('/get_doctors', methods=['POST'])
def get_doctors():
    """API endpoint to get doctors by hospital and specialization"""
    data = request.get_json()
    hospital = data.get('hospital')
    specialization = data.get('specialization')
    
    query = User.query.filter_by(role='doctor', hospital=hospital)
    if specialization:
        query = query.filter_by(specialization=specialization)
    
    doctors = query.all()
    return jsonify([{'id': d.id, 'username': d.username, 'specialization': d.specialization} for d in doctors])

@app.route('/check_doctor_availability', methods=['POST'])
def check_doctor_availability():
    """Check if doctor is available at given time"""
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    appointment_time = data.get('appointment_time')
    
    existing = Appointment.query.filter_by(
        doctor_user_id=doctor_id,
        appointment_time=appointment_time,
        status='admitted'  # Only check active appointments
    ).first()
    
    return jsonify({'available': existing is None})

@app.route('/admit_patient', methods=['POST'])
def admit_patient():
    if 'user_id' not in session or session['role'] != 'receptionist':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('login'))
    
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    problem = request.form.get('problem', '').strip()
    appointment_time = request.form.get('appointment_time', '').strip()
    doctor_id = request.form.get('doctor', '').strip()
    
    # Validate required fields
    if not name or not age or not problem or not appointment_time or not doctor_id:
        flash('All fields are required!', 'error')
        return redirect(url_for('receptionist_dashboard'))
    
    # Validate age
    try:
        age = int(age)
        if age < 0 or age > 120:
            flash('Age must be between 0 and 120.', 'error')
            return redirect(url_for('receptionist_dashboard'))
    except ValueError:
        flash('Age must be a valid number.', 'error')
        return redirect(url_for('receptionist_dashboard'))
    
    # Get doctor and verify it's from same hospital
    try:
        doctor_id = int(doctor_id)
        doctor = User.query.get(doctor_id)
        if not doctor or doctor.role != 'doctor' or doctor.hospital != session['hospital']:
            flash('Selected doctor not found or not in your hospital.', 'error')
            return redirect(url_for('receptionist_dashboard'))
    except ValueError:
        flash('Invalid doctor selection.', 'error')
        return redirect(url_for('receptionist_dashboard'))
    
    # Check for double booking (same doctor, same time)
    existing_appointment = Appointment.query.filter_by(
        doctor_user_id=doctor.id,
        appointment_time=appointment_time,
        status='admitted'  # Only check active appointments
    ).first()
    
    if existing_appointment:
        flash(f'Dr. {doctor.username} ({doctor.specialization}) is already booked at {appointment_time}. Choose another time.', 'error')
        return redirect(url_for('receptionist_dashboard'))
    
    # Create new patient
    new_patient = Patient(
        name=name,
        age=age,
        problem=problem,
        hospital=session['hospital'],
        admitted_datetime=datetime.now()
    )
    db.session.add(new_patient)
    db.session.flush()  # Get the patient ID
    
    # Create appointment
    new_appointment = Appointment(
        patient_id=new_patient.id,
        doctor_user_id=doctor.id,
        appointment_time=appointment_time,
        status='admitted'
    )
    db.session.add(new_appointment)
    db.session.commit()
    
    flash(f'✅ Patient {name} admitted successfully! Appointment with Dr. {doctor.username} at {appointment_time}', 'success')
    return redirect(url_for('receptionist_dashboard'))

@app.route('/doctor')
def doctor_dashboard():
    if 'user_id' not in session or session['role'] != 'doctor':
        flash('Please login as doctor.', 'error')
        return redirect(url_for('login'))
    
    # Get today's date for filtering
    today_str = date.today().strftime('%Y-%m-%d')
    
    # Get appointments for this doctor
    appointments = Appointment.query.filter_by(
        doctor_user_id=session['user_id']
    ).order_by(Appointment.appointment_time.desc()).all()
    
    # Get patient details for each appointment
    patients_data = []
    for apt in appointments:
        patient = Patient.query.get(apt.patient_id)
        # Check if appointment is today (simple contains check)
        is_today = today_str in apt.appointment_time if apt.appointment_time else False
        
        # Check if prescription already written
        prescription = Prescription.query.filter_by(patient_id=patient.id, doctor_user_id=session['user_id']).first()
        
        patients_data.append({
            'appointment_id': apt.id,
            'patient_id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'problem': patient.problem,
            'appointment_time': apt.appointment_time,
            'status': apt.status,
            'is_today': is_today,
            'has_prescription': prescription is not None
        })
    
    # Sort by appointment time (today first)
    patients_data.sort(key=lambda x: (not x['is_today'], x['appointment_time'] or ''))
    
    return render_template('doctor_dashboard.html', patients=patients_data, hospital=session['hospital'])

@app.route('/prescription/<int:appointment_id>')
def prescription_form(appointment_id):
    if 'user_id' not in session or session['role'] != 'doctor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify this appointment belongs to logged-in doctor
    if appointment.doctor_user_id != session['user_id']:
        flash('You can only write prescriptions for your own patients.', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    patient = Patient.query.get(appointment.patient_id)
    
    # Get existing prescriptions for this patient
    existing_prescriptions = Prescription.query.filter_by(patient_id=patient.id).order_by(Prescription.created_at.desc()).all()
    
    return render_template('prescription.html', patient=patient, appointment=appointment, prescriptions=existing_prescriptions)

@app.route('/save_prescription', methods=['POST'])
def save_prescription():
    if 'user_id' not in session or session['role'] != 'doctor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('login'))
    
    appointment_id = request.form.get('appointment_id', '')
    diagnosis = request.form.get('diagnosis', '').strip()
    medicines = request.form.get('medicines', '').strip()
    notes = request.form.get('notes', '').strip()
    
    # Validation
    if not diagnosis or not medicines:
        flash('Diagnosis and medicines are required!', 'error')
        return redirect(url_for('prescription_form', appointment_id=appointment_id))
    
    try:
        appointment_id = int(appointment_id)
        appointment = Appointment.query.get_or_404(appointment_id)
    except ValueError:
        flash('Invalid appointment ID.', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    if appointment.doctor_user_id != session['user_id']:
        flash('Unauthorized.', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    new_prescription = Prescription(
        patient_id=appointment.patient_id,
        doctor_user_id=session['user_id'],
        diagnosis=diagnosis,
        medicines=medicines,
        notes=notes
    )
    
    # Update appointment status
    appointment.status = 'treated'
    
    db.session.add(new_prescription)
    db.session.commit()
    
    flash('💾 Prescription saved successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)