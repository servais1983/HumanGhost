import os
from openai import OpenAI

def generate_text_with_llm(api_key, prompt):
    """
    Génère du texte en utilisant l'API d'OpenAI (GPT).

    Args:
        api_key (str): Votre clé API OpenAI.
        prompt (str): Le prompt décrivant le texte à générer.

    Returns:
        str: Le texte généré par le modèle.
    """
    if not api_key:
        return "[ERREUR] Clé API OpenAI non fournie. Veuillez la définir dans votre config ou en tant que variable d'environnement OPENAI_API_KEY."

    print(f"[*] Envoi du prompt au LLM...")
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Un modèle rapide et efficace
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en cybersécurité. Génère un texte court et crédible pour un email de phishing basé sur la demande de l'utilisateur. Le texte doit être direct et inciter à l'action. Sépare le sujet et le corps de l'email par '|||'."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_text = response.choices[0].message.content.strip()
        print("[+] Réponse du LLM reçue.")
        return generated_text
    except Exception as e:
        return f"[ERREUR] Échec de la communication avec l'API OpenAI : {e}"
