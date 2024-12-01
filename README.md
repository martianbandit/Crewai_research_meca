# 🔧 Assistant Mécanique Pro - CrewAI

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/votre-username/assistant-mecanique-pro)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Application d'assistance IA pour mécaniciens de camions, propulsée par CrewAI et Streamlit.

## 📑 Table des Matières
- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Agents AI](#agents-ai)
- [Base de Données](#base-de-données)
- [Sécurité](#sécurité)
- [Contribution](#contribution)
- [Support](#support)
- [Mises à jour](#mises-à-jour)

## 📖 Description

Assistant Mécanique Pro est une application innovante basée sur CrewAI, conçue pour aider les mécaniciens de camions dans leur travail quotidien. Elle combine l'intelligence artificielle, l'expertise technique et des outils de recherche avancés pour optimiser la gestion des réparations et de la maintenance.

### 🌟 Fonctionnalités Principales
 * _ Gestion des Bons de Travail
- Création automatisée de bons de travail détaillés
- Diagnostic assisté par IA
- Recommandations de réparations précises
- Estimation des coûts et des délais
 * _ Recherche Technique
- Accès aux manuels techniques
- Bulletins de service
- Historique des rappels (via NHTSA)
- Documentation spécifique aux modèles
 * Gestion des Pièces *
- Recherche multi-sources de pièces
- Comparaison des prix
- Localisation des fournisseurs
- Vérification de disponibilité
 - * Planification
- Calendrier de maintenance
- Optimisation des interventions
- Suivi des véhicules
- Historique des réparations
🛠️ ##Technologies Utilisées
### Framework Principal: - CrewAI, - Streamlit
### IA et LLM: - Langchain, - OpenAI
### Base de Données: - Supabase
### Outils de Recherche: - Serper, - Browse.ai
### Géolocalisation: - Geopy
### Mémoire et Cache: - Memo, - Redis
📋 ##Prérequis
_ Python 3.9+
_ Compte Supabase
_ Clés API (OpenAI, Serper, etc.)
_Chrome WebDriver (pour le scraping)
🚀 ##Installation
Cloner le repository:
'''git clone https://github.com/votre-username/assistant-mecanique-pro.git
cd assistant-mecanique-pro'''

Installer les dépendances:
'''pip install -r requirements.txt'''

Configurer les variables d'environnement:
![Interface principale](docs/images/interface.png)

## ✨ Fonctionnalités

### 1. Gestion des Bons de Travail
- 📝 Création automatisée de bons de travail détaillés
- 🔍 Diagnostic assisté par IA
- 💡 Recommandations de réparations précises
- 💰 Estimation des coûts et des délais

### 2. Recherche Technique
- 📚 Accès aux manuels techniques
- 📋 Bulletins de service
- 🚨 Historique des rappels (via NHTSA)
- 📖 Documentation spécifique aux modèles

### 3. Gestion des Pièces
- 🔎 Recherche multi-sources de pièces
- 💵 Comparaison des prix
- 🗺️ Localisation des fournisseurs
- ✅ Vérification de disponibilité

### 4. Planification
- 📅 Calendrier de maintenance
- ⚡ Optimisation des interventions
- 🚛 Suivi des véhicules
- 📊 Historique des réparations

## 🛠️ Technologies

| Catégorie | Technologies |
|-----------|-------------|
| Framework | CrewAI, Streamlit |
| IA et LLM | Langchain, OpenAI |
| Base de Données | Supabase |
| Recherche | Serper, Browse.ai |
| Géolocalisation | Geopy |
| Cache | Memo, Redis |

## 📋 Prérequis

- Python 3.9+
- Compte Supabase
- Clés API (OpenAI, Serper, etc.)
- Chrome WebDriver (pour le scraping)

## 🚀 Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/votre-username/assistant-mecanique-pro.git
   cd assistant-mecanique-pro
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos clés API
   ```

4. **Initialiser la base de données**
   ```sql
   -- Exécuter les scripts SQL fournis dans /docs/database
   ```

## 🎯 Utilisation

### Démarrage Rapide

1. **Lancer l'application**
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **Se connecter** avec les identifiants fournis
3. **Accéder** aux différentes fonctionnalités via le menu principal

### Exemple d'Utilisation

```python
# Exemple de création d'un bon de travail
from app.agents import MechanicCrew

crew = MechanicCrew(context={
    "vehicle": {"make": "Volvo", "model": "VNL", "year": 2020},
    "symptoms": "Bruit anormal au niveau des freins"
})

work_order = crew.process_work_order()
```

## 🤖 Agents AI

Notre système utilise des agents AI spécialisés :

| Agent | Rôle | Outils |
|-------|------|--------|
| Expert Diagnostic | Analyse des symptômes | NHTSA, DiagnosticTool |
| Chercheur Technique | Documentation | TechnicalDocs, ServiceBulletins |
| Spécialiste Pièces | Recherche de pièces | PartsSearch, GeoLocation |
| Rédacteur Technique | Rédaction des bons | TemplateEngine |
| Planificateur | Optimisation maintenance | MaintenanceScheduler |

## 📊 Base de Données

Structure des tables principales :

```sql
-- Exemple de schéma
CREATE TABLE vehicles (
    id UUID PRIMARY KEY,
    make VARCHAR,
    model VARCHAR,
    year INTEGER,
    vin VARCHAR UNIQUE
);
```

## 🔒 Sécurité

- 🔐 Authentification sécurisée
- 👥 Gestion des rôles et permissions
- 🔑 Protection des données sensibles
- 🔒 Chiffrement des communications

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives.

## 📞 Support

- 📚 [Documentation complète](/docs)
- 🐛 [Signaler un bug](https://github.com/votre-username/assistant-mecanique-pro/issues)
- 📧 Contact : support@assistant-mecanique.com

## 🔄 Mises à jour

| Version | Description |
|---------|-------------|
| 1.0.0 | Version initiale |
| 1.1.0 | Ajout géolocalisation |
| 1.2.0 | Intégration NHTSA |

## ⭐ Remerciements

- Équipe CrewAI
- Communauté open-source
- Tous nos contributeurs

---
Développé avec ❤️ pour la communauté des mécaniciens

# Assistant Mécanique Pro 🔧

## Description
Assistant Mécanique Pro est un outil d'IA avancé conçu pour aider les mécaniciens de camions dans leur travail quotidien. Il combine l'expertise de plusieurs agents spécialisés pour fournir une assistance complète dans le diagnostic, la maintenance et la réparation des véhicules lourds.

## Fonctionnalités Principales 🚀

- **Analyse d'Images** 📸
  - Détection automatique des dommages
  - Évaluation de la sévérité
  - Génération de rapports détaillés

- **Conformité Réglementaire** 📋
  - Vérification FMCSA et DOT
  - Suivi des rappels
  - Audit de conformité

- **Diagnostic Électronique** 💻
  - Interprétation des codes DTC
  - Analyse CAN Bus
  - Recommandations de réparation

- **Télémétrie IoT** 📡
  - Surveillance en temps réel
  - Analyse prédictive
  - Maintenance préventive

- **Assistance Technique** 📚
  - Recherche de tutoriels
  - Analyse de contenu vidéo
  - Documentation technique

## Installation 🛠️

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/assistant-mecanique-pro.git
cd assistant-mecanique-pro
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos clés API
Initialiser la base de données Supabase
-- Exécuter les scripts SQL fournis dans /docs/database
🎯 ##Utilisation
Lancer l'application:
'''streamlit run app/streamlit_app.py'''
Se connecter avec les identifiants fournis
Accéder aux différentes fonctionnalités via le menu principal
🤖 ##Agents AI
L'application utilise plusieurs agents spécialisés :

_Expert _en _Diagnostic: Analyse les symptômes et établit des diagnostics
_Chercheur _Technique: Recherche la documentation pertinente
_Spécialiste _Pièces: Identifie et localise les pièces nécessaires
_Rédacteur _Technique: Génère les bons de travail
_Planificateur: Optimise les interventions
📊 Structure de la Base de Données
_vehicles: Informations sur les véhicules
_mechanics: Données des mécaniciens
_parts: Catalogue de pièces
_work_orders: Bons de travail
_maintenance_history: Historique des interventions
🔒 Sécurité
Authentification sécurisée
Gestion des rôles et permissions
Protection des données sensibles
Chiffrement des communications
🤝 Contribution
Les contributions sont les bienvenues ! Voir CONTRIBUTING.md pour les directives.

📝 License
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
```

## Configuration ⚙️

1. Configurer les agents dans `config/agents.yaml`
2. Ajuster les paramètres dans `config/settings.yaml`
3. Personnaliser les outils dans `app/tools/`

## Utilisation 🚀

1. Lancer l'application Streamlit :
```bash
streamlit run streamlit_app.py
```

2. Utiliser l'API :
```python
from app.crews.mechanic_crew import MechanicCrew

# Initialiser l'équipe
crew = MechanicCrew()

# Inspecter un véhicule
result = crew.inspect_vehicle(
    vehicle_id="TRUCK_001",
    images=["image1.jpg", "image2.jpg"],
    dtc_codes=["P0123", "P0456"]
)
```

## Structure du Projet 📁

```
assistant-mecanique-pro/
├── app/
│   ├── agents/          # Agents spécialisés
│   ├── crews/           # Équipes d'agents
│   ├── tools/           # Outils spécialisés
│   └── utils/           # Utilitaires
├── config/              # Fichiers de configuration
├── docs/                # Documentation
├── tests/               # Tests unitaires et d'intégration
└── streamlit_app.py     # Interface utilisateur
```

## Variables d'Environnement 🔐

- `OPENAI_API_KEY`: Clé API OpenAI
- `SUPABASE_URL`: URL Supabase
- `SUPABASE_KEY`: Clé API Supabase
- `SERPER_API_KEY`: Clé API Serper
- `IMAGE_STORAGE_BUCKET`: Bucket de stockage d'images

## Tests 🧪

Exécuter les tests :
```bash
pytest tests/
```

## Documentation 📚

La documentation complète est disponible dans le dossier `docs/` et peut être générée avec MkDocs :
```bash
mkdocs serve
```

## Contribution 🤝

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence 📄

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact 📧

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)

Lien du projet : [https://github.com/votre-username/assistant-mecanique-pro](https://github.com/votre-username/assistant-mecanique-pro)
