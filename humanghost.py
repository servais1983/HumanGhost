#!/usr/bin/env python3

import typer
from typing_extensions import Annotated
from core.utils import run_script_yaml
import os

app = typer.Typer(help="HumanGhost: Social Engineering Toolkit pour Kali Linux 🎭")

@app.command()
def run(
    script: Annotated[str, typer.Argument(help="Chemin vers le fichier de scénario YAML.")]
):
    """
    Exécute une campagne complète à partir d'un scénario YAML.
    """
    if not os.path.exists(script):
        typer.secho(f"[!] Fichier de scénario introuvable : {script}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    run_script_yaml(script)

@app.command()
def generate_config(
    filename: Annotated[str, typer.Argument(help="Nom du fichier de configuration à générer.")] = "config_example.yaml"
):
    """
    Génère un fichier de configuration d'exemple.
    """
    # Ce contenu est un exemple complet de ce que l'utilisateur peut configurer.
    # Dans la version précédente, ces infos étaient en dur.
    example_content = """
name: "Campagne de phishing contre Service Financier"
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
  template_file: "templates/email_template.html" # Nouveau template d'email
  phishing_url: "http://127.0.0.1:5000" # URL de votre serveur Flask

server:
  host: "0.0.0.0"
  port: 5000
  template: "fake_login.html" # Template de la page de phishing
  redirect_url: "https://www.google.com" # Où rediriger après le vol d'infos

steps:
  - send
  - host
"""
    with open(filename, "w") as f:
        f.write(example_content)
    typer.secho(f"[+] Fichier de configuration d'exemple généré : {filename}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
