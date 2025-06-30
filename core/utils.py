import yaml
from core import host, send, qr_generator, llm_generator # On ajoute llm_generator
import time
import os

def run_script_yaml(path):
    print(f"[*] Chargement du scénario YAML : {path}")
    # ... (le chargement du fichier config ne change pas) ...
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # Variables pour le contenu dynamique
    dynamic_subject = None
    dynamic_body = None

    # Étape de génération de texte (implicite)
    llm_config = config.get('llm', {})
    if llm_config.get('enabled', False):
        print("[*] Le mode LLM est activé. Génération du contenu de l'email...")
        # On privilégie la variable d'environnement pour la sécurité
        api_key = os.getenv("OPENAI_API_KEY") or llm_config.get('api_key')
        prompt = llm_config.get('prompt', "Rédige un email de phishing simple.")
        
        generated_content = llm_generator.generate_text_with_llm(api_key, prompt)
        if "|||" in generated_content:
            dynamic_subject, dynamic_body = generated_content.split('|||', 1)
            # On injecte l'URL de phishing dans le corps de l'email
            phishing_url = config.get('email', {}).get('phishing_url', '')
            dynamic_body = dynamic_body.replace("[LIEN]", f'<a href="{phishing_url}">{phishing_url}</a>')
        else:
            print("[!] Avertissement: Le LLM n'a pas retourné le format attendu. L'envoi pourrait échouer ou être mal formaté.")

    # ... (le reste du code pour les steps ne change pas, mais la partie 'send' est modifiée) ...
    server_thread = None
    for step in config.get("steps", []):
        if step == "host":
            server_thread = host.run_server_in_thread(config)
        elif step == "send":
            time.sleep(1)
            # On passe le contenu dynamique à la fonction send
            send.run(config, dynamic_subject, dynamic_body)
        elif step == "generate_qr":
            # ... (la logique QR ne change pas)
            qr_config = config.get('qrcode', {})
            if qr_config.get('enabled', False):
                # ...
                qr_generator.create_qr_code(url, filename)
    
    # ... (la fin de la fonction ne change pas) ...
