# Changelog

## Non publié

- Harmonise le router des résultats : `GET /events/{event_id}/ranking` renvoie la liste nue (plus d'enveloppe `{"data", "count"}`) et lève `NotFoundError` (404) ; ajoute un `summary` à chaque route.
- Ajoute `GET /athletes/{athlete_id}` : détail d'un athlète (200, 404, 422).
