import smtplib
from email.message import EmailMessage

def send_email(smtp_config, target_email, subject, body):
    """
    Envoie un email en utilisant la configuration fournie.
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = smtp_config['sender_email']
    msg['To'] = target_email
    msg.set_content("Veuillez activer le HTML pour voir ce message.")
    msg.add_alternative(body, subtype='html')

    try:
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as s:
            s.starttls()
            s.login(smtp_config['username'], smtp_config['password'])
            s.send_message(msg)
        print(f"[+] Email envoyé avec succès à {target_email}")
        return True
    except Exception as e:
        print(f"[!] Échec de l'envoi de l'email à {target_email}: {e}")
        return False
