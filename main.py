from server import ClinicHandler
from http.server import ThreadingHTTPServer
from database import ClinicDatabase

def main():
    db = ClinicDatabase()
    server_address = ('', 8502)
    httpd = ThreadingHTTPServer(server_address, ClinicHandler)
    print(f"Server running on port {server_address[1]}...")
    httpd.serve_forever()

if __name__ == '__main__':
    main() 