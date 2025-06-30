#!/usr/bin/env python3

import typer
from typing_extensions import Annotated
from core.utils import run_script_yaml
from core import host, qr_generator # On importe le nouveau module
import os
import yaml

app = typer.Typer(help="HumanGhost: Social Engineering Toolkit pour Kali Linux 🎭")

# ... (les commandes 'run' et 'dashboard' restent inchangées) ...
@app.command()
def run(
    script: Annotated[str, typer.Argument(help="Chemin vers le fichier de scénario YAML.")]
):
    """
    Exécute une campagne complète (email + serveur) à partir d'un scénario.
    """
    if not os.path.exists(script):
        typer.secho(f"[!] Fichier de scénario introuvable : {script}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    run_script_yaml(script)

@app.command()
def dashboard(
    config_file: Annotated[str, typer.Argument(help="Chemin vers le fichier de configuration YAML.")] = "config_example.yaml"
):
    """
    Lance uniquement le serveur de phishing avec son tableau de bord.
    """
    if not os.path.exists(config_file):
        typer.secho(f"[!] Fichier de configuration introuvable : {config_file}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    print(f"[*] Chargement de la configuration : {config_file}")
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        
    server_thread = host.run_server_in_thread(config)
    print("[+] Serveur et tableau de bord actifs. Appuyez sur CTRL+C pour arrêter.")
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\n[*] Arrêt du serveur.")

@app.command()
def generate_qr(
    url: Annotated[str, typer.Option(help="L'URL à encoder dans le QR code.")] = "http://127.0.0.1:5000",
    output: Annotated[str, typer.Option(help="Nom du fichier de sortie.")] = "phishing_qr.png"
):
    """
    Génère un QR code malveillant pointant vers une URL.
    """
    qr_generator.create_qr_code(url, output)

# ... (la commande 'generate_config' est mise à jour ci-dessous) ...
@app.command()
def generate_config(
    filename: Annotated[str, typer.Argument(help="Nom du fichier de configuration à générer.")] = "config_example.yaml"
):
    """
    Génère un fichier de configuration d'exemple.
    """
    example_content = """
name: "Campagne de phishing avancée avec QR Code"
target:
  name: "John Doe"
  email: "victime@example.com"

smtp:
  host: "smtp.mondomaine.com"
  port: 587
  username: "votre_email@mondomaine.com"
  password: "votre_mot_de_passe"
  sender_email: "security-update@mondomaine.com"
  use_tls: true

email:
  subject: "Action requise : Mise à jour de sécurité de votre compte"
  template_file: "templates/email_template.html"
  phishing_url: "http://127.0.0.1:5000"

server:
  host: "0.0.0.0"
  port: 5000
  template: "fake_login.html"
  redirect_url: "https://www.google.com"

# Nouvelle section pour la configuration du QR Code
qrcode:
  enabled: true
  output_filename: "campaign_qr_code.png"

steps:
  - host      # Lance le serveur en arrière-plan
  - generate_qr # Génère le QR Code
  - send      # Envoie l'email
"""
    with open(filename, "w") as f:
        f.write(example_content)
    typer.secho(f"[+] Fichier de configuration d'exemple généré : {filename}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
