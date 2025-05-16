from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def run():
    print("[*] Hébergement d'un faux site sur http://localhost:5000")
    os.chdir("templates")
    server = HTTPServer(('0.0.0.0', 5000), SimpleHTTPRequestHandler)
    server.serve_forever()