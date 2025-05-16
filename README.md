# HumanGhost CLI

Social Engineering CLI pour Kali Linux (phishing, vishing, smishing).

## ⚙️ Installation

```bash
chmod +x install.sh
./install.sh
```

## 🛠️ Commandes

* `create` : Génère le contenu de phishing
* `host` : Lance un faux site sur localhost
* `send` : Envoie l'attaque par mail
* `run` : Exécute un scénario YAML complet

## 🚀 Exemple

```bash
python3 humanghost.py run scripts/phishing_exec.yaml
```