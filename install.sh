#!/bin/bash
echo "[*] Installation de HumanGhost (social engineering) sur Kali..."

# Mise à jour des paquets et installation des prérequis système
sudo apt update
sudo apt install -y python3-pip python3-venv sendmail

# Création d'un environnement virtuel
echo "[*] Création de l'environnement virtuel dans le dossier 'venv'..."
python3 -m venv venv

# Activation de l'environnement et installation des dépendances Python
echo "[*] Installation des dépendances Python via pip..."
source venv/bin/activate
pip install -r requirements.txt

echo "[+] Installation terminée."
echo "Pour activer l'environnement, lancez : source venv/bin/activate"
echo "Ensuite, lancez l'outil avec : python3 humanghost.py run scripts/phishing_exec.yaml"
