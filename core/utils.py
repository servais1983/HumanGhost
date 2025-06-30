import yaml
from core import host, send
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
            # On lance le serveur dans un thread et on continue
            server_thread = host.run_server_in_thread(config)
            print("[*] Le serveur tourne en arrière-plan...")
        elif step == "send":
            # On attend une seconde pour s'assurer que le serveur est bien démarré
            time.sleep(1)
            send.run(config)
        else:
            print(f"[!] Étape inconnue dans le scénario : {step}")
            
    # Si le serveur tourne, on garde le script principal en vie
    if server_thread and server_thread.is_alive():
        print("[+] Campagne en cours. Appuyez sur CTRL+C pour arrêter le serveur et quitter.")
        try:
            # Garde le script principal en attente
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Arrêt du serveur et fin de la campagne.")
