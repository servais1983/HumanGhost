#!/usr/bin/env python3
"""
Script de test automatisé pour HumanGhost C2
Vérifie que tous les composants fonctionnent correctement après le nettoyage.
"""

import sys
import os
import importlib.util

def test_imports():
    """Test des imports de tous les modules essentiels"""
    print("🔍 Test des imports des modules...")
    
    try:
        # Test import principal
        sys.path.append('.')
        
        # Test des modules core essentiels
        from core import host, models, send, llm_generator, qr_generator
        print("✅ Import des modules core - OK")
        
        # Test des dépendances Flask
        from flask import Flask
        from flask_socketio import SocketIO
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Import des dépendances Flask - OK")
        
        # Test des autres dépendances
        import typer
        import openai
        import qrcode
        from weasyprint import HTML
        print("✅ Import des dépendances externes - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_flask_app_creation():
    """Test de création de l'application Flask"""
    print("\n🔍 Test de création de l'application Flask...")
    
    try:
        from core.host import create_app
        
        app = create_app()
        
        # Vérification de la configuration
        assert app.config['SECRET_KEY'] is not None
        assert 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI']
        print("✅ Configuration Flask - OK")
        
        # Test des routes principales
        with app.test_client() as client:
            # Test redirection index
            response = client.get('/')
            assert response.status_code == 302  # Redirection vers dashboard
            print("✅ Route index (redirection) - OK")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur création Flask: {e}")
        return False

def test_database_models():
    """Test des modèles de base de données"""
    print("\n🔍 Test des modèles de base de données...")
    
    try:
        from core.models import db, Setting, EmailTemplate, PageTemplate, TargetGroup, Campaign, Event
        
        # Vérification que tous les modèles existent
        models = [Setting, EmailTemplate, PageTemplate, TargetGroup, Campaign, Event]
        for model in models:
            assert hasattr(model, '__tablename__') or hasattr(model, '__table__')
        
        print("✅ Modèles de base de données - OK")
        return True
        
    except Exception as e:
        print(f"❌ Erreur modèles DB: {e}")
        return False

def test_core_modules():
    """Test des modules core individuels"""
    print("\n🔍 Test des modules core...")
    
    try:
        # Test module send
        from core.send import send_email
        assert callable(send_email)
        print("✅ Module send - OK")
        
        # Test module llm_generator
        from core.llm_generator import generate_text_with_llm
        assert callable(generate_text_with_llm)
        print("✅ Module llm_generator - OK")
        
        # Test module qr_generator
        from core.qr_generator import create_qr_code
        assert callable(create_qr_code)
        print("✅ Module qr_generator - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur modules core: {e}")
        return False

def test_templates_existence():
    """Test de l'existence des templates essentiels"""
    print("\n🔍 Test de l'existence des templates...")
    
    essential_templates = [
        'templates/layout.html',
        'templates/dashboard.html',
        'templates/settings.html',
        'templates/campaign_launcher.html',
        'templates/manage_resources.html',
        'templates/crud_form.html',
        'templates/manage_list.html',
        'templates/report_template.html',
        'templates/fake_login.html'
    ]
    
    missing_templates = []
    for template in essential_templates:
        if not os.path.exists(template):
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ Templates manquants: {missing_templates}")
        return False
    else:
        print("✅ Tous les templates essentiels présents - OK")
        return True

def test_legacy_cleanup():
    """Vérifie que les fichiers legacy ont bien été supprimés"""
    print("\n🔍 Vérification du nettoyage legacy...")
    
    # Vérification que les fichiers sont vides (supprimés)
    empty_files = [
        'core/create.py',
        'core/utils.py', 
        'templates/email_template.html'
    ]
    
    cleanup_ok = True
    for file_path in empty_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            if size > 0:
                print(f"⚠️  Fichier {file_path} devrait être vide (taille: {size})")
                cleanup_ok = False
    
    # Vérification scripts
    script_file = 'scripts/phishing_exec.yaml'
    if os.path.exists(script_file) and os.path.getsize(script_file) > 0:
        print(f"⚠️  Fichier {script_file} devrait être vide")
        cleanup_ok = False
    
    if cleanup_ok:
        print("✅ Nettoyage legacy - OK")
    
    return cleanup_ok

def main():
    """Fonction principale de test"""
    print("🎭 === HumanGhost C2 - Tests Automatisés ===\n")
    
    tests = [
        ("Imports", test_imports),
        ("Application Flask", test_flask_app_creation),
        ("Modèles DB", test_database_models),
        ("Modules Core", test_core_modules),
        ("Templates", test_templates_existence),
        ("Nettoyage Legacy", test_legacy_cleanup)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 RÉSULTAT GLOBAL: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS PASSENT - La plateforme est opérationnelle !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué - Vérification nécessaire")
        return 1

if __name__ == "__main__":
    sys.exit(main())
