# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à Assistant Mécanique Pro ! Ce guide vous aidera à comprendre comment participer efficacement au projet.

## 🌟 Types de Contributions

Nous accueillons différents types de contributions :
- 🐛 Correction de bugs
- ✨ Nouvelles fonctionnalités
- 📚 Documentation
- 🔍 Tests
- 🌐 Traductions
- 💡 Suggestions d'amélioration

## 🚀 Comment Contribuer

### 1. Préparation
1. Fork le projet
2. Clonez votre fork :
   ```bash
   git clone https://github.com/votre-username/assistant-mecanique-pro.git
   ```
3. Créez une nouvelle branche :
   ```bash
   git checkout -b feature/ma-contribution
   ```

### 2. Développement
1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Configurez votre environnement :
   ```bash
   cp .env.example .env
   # Ajoutez vos clés API de test
   ```

### 3. Standards de Code
- Suivez PEP 8 pour Python
- Commentez votre code en français
- Utilisez des noms de variables et fonctions explicites
- Ajoutez des docstrings pour les nouvelles fonctions
- Maintenez une couverture de tests > 80%

### 4. Tests
```bash
pytest tests/
```

### 5. Soumission
1. Committez vos changements :
   ```bash
   git commit -m "feat: ajout de [fonctionnalité]"
   ```
2. Poussez vers votre fork :
   ```bash
   git push origin feature/ma-contribution
   ```
3. Créez une Pull Request

## 📝 Convention de Commit

Utilisez les préfixes suivants :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `test:` Ajout/modification de tests
- `refactor:` Refactoring
- `style:` Formatage
- `perf:` Optimisation

## 🔍 Processus de Review

1. Vérification automatique :
   - Tests
   - Linting
   - Couverture de code

2. Review humaine :
   - Clarté du code
   - Performance
   - Sécurité
   - Documentation

## 🎯 Priorités Actuelles

1. Amélioration des agents AI :
   - Optimisation des prompts
   - Nouveaux outils spécialisés
   - Meilleure gestion du contexte

2. Interface utilisateur :
   - UX plus intuitive
   - Nouveaux composants Streamlit
   - Mode sombre

3. Documentation :
   - Guides utilisateur
   - Documentation API
   - Exemples d'utilisation

## ⚠️ À Éviter

- Code non testé
- Commits directs sur main
- Modifications de l'API sans documentation
- Dépendances lourdes sans justification

## 🆘 Besoin d'Aide ?

- 💬 Ouvrez une issue pour discuter
- 📧 Contactez l'équipe : support@assistant-mecanique.com
- 💡 Consultez les discussions GitHub

## 🙏 Code de Conduite

- Soyez respectueux
- Acceptez les critiques constructives
- Aidez les autres contributeurs
- Maintenez un environnement positif

---

💪 Ensemble, rendons l'Assistant Mécanique Pro encore meilleur !
