from database import User, Patient, Appointment, Prescription
from app import app
with app.app_context():
    print('users:')
    for u in User.query.order_by(User.id).all():
        print(u.id, u.username, u.role, u.hospital, u.specialization)
    print('patients:', Patient.query.count())
    print('appointments:', Appointment.query.count())
    print('prescriptions:', Prescription.query.count())
