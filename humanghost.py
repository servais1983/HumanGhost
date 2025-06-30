#!/usr/bin/env python3

import typer
from core.host import run_server

app = typer.Typer(help="HumanGhost: Lance le serveur de la plateforme de C2.")

@app.command()
def start(
    host: str = "0.0.0.0",
    port: int = 5000
):
    """
    Démarre le serveur web HumanGhost.
    """
    typer.echo(f"[*] Démarrage du serveur HumanGhost sur http://{host}:{port}")
    run_server(host, port)

if __name__ == "__main__":
    app()
