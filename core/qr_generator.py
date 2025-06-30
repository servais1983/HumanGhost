import qrcode
import os

def create_qr_code(url, filename="phishing_qr.png"):
    """
    Génère une image de QR code à partir d'une URL.

    Args:
        url (str): L'URL à encoder dans le QR code.
        filename (str): Le nom du fichier image à sauvegarder.
    """
    try:
        print(f"[*] Génération du QR code pour l'URL : {url}")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # S'assurer que le dossier de sortie existe
        output_dir = "campaign_files"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print(f"[+] QR code sauvegardé avec succès dans : {filepath}")
    except Exception as e:
        print(f"[!] Erreur lors de la génération du QR code : {e}")
