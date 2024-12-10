from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
import os
from database import ClinicDatabase

class ClinicHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = ClinicDatabase()
        super().__init__(*args, **kwargs)

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_cors_headers()
                self.end_headers()
                with open('html/index.html', 'rb') as f:
                    self.wfile.write(f.read())
            
            elif parsed_path.path == '/api/appointments':
                query = parse_qs(parsed_path.query)
                start_date = query.get('start_date', [None])[0]
                
                if start_date:
                    appointments = self.db.get_week_appointments(start_date)
                    print(f"Debug - Start date: {start_date}")
                    print(f"Debug - Appointments found: {appointments}")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(appointments).encode('utf-8'))
                else:
                    self.send_error(400, "Missing start_date parameter")
                
            else:
                try:
                    file_path = os.path.join('html', parsed_path.path.lstrip('/'))
                    with open(file_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-type', self._get_content_type(file_path))
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(f.read())
                except FileNotFoundError:
                    self.send_error(404)
        except Exception as e:
            print(f"Error in do_GET: {str(e)}")
            self.send_error(500, str(e))

    def do_POST(self):
        try:
            if self.path == '/api/appointments':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                appointment_data = json.loads(post_data.decode('utf-8'))
                
                print(f"Debug - Received appointment data: {appointment_data}")
                
                self.db.add_appointment(
                    patient_name=appointment_data['patient_name'],
                    diagnosis=appointment_data['diagnosis'],
                    phone=appointment_data['phone'],
                    appointment_date=appointment_data['appointment_date'],
                    doctor=appointment_data['doctor']
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        except Exception as e:
            print(f"Error in do_POST: {str(e)}")
            self.send_error(500, str(e))

    def do_PUT(self):
        try:
            if self.path.startswith('/api/appointments/'):
                appointment_id = int(self.path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                appointment_data = json.loads(post_data.decode('utf-8'))
                
                print(f"Debug - Updating appointment {appointment_id} with data:", appointment_data)
                
                self.db.update_appointment(
                    appointment_id,
                    patient_name=appointment_data['patient_name'],
                    diagnosis=appointment_data['diagnosis'],
                    phone=appointment_data['phone'],
                    appointment_date=appointment_data['appointment_date'],
                    doctor=appointment_data['doctor']
                )
                
                print(f"Debug - Successfully updated appointment {appointment_id}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        except Exception as e:
            print(f"Error in do_PUT: {str(e)}")
            self.send_error(500, str(e))

    def do_DELETE(self):
        try:
            if self.path.startswith('/api/appointments/'):
                appointment_id = int(self.path.split('/')[-1])
                self.db.delete_appointment(appointment_id)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        except Exception as e:
            print(f"Error in do_DELETE: {str(e)}")
            self.send_error(500, str(e))

    def _get_content_type(self, path):
        if path.endswith('.html'):
            return 'text/html'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        return 'text/plain' 