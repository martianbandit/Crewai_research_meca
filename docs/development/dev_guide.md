# Guide du Développeur - Assistant Mécanique Pro

## Table des Matières
1. [Architecture](#architecture)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Développement](#développement)
5. [Tests](#tests)
6. [Déploiement](#déploiement)
7. [Maintenance](#maintenance)

## Architecture

### Vue d'Ensemble
```
app/
├── agents/          # Agents AI spécialisés
├── database/        # Gestion base de données
├── memory/          # Gestion de la mémoire
├── utils/           # Outils et utilitaires
└── streamlit_app.py # Interface utilisateur
```

### Composants Principaux

#### 1. Agents AI
- **DiagnosticExpert** : Analyse des symptômes
- **TechnicalResearcher** : Recherche documentation
- **PartsSpecialist** : Gestion des pièces
- **TechnicalWriter** : Génération de rapports
- **MaintenancePlanner** : Planification

#### 2. Base de Données
- PostgreSQL via Supabase
- Schéma détaillé dans `/docs/database/`

#### 3. API
- FastAPI pour les endpoints
- OpenAPI/Swagger pour la documentation

## Installation

### Prérequis
- Python 3.9+
- PostgreSQL 13+
- Node.js 14+ (pour le frontend)

### Configuration Développement
```bash
# Cloner le repo
git clone https://github.com/votre-username/assistant-mecanique-pro.git
cd assistant-mecanique-pro

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sous Windows

# Dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Variables d'Environnement
```bash
# .env
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
SERPER_API_KEY=...
BROWSE_AI_KEY=...
```

## Développement

### Standards de Code
- PEP 8 pour Python
- ESLint pour JavaScript
- Black pour le formatage
- Type hints obligatoires

### Structure des Agents

```python
from crewai import Agent

class DiagnosticExpert(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            name="Expert Diagnostic",
            goal="Analyser les symptômes et établir un diagnostic précis",
            backstory="Expert en diagnostic avec 20 ans d'expérience"
        )
    
    async def analyze_symptoms(self, symptoms: list) -> dict:
        # Logique d'analyse
        pass
```

### Gestion de la Mémoire

```python
from app.memory import MemoManager

class MemoryHandler:
    def __init__(self):
        self.memo = MemoManager()
    
    async def store_context(self, context: dict):
        await self.memo.store(context)
```

### Outils Personnalisés

```python
from app.utils.tools import BaseTool

class NHTSATool(BaseTool):
    def search_recalls(self, vin: str) -> list:
        # Logique de recherche
        pass
```

## Tests

### Configuration
```bash
# Installation des dépendances de test
pip install pytest pytest-asyncio pytest-cov

# Lancer les tests
pytest tests/
```

### Structure des Tests
```python
# tests/test_diagnostic_expert.py
import pytest
from app.agents import DiagnosticExpert

@pytest.mark.asyncio
async def test_symptom_analysis():
    expert = DiagnosticExpert()
    result = await expert.analyze_symptoms(["bruit_moteur"])
    assert "diagnostic" in result
```

### Coverage
```bash
# Générer un rapport de couverture
pytest --cov=app tests/
```

## Déploiement

### Production
1. Construire l'image Docker
   ```bash
   docker build -t assistant-mecanique .
   ```

2. Déployer
   ```bash
   docker-compose up -d
   ```

### Monitoring
- Sentry pour le suivi des erreurs
- Prometheus pour les métriques
- Grafana pour la visualisation

## Maintenance

### Logs
- Rotation quotidienne
- Niveau INFO en prod
- Structured logging

### Sauvegardes
- Automatisées via Supabase
- Rétention de 30 jours
- Test de restauration mensuel

### Mises à Jour
1. Créer une branche
2. Développer la fonctionnalité
3. Tests et review
4. Merge vers main
5. Déploiement automatique

## Sécurité

### Bonnes Pratiques
- Validation des entrées
- Sanitization des données
- Rate limiting
- CORS configuré

### Authentification
- JWT via Supabase Auth
- Refresh tokens
- Sessions sécurisées

## Contribution

Voir [CONTRIBUTING.md](../../CONTRIBUTING.md) pour :
- Workflow Git
- Standards de code
- Process de review
- Templates d'issues/PR

## Resources

### Documentation
- [CrewAI Docs](https://docs.crewai.com)
- [Streamlit Docs](https://docs.streamlit.io)
- [Supabase Docs](https://supabase.io/docs)

### Outils
- [Black](https://black.readthedocs.io)
- [PyTest](https://docs.pytest.org)
- [Docker](https://docs.docker.com)
