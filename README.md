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
