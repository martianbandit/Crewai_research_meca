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
