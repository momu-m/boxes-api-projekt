# Kisten-Verwaltungs API 📦 (Transferarbeit)

Dozent: fhirter | Studierender: momu | Projekt: REST-API für Lagerboxen

## Inbetriebnahme

1. **Umgebung vorbereiten:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # MacOS/Linux
   pip install -r requirements.txt
   ```

2. **API starten:**
   ```bash
   python app.py
   ```
   Läuft unter: `http://127.0.0.1:5006`

3. **Tests ausführen:**
   ```bash
   python test_api.py
   ```

## Erfüllung der REST-Prinzipien

Dieses Projekt setzt die geforderten REST-Prinzipien wie folgt um:

*   **Zustandslosigkeit (Statelessness):** Die API speichert keine Session-Daten auf dem Server. Jeder Request enthält alle nötigen Informationen zur Verarbeitung.
*   **Caching:** Über den `Cache-Control` Header in den GET-Antworten wird dem Client signalisiert, dass Daten für 60 Sekunden gecacht werden dürfen (siehe `add_header` in `app.py`).
*   **Uniform Interface:**
    *   **Identification of Resources:** Ressourcen werden eindeutig über URIs identifiziert (z.B. `/boxes/K-001`).
    *   **Manipulation durch Repräsentationen:** Der Datenaustausch erfolgt ausschließlich via JSON.
    *   **Self-Descriptive Messages:** Es werden die korrekten HTTP-Verben (GET, POST, PUT, DELETE) und Statuscodes (200, 201, 400, 404) verwendet.
    *   **Hypermedia (HATEOAS):** Jedes Ressourcen-Objekt enthält ein `_links` Attribut mit Verweisen auf sich selbst und die Collection.
*   **Persistenz:** Alle Daten werden in einer relationalen SQLite-Datenbank (`boxes.db`) gespeichert.

## CRUD Abdeckung
- **Create:** `POST /boxes`
- **Read:** `GET /boxes` (Collection) und `GET /boxes/<code\>` (Einzeln)
- **Update:** `PUT /boxes/<code\>`
- **Delete:** `DELETE /boxes/<code\>`
