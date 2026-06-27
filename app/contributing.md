# Guide de contribution

Merci de votre intérêt pour contribuer au projet Ubisoft People Analytics !

## 🚀 Comment contribuer

### 1. Fork et Clone
git fork https://github.com/remichenouri/ubisoft_people_analytics
git clone https://github.com/YOUR_USERNAME/ubisoft_people_analytics
cd ubisoft_people_analytics

### 2. Setup environnement de développement
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
pre-commit install

### 3. Créer une branche
git checkout -b feature/your-feature-name
ou
git checkout -b fix/your-bug-fix

## 📋 Standards de développement

### Code Style
- **Black** pour le formatting Python
- **isort** pour les imports
- **flake8** pour le linting
- **Type hints** obligatoires pour nouvelles fonctions

### Tests
Lancer tous les tests
pytest

Tests avec coverage
pytest --cov=src

Tests spécifiques
pytest tests/test_models.py -v

### Commits
Format : `type(scope): description`

Types acceptés :
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug  
- `docs`: documentation
- `style`: formatting, pas de changement de code
- `refactor`: refactoring code
- `test`: ajout/modification tests
- `chore`: tâches maintenance

Exemple : `feat(ml): add XGBoost model for turnover prediction`

### Documentation
- Docstrings format Google Style
- README à jour si changement d'interface
- Documentation technique si nouvelle architecture

## 🔍 Process de review

1. **Pre-commit hooks** passent ✅
2. **Tests CI/CD** passent ✅  
3. **Review par maintainer** avant merge
4. **Squash merge** dans main

## 🐛 Signaler un bug

Utilisez le template GitHub Issue avec :
- Description claire du problème
- Steps de reproduction
- Environnement (OS, Python version, etc.)
- Screenshots si applicable

## 💡 Proposer une fonctionnalité

1. Créer GitHub Issue avec label `enhancement`
2. Discussion avec maintainers
3. Validation concept avant développement

## 📞 Questions

- 💬 GitHub Discussions pour questions générales
- 📧 chenouri.remi@proton.me pour questions spécifiques
- 🐛 GitHub Issues pour bugs/features

Merci de contribuer à améliorer l'accompagnement de la neurodiversité en tech ! 🧠✨
