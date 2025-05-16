#!/bin/bash
echo "[*] Installation de HumanGhost (social engineering) sur Kali..."

sudo apt update
sudo apt install -y python3 python3-pip sendmail
pip3 install -r requirements.txt

echo "[+] Installation terminée. Lancez : python3 humanghost.py run scripts/phishing_exec.yaml"