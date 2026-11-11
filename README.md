# Financia – API

## Installation
```
python -m venv .venv
.venv\Scripts\activate            # Windows (Linux/macOS : source .venv/bin/activate)
pip install -r requirements-dev.txt
alembic upgrade head              # crée les tables
```

## Lancer (toujours depuis la racine du projet)
```
uvicorn backend.main:app --reload
```
Documentation interactive : http://127.0.0.1:8000/docs

## Tests
```
pytest
```

## Migrations (après avoir modifié un model)
```
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Organisation
Un dossier par module métier (`referentiel/`, plus tard `bia/`, `risques/`...),
chacun avec `models.py` (tables), `schemas.py` (validation), `service.py`
(règles métier) et `router.py` (routes). `core/` contient la configuration et
la base de données. Un nouveau module avec des tables : importer son
`models.py` dans `alembic/env.py`.


# Financia – Application de cartographie des risques SMCA

Application backend permettant d’identifier, d’évaluer, de valider et de suivre les risques liés à la continuité des activités de Financia.

## Architecture technique

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite en développement
- PostgreSQL prévu pour la production
- Pytest
- Architecture en monolithe modulaire

## Modules développés

### 1. Référentiel

Le module Référentiel gère les éléments de base utilisés dans l’analyse des risques.

#### Activités

Une activité contient :

- nom
- description
- statut d’archivage

Fonctionnalités backend :

- créer une activité
- consulter les activités
- consulter une activité
- archiver une activité

#### Ressources

Une ressource contient :

- nom
- type de ressource
- description
- statut d’archivage

Fonctionnalités backend :

- créer une ressource
- consulter les ressources
- consulter une ressource
- archiver une ressource

#### Dépendances

Une dépendance relie une activité à une ressource.

Elle contient :

- activité associée
- ressource associée
- niveau de criticité
- caractère indispensable
- solution alternative

Les doublons sont interdits.

---

### 2. BIA – Business Impact Analysis

Le module BIA permet d’évaluer les conséquences d’une interruption d’activité.

Une BIA contient :

- activité concernée
- responsable
- heures de fonctionnement
- sites concernés
- période de pointe
- MTPD
- RTO
- RPO
- capacité minimale
- justifications
- impacts selon plusieurs horizons temporels
- statut de validation

Les statuts possibles sont :

- brouillon
- soumis
- validé
- à corriger

Règles principales :

- le RTO doit être inférieur à la MTPD
- les valeurs RTO, RPO et MTPD sont contrôlées
- une activité ne peut posséder qu’une seule BIA
- une BIA validée doit être complète
- les impacts peuvent être renseignés pour les horizons 1, 4, 8, 24 et 72 heures

---

### 3. Registre des risques

Le module Risques permet d’identifier et d’évaluer les risques.

Un risque contient :

- scénario
- cause
- menace
- vulnérabilité
- conséquences
- propriétaire
- activités associées
- ressources associées
- probabilité
- impact
- score de criticité
- niveau de risque
- statut de validation

#### Échelle de cotation

La probabilité et l’impact utilisent une échelle de 1 à 5.

Le score est calculé automatiquement :

```text
Score = Probabilité × Impact