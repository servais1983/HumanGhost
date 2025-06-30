import yaml
from core import host, send  # On retire 'create'

def run_script_yaml(path):
    print(f"[*] Chargement du scénario YAML : {path}")
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"[!] Erreur de lecture du fichier de scénario : {e}")
        return

    print(f"[*] Démarrage de la campagne : {config.get('name', 'Sans nom')}")

    # L'ordre est maintenant défini dans la config
    for step in config.get("steps", []):
        if step == "host":
            # Le serveur host est bloquant, il est préférable de le lancer en dernier ou en parallèle
            # Pour une exécution simple, on suppose qu'il est lancé et que l'utilisateur enverra l'email manuellement
            # ou via un autre terminal. Dans une version avancée, on utiliserait des threads.
            host.run(config)
        elif step == "send":
            send.run(config)
        else:
            print(f"[!] Étape inconnue dans le scénario : {step}")
