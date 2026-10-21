# Changelog

## Non publié

- Ajoute `GET /competitions/{competition_id}/stats` : nombre d'épreuves, d'inscriptions confirmées et de résultats (200, 404, 422).
- Harmonise le router des résultats : `GET /events/{event_id}/ranking` renvoie la liste nue (plus d'enveloppe `{"data", "count"}`) et lève `NotFoundError` (404) ; ajoute un `summary` à chaque route.
- Ajoute `GET /athletes/{athlete_id}` : détail d'un athlète (200, 404, 422).
