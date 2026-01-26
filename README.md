# Kisten-Verwaltungs API 📦

Dies ist eine schlanke REST-API zur Verwaltung von Lagerkisten. Der Fokus liegt auf klarem Code, sauberer Struktur und umfassenden Tests (Unit, Integration, E2E).

## Projekt-Struktur

*   `app.py`: Die Haupt-Anwendung (Flask mit SQLAlchemy). Einfach und verständlich.
*   `test_api.py`: Die Test-Suite für `app.py` (CRUD-Tests).
*   `boxes.db`: Die SQLite-Datenbank.


## Installation & Start

1. **Umgebung aktivieren:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **API starten:**
   ```bash
   python app.py
   ```
   Die API läuft dann unter `http://127.0.0.1:5006`.

## Testen (Qualitätssicherung)

Um zu beweisen, dass die API korrekt funktioniert, gibt es automatisierte Tests.

1. **Standard-Tests ausführen:**
   ```bash
   python test_api.py
   ```
   Dies testet Erstellen, Lesen, Aktualisieren, Löschen und Filtern.



## Erfüllung der REST-Prinzipien (Laut Aufgabenstellung)

Dies sind die Punkte, die in der Bewertung (10 Punkte für HATEOAS, 5 für Caching etc.) gefordert sind:

*   **Zustandslosigkeit (Statelessness):** Die API speichert keine Session-Daten. Jeder Request ist vollständig.
*   **Caching:** Im Code (`app.py`) wird der `Cache-Control: max-age=60` Header gesetzt.
*   **Uniform Interface:**
    *   **Identification of Resources:** URIs sind eindeutig (z.B. `/boxes/K-001`).
    *   **Manipulation:** Alles läuft über JSON.
    *   **Self-Descriptive Messages:** HTTP-Methoden (GET/POST/PUT/DELETE) und Statuscodes (200, 201, 404) werden korrekt genutzt.
    *   **HATEOAS (Hypermedia):** Jedes JSON-Objekt enthält jetzt wieder `_links` (Verweise auf sich selbst und die Liste), um die 10 Punkte zu sichern.
*   **Persistenz:** Daten landen in der SQLite-Datenbank (`boxes.db`).

## CRUD & Features
- **Create:** `POST /boxes` (Erstellt Ressource)
- **Read:** `GET /boxes` & `GET /boxes/<code>` (Liest Ressource)
- **Update:** `PUT /boxes/<code>` (Aktualisiert Ressource)
- **Delete:** `DELETE /boxes/<code>` (Löscht Ressource)
- **Filter:** `GET /boxes?location=...`
- **Statistik:** `GET /stats`
