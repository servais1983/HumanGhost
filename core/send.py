import smtplib
from email.message import EmailMessage

def run():
    print("[*] Envoi d'un email de phishing (démo)")
    msg = EmailMessage()
    msg['Subject'] = 'Mise à jour de votre compte'
    msg['From'] = 'admin@fakebank.com'
    msg['To'] = 'victime@example.com'
    msg.set_content('Cliquez ici : http://localhost:5000/login')

    try:
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)
            print("[+] Email envoyé (via SMTP local)")
    except Exception as e:
        print(f"[!] Erreur d'envoi : {e}")