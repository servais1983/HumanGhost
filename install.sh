#!/bin/bash
echo "[*] Installation de HumanGhost (social engineering) sur Kali..."

# Mise à jour des paquets et installation des prérequis système
# Ajout des dépendances pour WeasyPrint (génération de PDF)
sudo apt update
sudo apt install -y python3-pip python3-venv sendmail build-essential python3-dev python3-cffi libcairo2-dev pango1.0-tools libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# ... (le reste du script ne change pas) ...
echo "[*] Création de l'environnement virtuel dans le dossier 'venv'..."
python3 -m venv venv

echo "[*] Installation des dépendances Python via pip..."
source venv/bin/activate
pip install -r requirements.txt

echo "[+] Installation terminée."
# ...
