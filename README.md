![image](humanghost.png)

# 🎭 HumanGhost C2 - Plateforme de Social Engineering

<p align="center">
  <img src="https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kali-linux&logoColor=white" alt="Kali Linux"/>
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Framework-Flask-black.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License: MIT"/>
</p>

<p align="center">
  <b>Plateforme web complète pour orchestrer vos campagnes de Social Engineering</b><br>
  <sub>📊 Tableau de bord | 🚀 Lancement de campagnes | 🗂️ Gestion de ressources | 📝 Rapports PDF</sub>
</p>

---

## 📋 Description

**HumanGhost** est une plateforme de commandement et de contrôle (C2) conçue pour planifier, lancer et suivre des campagnes de social engineering dans un cadre légal et éthique (Red Team, tests d'intrusion autorisés). L'outil est désormais doté d'une interface web complète pour une gestion centralisée et intuitive.

> ⚠️ **Avertissement** : Cet outil est destiné exclusivement à des fins légitimes telles que les tests de pénétration, la formation à la sensibilisation à la sécurité et l'évaluation des vulnérabilités. Toute utilisation non autorisée est illégale et contraire à l'éthique.

## ✨ Fonctionnalités

### Interface Web (C2)
Une plateforme complète pour gérer toutes les facettes de vos campagnes.

### 📊 Tableau de Bord
Suivez en temps réel les événements de vos campagnes (visites, identifiants collectés) grâce à l'intégration SocketIO.

### 🗂️ Gestion des Ressources (CRUD)
Créez, modifiez et gérez de manière centralisée :
- Vos templates d'e-mails de phishing (HTML)
- Vos templates de pages de phishing (HTML)
- Vos groupes de cibles

### 🚀 Lancement de Campagnes Simplifié
Lancez une campagne complète en quelques clics depuis l'interface web.

### 📝 Génération de Rapports PDF
Générez automatiquement un rapport de campagne détaillé au format PDF, incluant les statistiques et le journal des événements.

### 🤖 Intégration LLM (OpenAI)
Générez dynamiquement des sujets et des corps d'e-mails de phishing crédibles en utilisant l'API d'OpenAI.

### 📱 Génération de QR Codes
Créez des QR codes malveillants pour vos scénarios de "quishing".

### ⚙️ Configuration Sécurisée
Gérez vos clés API (OpenAI) et vos configurations de serveur SMTP directement depuis l'interface.

## ⚙️ Installation

Le script d'installation a été mis à jour pour inclure les nouvelles dépendances nécessaires au fonctionnement du serveur web et à la génération de PDF.

```bash
# Cloner le dépôt
git clone https://github.com/servais1983/HumanGhost.git
cd HumanGhost

# Rendre le script d'installation exécutable
chmod +x install.sh

# Lancer l'installation (installe les dépendances système et Python)
./install.sh
```

## 🚀 Démarrage

L'outil se lance désormais comme un serveur web.

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer le serveur HumanGhost (par défaut sur http://0.0.0.0:5000)
python3 humanghost.py start
```

Ouvrez ensuite votre navigateur et rendez-vous sur **http://127.0.0.1:5000** pour accéder au tableau de bord.

## 🗂️ Structure du Projet

La structure a été adaptée pour supporter l'application web Flask.

```
humanghost/
├── core/                   # Modules principaux de l'application
│   ├── host.py             # Logique du serveur Flask (C2)
│   ├── models.py           # Modèles de base de données (SQLAlchemy)
│   ├── llm_generator.py    # Générateur de contenu via OpenAI
│   ├── qr_generator.py     # Générateur de QR Code
│   ├── send.py             # Logique d'envoi d'emails
│   └── utils.py            # Utilitaires
├── templates/              # Templates HTML pour l'interface web et les emails
│   ├── dashboard.html      # Tableau de bord principal
│   ├── campaign_launcher.html # Page pour lancer les campagnes
│   ├── manage_resources.html # Hub de gestion des ressources
│   ├── report_template.html  # Modèle pour les rapports PDF
│   ├── settings.html       # Configuration globale
│   └── layout.html         # Template de base
├── scripts/                # Scénarios prédéfinis (legacy CLI)
│   └── phishing_exec.yaml
├── humanghost.py           # Point d'entrée principal (CLI pour démarrer le serveur)
├── humanghost.db           # Base de données SQLite
├── requirements.txt        # Dépendances Python
├── install.sh              # Script d'installation
└── README.md               # Cette documentation
```

## 🛠️ Utilisation de l'Interface Web

### 1. Configuration Initiale
Accédez à la section **Paramètres** pour configurer :
- Serveur SMTP (hôte, port, authentification)
- Clé API OpenAI pour la génération automatique de contenu

### 2. Création des Ressources
Dans la section **Gérer les Ressources**, créez :
- **Templates d'E-mail** : Sujets et corps HTML des emails de phishing
- **Templates de Page** : Pages de capture d'identifiants
- **Groupes de Cibles** : Listes d'adresses email à cibler

### 3. Lancement de Campagne
Utilisez le **Lanceur de Campagne** pour :
- Sélectionner un template d'email, une page de phishing et un groupe de cibles
- Lancer la campagne automatiquement
- Suivre les résultats en temps réel

### 4. Suivi et Analyse
Le **Tableau de Bord** permet de :
- Visualiser les événements en temps réel
- Télécharger des rapports PDF détaillés
- Analyser l'efficacité des campagnes

## 📈 Fonctionnalités Avancées

### Génération de Contenu par IA
Intégration avec l'API OpenAI pour générer automatiquement des emails de phishing crédibles et contextualisés.

### QR Codes Malveillants
Création de QR codes pointant vers vos pages de phishing pour des attaques de "quishing".

### Rapports Professionnels
Génération automatique de rapports PDF complets avec statistiques et journaux d'événements pour vos clients ou votre équipe.

### Interface Temps Réel
Suivi live des campagnes grâce à l'intégration WebSocket (SocketIO).

## 🔒 Sécurité et Éthique

Ce projet est conçu pour des **tests de sécurité légitimes** et pour **sensibiliser à la sécurité**. Utilisez-le uniquement avec une autorisation explicite dans le cadre de :

- ✅ Tests de pénétration autorisés
- ✅ Formations de sensibilisation à la sécurité
- ✅ Évaluations de sécurité internes
- ✅ Démonstrations éducatives dans un cadre Red Team

**IMPORTANT** : Les développeurs de cet outil déclinent toute responsabilité en cas d'utilisation malveillante ou illégale. Respectez les lois locales et internationales.

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request pour améliorer l'outil.

### Roadmap
- [ ] Support multi-utilisateurs avec authentification
- [ ] Intégration avec d'autres services de messagerie
- [ ] Templates additionnels (réseaux sociaux, services cloud)
- [ ] API REST pour l'automatisation
- [ ] Dashboard analytics avancé

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

<p align="center">
  <sub>🔐 Développé pour promouvoir la sensibilisation à la sécurité et les tests d'intrusion éthiques 🛡️</sub>
</p>