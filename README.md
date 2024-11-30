🔧 Assistant Mécanique Pro - CrewAI
Description
Assistant Mécanique Pro est une application innovante basée sur CrewAI, conçue pour aider les mécaniciens de camions dans leur travail quotidien. Elle combine l'intelligence artificielle, l'expertise technique et des outils de recherche avancés pour optimiser la gestion des réparations et de la maintenance.

🌟 Fonctionnalités Principales
1. Gestion des Bons de Travail
Création automatisée de bons de travail détaillés
Diagnostic assisté par IA
Recommandations de réparations précises
Estimation des coûts et des délais
2. Recherche Technique
Accès aux manuels techniques
Bulletins de service
Historique des rappels (via NHTSA)
Documentation spécifique aux modèles
3. Gestion des Pièces
Recherche multi-sources de pièces
Comparaison des prix
Localisation des fournisseurs
Vérification de disponibilité
4. Planification
Calendrier de maintenance
Optimisation des interventions
Suivi des véhicules
Historique des réparations
🛠️ Technologies Utilisées
Framework Principal: CrewAI, Streamlit
IA et LLM: Langchain, OpenAI
Base de Données: Supabase
Outils de Recherche: Serper, Browse.ai
Géolocalisation: Geopy
Mémoire et Cache: Memo, Redis
📋 Prérequis
Python 3.9+
Compte Supabase
Clés API (OpenAI, Serper, etc.)
Chrome WebDriver (pour le scraping)
🚀 Installation
Cloner le repository
bash
CopyInsert
git clone https://github.com/votre-username/assistant-mecanique-pro.git
cd assistant-mecanique-pro
Installer les dépendances
bash
CopyInsert in Terminal
pip install -r requirements.txt
Configurer les variables d'environnement
bash
CopyInsert
cp .env.example .env
# Éditer .env avec vos clés API
Initialiser la base de données Supabase
sql
CopyInsert
-- Exécuter les scripts SQL fournis dans /docs/database
🎯 Utilisation
Lancer l'application
bash
CopyInsert in Terminal
streamlit run app/streamlit_app.py
Se connecter avec les identifiants fournis
Accéder aux différentes fonctionnalités via le menu principal
🤖 Agents AI
L'application utilise plusieurs agents spécialisés :

Expert en Diagnostic: Analyse les symptômes et établit des diagnostics
Chercheur Technique: Recherche la documentation pertinente
Spécialiste Pièces: Identifie et localise les pièces nécessaires
Rédacteur Technique: Génère les bons de travail
Planificateur: Optimise les interventions
📊 Structure de la Base de Données
vehicles: Informations sur les véhicules
mechanics: Données des mécaniciens
parts: Catalogue de pièces
work_orders: Bons de travail
maintenance_history: Historique des interventions
🔒 Sécurité
Authentification sécurisée
Gestion des rôles et permissions
Protection des données sensibles
Chiffrement des communications
🤝 Contribution
Les contributions sont les bienvenues ! Voir CONTRIBUTING.md pour les directives.

📝 License
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

📞 Support
Documentation: /docs
Issues: GitHub Issues
Contact: support@assistant-mecanique.com
🔄 Mises à jour
Version 1.0.0 : Version initiale
Version 1.1.0 : Ajout de la géolocalisation
Version 1.2.0 : Intégration NHTSA
⭐ Remerciements
Équipe CrewAI
Communauté open-source
Contributeurs
Développé avec ❤️ pour la communauté des mécaniciens

