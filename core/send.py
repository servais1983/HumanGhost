import smtplib
from email.message import EmailMessage
from jinja2 import Template

# Le run() accepte maintenant du contenu dynamique
def run(config, dynamic_subject=None, dynamic_body=None):
    """
    Génère et envoie l'email de phishing.
    Peut utiliser soit un template de fichier, soit du contenu dynamique.
    """
    print("[*] Préparation de l'email de phishing...")
    
    email_subject = dynamic_subject or config['email']['subject']
    
    if dynamic_body:
        email_body_html = dynamic_body.replace('\n', '<br>')
    else:
        # Utilisation de Jinja2 si pas de contenu dynamique
        with open(config['email']['template_file'], 'r') as f:
            template = Template(f.read())
        template_vars = {
            "phishing_url": config['email']['phishing_url'],
            "target_name": config['target']['name']
        }
        email_body_html = template.render(template_vars)

    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = config['smtp']['sender_email']
    msg['To'] = config['target']['email']
    msg.set_content("Veuillez activer le HTML pour voir ce message.")
    msg.add_alternative(email_body_html, subtype='html')
    
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
