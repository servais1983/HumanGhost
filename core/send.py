import smtplib
from email.message import EmailMessage
from jinja2 import Template

def run(config):
    """
    Génère et envoie l'email de phishing.
    """
    print("[*] Préparation de l'email de phishing...")

    # Utilisation de Jinja2 pour le template d'email
    with open(config['email']['template_file'], 'r') as f:
        template = Template(f.read())

    # Variables pour le template
    template_vars = {
        "phishing_url": config['email']['phishing_url'],
        "target_name": config['target']['name']
    }
    
    email_body = template.render(template_vars)

    msg = EmailMessage()
    msg['Subject'] = config['email']['subject']
    msg['From'] = config['smtp']['sender_email']
    msg['To'] = config['target']['email']
    msg.set_content("Veuillez activer le HTML pour voir ce message.")
    msg.add_alternative(email_body, subtype='html')
    
    try:
        print(f"[*] Connexion au serveur SMTP : {config['smtp']['host']}:{config['smtp']['port']}...")
        with smtplib.SMTP(config['smtp']['host'], config['smtp']['port']) as s:
            if config['smtp'].get('use_tls', True):
                s.starttls()
            s.login(config['smtp']['username'], config['smtp']['password'])
            s.send_message(msg)
            print(f"[+] Email de phishing envoyé à {config['target']['email']}")
    except Exception as e:
        print(f"[!] Erreur lors de l'envoi de l'email : {e}")
