import sqlite3
from datetime import datetime

class ClinicDatabase:
    def __init__(self, db_file="clinic.db"):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_name TEXT NOT NULL,
                        diagnosis TEXT,
                        phone TEXT,
                        appointment_date DATE,
                        doctor TEXT
                    )
                ''')
                print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise
    
    def add_appointment(self, patient_name, diagnosis, phone, appointment_date, doctor):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    INSERT INTO appointments 
                    (patient_name, diagnosis, phone, appointment_date, doctor)
                    VALUES (?, ?, ?, ?, ?)
                ''', (patient_name, diagnosis, phone, appointment_date, doctor))
                print(f"Added appointment: {patient_name} on {appointment_date}")
        except Exception as e:
            print(f"Error adding appointment: {str(e)}")
            raise
    
    def get_week_appointments(self, start_date):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM appointments 
                    WHERE appointment_date >= ? AND appointment_date < date(?, '+7 days')
                    ORDER BY appointment_date, doctor
                ''', (start_date, start_date))
                
                appointments = []
                for row in cursor:
                    appointments.append({
                        'id': row['id'],
                        'patient_name': row['patient_name'],
                        'diagnosis': row['diagnosis'],
                        'phone': row['phone'],
                        'appointment_date': row['appointment_date'],
                        'doctor': row['doctor']
                    })
                print(f"Retrieved {len(appointments)} appointments for week starting {start_date}")
                return appointments
        except Exception as e:
            print(f"Error getting appointments: {str(e)}")
            raise
    
    def delete_appointment(self, appointment_id):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
                print(f"Deleted appointment with ID: {appointment_id}")
        except Exception as e:
            print(f"Error deleting appointment: {str(e)}")
            raise
    
    def update_appointment(self, appointment_id, patient_name, diagnosis, phone, appointment_date, doctor):
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute('''
                    UPDATE appointments 
                    SET patient_name = ?, diagnosis = ?, phone = ?, 
                        appointment_date = ?, doctor = ?
                    WHERE id = ?
                ''', (patient_name, diagnosis, phone, appointment_date, doctor, appointment_id))
                print(f"Updated appointment with ID: {appointment_id}")
        except Exception as e:
            print(f"Error updating appointment: {str(e)}")
            raise