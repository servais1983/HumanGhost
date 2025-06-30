import yaml
from core import host, send, qr_generator # On ajoute qr_generator
import time

def run_script_yaml(path):
    print(f"[*] Chargement du scénario YAML : {path}")
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"[!] Erreur de lecture du fichier de scénario : {e}")
        return

    print(f"[*] Démarrage de la campagne : {config.get('name', 'Sans nom')}")
    
    server_thread = None
    
    for step in config.get("steps", []):
        if step == "host":
            server_thread = host.run_server_in_thread(config)
            print("[*] Le serveur tourne en arrière-plan...")
        elif step == "send":
            time.sleep(1) # Laisse le temps au serveur de démarrer
            send.run(config)
        elif step == "generate_qr":
            # On vérifie si la section qrcode est présente et activée
            qr_config = config.get('qrcode', {})
            if qr_config.get('enabled', False):
                url = config.get('email', {}).get('phishing_url', 'http://127.0.0.1:5000')
                filename = qr_config.get('output_filename', 'phishing_qr.png')
                qr_generator.create_qr_code(url, filename)
        else:
            print(f"[!] Étape inconnue dans le scénario : {step}")
            
    if server_thread and server_thread.is_alive():
        print("[+] Campagne en cours. Le QR code a été généré dans le dossier 'campaign_files'.")
        print("[+] Appuyez sur CTRL+C pour arrêter le serveur et quitter.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Arrêt du serveur et fin de la campagne.")
