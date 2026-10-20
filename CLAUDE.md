# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commandes

```bash
pip install -e ".[dev]"
pytest
pytest tests/test_athletes.py::test_get_athlete_returns_athlete   # un seul test
ruff check . && ruff format .
python scripts/seed.py --reset
uvicorn app.main:app --reload
```

## Règles

- Lancer `pytest` avant tout commit ; ne pas commiter si un test échoue.
- Lancer `ruff check . && ruff format .` après toute modification de fichier Python.
- Lever une sous-classe d'`ApiError` (`app/errors.py`) pour toute erreur métier ; ne jamais utiliser `HTTPException`.
- Ne jamais appeler `conn.commit()` dans `app/repositories/` : la dépendance `Conn` (`app/db.py`) commite et fait le rollback.
- Ne jamais stocker `category` d'un athlète en base : elle est calculée par `age_category` (`app/categories.py`).
- Ne jamais lire ni afficher .env : il contient des secrets.
- Après toute modification de `v_public_athletes` ou `v_public_results` dans `app/schema.sql`, adapter `scripts/mcp_dossard.py`.
- Pas de migrations : `app/schema.sql` est rejoué à chaque démarrage ; n'y utiliser que `CREATE ... IF NOT EXISTS`.

## Tests

- Créer les données de test avec les fixtures `make_competition`, `make_event`, `make_athlete`, `make_registration` de `tests/conftest.py`.
- Mettre les tests d'un router dans `tests/test_<entité>.py`.
- Ajouter un test pour chaque code 404, 409 et 422 que l'endpoint peut renvoyer.

## Routes ajoutées ou modifiées

- Ajouter ou modifier la ligne de la route dans `docs/api.md`, avec ses codes de statut.
- Ajouter une entrée en tête de la section « Non publié » de `CHANGELOG.md` (créer le fichier s'il n'existe pas).

## Interdits sans demande explicite

- Modifier ou supprimer un fichier de `scripts/legacy/` (lecture autorisée).
- Ajouter une dépendance dans `pyproject.toml`.
