# Contribuer à **Ubisoft People Analytics**

Merci de votre intérêt ! Toute contribution, petite ou grande, est la bienvenue.  
Le guide ci-dessous explique comment installer le projet, ouvrir une _issue_ ou une _pull request_ et respecter notre style de code.

---

## ⚙️ Pré-requis

| Outil | Version minimale | Vérifier |
|-------|------------------|----------|
| Python | 3.9 | `python --version` |
| Git    | 2.30 | `git --version` |
| Docker | 20.10 (facultatif) | `docker --version` |

---

## 🚀 Mise en place locale

git clone https://github.com/remichenouri/ubisoft_people_analytics.git
cd ubisoft_people_analytics
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py

Les tests doivent passer :

ruff check
pytest

---

## 🌳 Workflow Git Flow simplifié

1. `main` : toujours déployable.  
2. `dev` : branche d’intégration (merge automatique après CI).  
3. `feature/<nom>` : votre branche de travail.  

git checkout -b feature/ma_fonction
git push origin feature/ma_fonction


Ouvrez ensuite une _pull request_ vers **dev**.

---

## 🎨 Style de code

| Outil | Commande CI |
|-------|-------------|
| Black | `black .` |
| Ruff  | `ruff --fix .` |
| Mypy  | `mypy src` |

La CI rejette toute PR non conforme.

---

## ✅ Checklist Pull Request

- [ ] Le code se lance sans erreur (`streamlit run` ou `pytest`).
- [ ] Tests et lint passent localement.
- [ ] Documentation mise à jour (`README`, docstring, screenshots).
- [ ] Si nouveau modèle : enregistré dans `models/` (< 10 Mo) et référencé dans `docs/`.
- [ ] L’**issue** liée est mentionnée (`Fixes #42`).

---

## 🤝 Code of Conduct

Nous appliquons le [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). En contribuant, vous acceptez de respecter ces règles.

Merci encore !  
— Rémi & la communauté
