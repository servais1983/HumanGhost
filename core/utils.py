import yaml
from core import create, send, host

def run_script_yaml(path):
    print(f"[*] Chargement du scénario : {path}")
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    for step in data.get("steps", []):
        if step == "create":
            create.run()
        elif step == "send":
            send.run()
        elif step == "host":
            host.run()
        else:
            print(f"[!] Étape inconnue : {step}")