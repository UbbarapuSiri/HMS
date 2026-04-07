# Hospital Management System

A comprehensive web-based hospital management system built with Flask and SQLite. This application streamlines patient admission, doctor appointments, and prescription management.

## 🎯 Features Implemented

### 1. **Authentication System**
- **Receptionist Login**: Manage patient admissions (Username: `reception1`, Password: `pass123`)
- **Doctor Login**: View assigned patients and write prescriptions (Username: `doctor1`, Password: `doc123`)
- Hospital selection from dropdown during login
- Secure session management with role-based access control

### 2. **Receptionist Module**
After login, receptionists can:
- ✅ **Admit New Patients**: 
  - Enter patient name, age, and chief complaint/problem
  - Select doctor specialization from dropdown
  - System dynamically filters doctors based on specialization
  - Choose available appointment time
  - Prevent double-booking (same doctor cannot be assigned at the same time)

- ✅ **View Patient List**:
  - See all patients admitted in the hospital
  - Display patient name, age, problem, and admission time
  - Scrollable patient table for easy navigation

### 3. **Doctor Module**
After login, doctors can:
- ✅ **View Assigned Patients**:
  - See all patients assigned to them
  - Display patient details: name, age, chief complaint
  - View appointment time and current status
  - Status indicator: "Admitted" (yellow) or "Treated" (green)
  - "Today" badge for today's appointments

- ✅ **Write Prescriptions**:
  - View patient information (name, age, hospital, problem, appointment time)
  - Fill in diagnosis (up to 1000 characters)
  - Add medicines with dosage and frequency (up to 2000 characters)
  - Add optional notes/instructions (up to 500 characters)
  - Save prescriptions to database

- ✅ **View Prescription History**:
  - Access previous prescriptions for patient
  - Display diagnosis, medicines, and notes
  - Timestamp for each prescription

### 4. **Database Design**
Complete relational database with 4 tables:

**Users Table**
```
id, username, password, role, hospital, specialization, created_at
```

**Patients Table**
```
id, name, age, hospital, problem, admitted_datetime
```

**Appointments Table**
```
id, patient_id, doctor_user_id, appointment_time, status, created_at
```

**Prescriptions Table**
```
id, patient_id, doctor_user_id, diagnosis, medicines, notes, created_at
```

### 5. **Validation Features**
- ✅ Required fields must not be empty
- ✅ Age validation (0-120 years)
- ✅ No duplicate doctor booking at same time
- ✅ Doctor must be from same hospital
- ✅ Only doctors can see their patients
- ✅ Only doctors can write prescriptions for their patients
- ✅ Character limits on prescription fields

### 6. **User Interface**
- **Clean, Modern Design**: Gradient purple background with white cards
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: 
  - Dynamic doctor filtering by specialization
  - Real-time availability status
  - Hover effects on buttons and cards
  - Color-coded status indicators
- **Professional Color Scheme**: Purple primary (#667eea), green success (#48bb78), red danger (#f56565)
- **Accessibility**: Clear labels, required field indicators, helpful placeholder text

## 📊 Pre-loaded Demo Data

### Receptionist Accounts
- Username: `reception1` / Password: `pass123` (City Hospital)
- Username: `reception2` / Password: `pass123` (Memorial Medical Center)

### Doctor Accounts
- Username: `doctor1` / Password: `doc123` (City Hospital, Cardiologist)
- Username: `doctor2` / Password: `doc123` (City Hospital, Neurologist)
- Username: `doctor3` / Password: `doc123` (Memorial Medical Center, Orthopedic)
- Username: `doctor4` / Password: `doc123` (Memorial Medical Center, Pediatrician)

## 🏥 Available Hospitals
1. City Hospital
2. Memorial Medical Center
3. St. Mary's Hospital
4. General Hospital

## 🔧 Technologies Used
- **Frontend**: HTML5, CSS3 (Responsive Design)
- **Backend**: Flask (Python Web Framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Session Management**: Flask Sessions

## 📁 Project Structure
```
hospital_management/
├── app.py                          # Main Flask application
├── database.py                     # Database models and initialization
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── instance/
│   └── hospital.db                # SQLite database (auto-created)
├── static/
│   └── style.css                  # Complete styling
└── templates/
    ├── login.html                 # Login page
    ├── receptionist_dashboard.html # Receptionist interface
    ├── doctor_dashboard.html        # Doctor interface
    └── prescription.html            # Prescription form
```

## 🚀 Getting Started

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🔐 Security Notes
- The secret key in app.py should be changed in production
- Passwords are stored in plain text (for demo purposes only)
- Implement proper password hashing in production (use werkzeug.security)
- Always use HTTPS in production

## 📝 Prescription Format Example
When entering medicines, use this format:
```
1. Aspirin - 500mg - Twice daily for 5 days
2. Paracetamol - 650mg - Once daily after meals
3. Amoxicillin - 250mg - Thrice daily for 7 days
```

## 🎓 How to Use

### As a Receptionist:
1. Login with receptionist credentials
2. Select a non-empty specialization (Cardiologist, Neurologist, etc.)
3. Choose a doctor from the filtered list
4. Select an available appointment time
5. Click "Admit Patient" to save

### As a Doctor:
1. Login with doctor credentials
2. View your assigned patients on the dashboard
3. Click "Write Prescription" to add diagnosis and medicines
4. View prescription history on the right side
5. Update or view prescriptions anytime

## ✨ Key Features Highlight
- **Dynamic Doctor Filtering**: Select specialization → automatically shows available doctors
- **Double-Booking Prevention**: System prevents assigning same doctor at same time
- **Status Tracking**: Monitor patient status from admitted to treated
- **Prescription Management**: Complete prescription history per patient
- **Hospital Isolation**: Doctors and patients are filtered by hospital
- **Responsive Design**: Works seamlessly on all screen sizes

## 🐛 Future Enhancement Ideas
- Email notifications for appointments
- Patient discharge functionality
- Billing system integration
- Appointment rescheduling
- Patient medical history
- Drug interaction checker
- SMS reminders
- Admin dashboard
- Real-time availability calendar

## 📞 Support
For issues or questions, review the validation messages and ensure:
- All required fields are filled
- Hospital selection matches your credentials
- Age is between 0-120
- Appointment time is in the future

---

**System Status**: ✅ Fully Functional and Ready to Use

Last Updated: April 7, 2026
