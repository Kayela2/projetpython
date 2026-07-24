# Serenity — Prédiction du risque de dépression étudiante

Projet M1 Data Science — classification supervisée (Kernel SVM) sur le dataset `student_lifestyle_100k`, avec une application web complète (React + FastAPI) plutôt qu'une simple app Streamlit.

- **Variable cible :** `Depression` (binaire)
- **Algorithme imposé :** Kernel SVM (noyau RBF)
- **Dataset :** 100 000 étudiants, 9 variables explicatives (âge, genre, département, CGPA, sommeil, heures d'étude, réseaux sociaux, activité physique, niveau de stress)

## Architecture

```
student-depression-ml/
├── notebooks/           # 01_EDA, 02_Underfitting, 03_Overfitting, 04_Optimisation
├── src/                 # Pipeline de prétraitement partagé par les notebooks (config, data, preprocessing)
├── dataset/             # Copie locale du CSV source
├── models/              # Pipeline sklearn final (.joblib) + métadonnées (model_metadata.json)
├── reports/             # Figures et métriques exportées par les notebooks
├── backend/              # API FastAPI (charge le modèle, sert les prédictions)
└── frontend/             # App React + TypeScript (maquettes UI/UX du projet)
```

## Pourquoi cette architecture (et pas Streamlit)

Le prétraitement (`src/preprocessing.py`) est écrit une seule fois et importé par les 4 notebooks, pour garantir que la comparaison Underfitting / Overfitting / Optimisation porte uniquement sur les hyperparamètres du modèle — pas sur des différences de préparation des données. Le pipeline final (prétraitement + SVM) est sauvegardé comme un seul objet `joblib`, ce qui évite de dupliquer la logique de feature engineering côté API.

## Résultats clés

- **EDA (100 000 lignes)** : dataset propre (0 valeur manquante, 0 doublon), cible déséquilibrée (`Depression=True` = 10.06 %, ratio 8.94:1), corrélations linéaires faibles avec la cible (`CGPA` = -0.18 au maximum) — ce qui justifie un modèle à noyau non-linéaire plutôt qu'un modèle linéaire.
- **Underfitting** (`C=0.001, gamma=0.001`) : F1 = 0.000 sur train et test — le modèle prédit uniquement la classe majoritaire.
- **Overfitting** (`C=1000, gamma=1`) : F1 train = 1.000, F1 test = 0.064 — mémorisation du train, écart massif avec le test.
- **Optimisation** (GridSearchCV, 5-fold stratifié, scoring F1) : meilleurs hyperparamètres `C=10, gamma=0.01, class_weight='balanced'` → F1 test = **0.287**, recall = **0.602**, ROC AUC = **0.667**.

Les notebooks de modélisation (Underfitting/Overfitting/Optimisation) tournent sur un **échantillon stratifié de 12 000 lignes** (et non les 100 000 lignes complètes) : le Kernel SVM (libsvm) a une complexité proche de O(n²·⁵), ce qui rend l'entraînement sur le dataset complet impraticable en temps interactif (benchmark : ~15-20 min pour un seul fit à 80 000 lignes, ce qui aurait rendu GridSearchCV — des dizaines de fits — irréalisable). Le sous-échantillonnage préserve le ratio de déséquilibre 8.94:1 (voir `src/config.py`).

## Prérequis

- Python 3.12 avec un environnement virtuel dédié (pandas, scikit-learn, seaborn, jupyter, fastapi, uvicorn — voir `backend/requirements.txt`)
- Node.js 22+ / npm 10+
- Un kernel Jupyter enregistré pointant vers ce même environnement (voir ci-dessous) — **important** : les notebooks et le backend doivent utiliser le même environnement pour éviter les incompatibilités de version de `scikit-learn` lors du chargement du modèle sauvegardé.

```bash
# Enregistrer le kernel Jupyter du venv du projet (une seule fois)
pip install ipykernel
python -m ipykernel install --user --name student-depression-venv --display-name "Python (student-depression-ml venv)"
```

## Reproduire les notebooks

```bash
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_EDA.ipynb --ExecutePreprocessor.kernel_name=student-depression-venv
jupyter nbconvert --to notebook --execute --inplace 02_Underfitting.ipynb --ExecutePreprocessor.kernel_name=student-depression-venv
jupyter nbconvert --to notebook --execute --inplace 03_Overfitting.ipynb --ExecutePreprocessor.kernel_name=student-depression-venv
jupyter nbconvert --to notebook --execute --inplace 04_Optimisation.ipynb --ExecutePreprocessor.kernel_name=student-depression-venv
```

`04_Optimisation.ipynb` régénère `models/depression_svm_pipeline.joblib` et `models/model_metadata.json`, consommés par le backend.

## Lancer le backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- `GET /api/health` — statut de chargement du modèle
- `GET /api/model/info` — hyperparamètres et métriques du modèle
- `POST /api/predict` — prédiction (voir `backend/app/schemas.py` pour le payload)

Tests : `pip install -r requirements-dev.txt && pytest tests/ -v`

## Lancer le frontend

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173 (le backend doit tourner sur :8000)
npm test          # tests unitaires (Vitest)
npm run test:e2e  # test end-to-end (Playwright) — backend + frontend doivent déjà tourner
```

## Avertissement

Les prédictions sont générées par un modèle statistique à des fins pédagogiques et ne constituent en aucun cas un diagnostic médical.
