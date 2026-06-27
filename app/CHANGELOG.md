# Journal des versions – Ubisoft People Analytics

Tous les changements notables de ce projet seront consignés ici en suivant la nomenclature [SemVer](https://semver.org/lang/fr/).

---

## [1.0.0] – 2025-08-25
### Ajouté
- Déploiement Kubernetes (manifests `deployment/k8s/`).
- Workflow CI/CD complet : lint, tests, build Docker, push sur GHCR.
- Tableau de bord Prometheus / Grafana pour la surveillance des métriques modèles.

### Modifié
- Refactor complet du code vers structure `src/`.
- README enrichi (table des matières, badges dynamiques, GIF).

---

## [0.2.0] – 2025-07-15
### Ajouté
- `Dockerfile` + `docker-compose.yml` pour environnement dev + PostgreSQL.
- Scripts d’entraînement MLflow (`train_model.py`).
- Exemple de données anonymisées (`data/sample_data.csv`).

### Corrigé
- Validation du formulaire Streamlit (bug champs vides).

---

## [0.1.0] – 2025-06-30
### Ajouté
- Première démo Streamlit hébergée (`app.py`).
- Classification RandomForest (F1 96 %).
- README initial, licenses, structure basique du repo.
