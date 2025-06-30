#!/usr/bin/env python3

import typer
from typing_extensions import Annotated
from core.utils import run_script_yaml
from core import host, qr_generator, llm_generator # On importe le nouveau module
import os
import yaml

app = typer.Typer(help="HumanGhost: Social Engineering Toolkit pour Kali Linux 🎭")

# ... (les commandes 'run', 'dashboard', 'generate-qr' restent inchangées) ...

@app.command()
def generate_text(
    prompt: Annotated[str, typer.Argument(help="Le scénario pour lequel générer le texte (ex: 'email urgent de la banque pour mot de passe oublié').")],
    api_key: Annotated[str, typer.Option(help="Votre clé API OpenAI.", envvar="OPENAI_API_KEY")] = None
):
    """
    Génère un sujet et un corps d'email de phishing avec une IA (GPT).
    """
    if not api_key:
        typer.secho("[!] La clé API OpenAI est requise. Utilisez l'option --api-key ou la variable d'environnement OPENAI_API_KEY.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    generated_content = llm_generator.generate_text_with_llm(api_key, prompt)
    
    if "|||" in generated_content:
        subject, body = generated_content.split('|||', 1)
        typer.secho("\n--- SUJET ---", fg=typer.colors.GREEN)
        typer.echo(subject.strip())
        typer.secho("\n--- CORPS ---", fg=typer.colors.GREEN)
        typer.echo(body.strip())
    else:
        typer.secho("[!] Le LLM n'a pas retourné le format attendu (sujet|||corps). Voici la réponse brute :", fg=typer.colors.YELLOW)
        typer.echo(generated_content)


@app.command()
def generate_config(
    filename: Annotated[str, typer.Argument(help="Nom du fichier de configuration à générer.")] = "config_example.yaml"
):
    """
    Génère un fichier de configuration d'exemple.
    """
    example_content = """
name: "Campagne de phishing propulsée par l'IA"

# ... (les sections target, smtp, server, qrcode restent les mêmes) ...

# Nouvelle section pour la configuration du LLM
llm:
  enabled: true
  # La clé API peut être mise ici, mais il est RECOMMANDÉ d'utiliser
  # la variable d'environnement OPENAI_API_KEY pour plus de sécurité.
  api_key: ""
  prompt: "Rédige un email de phishing très court et urgent. La cible doit cliquer sur un lien pour éviter la suspension de son compte de messagerie professionnelle pour cause de stockage plein."

# La section email peut maintenant être simplifiée si le LLM est activé
email:
  # Le sujet et le template sont ignorés si llm.enabled = true
  # subject: "Action requise : Mise à jour de sécurité de votre compte"
  # template_file: "templates/email_template.html"
  phishing_url: "http://127.0.0.1:5000"

steps:
  - host
  - generate_qr
  # - generate_text # Cette étape est maintenant implicite si llm.enabled=true
  - send
"""
    # ... (le reste de la fonction ne change pas)
    with open(filename, "w") as f:
        f.write(example_content)
    typer.secho(f"[+] Fichier de configuration d'exemple généré : {filename}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
