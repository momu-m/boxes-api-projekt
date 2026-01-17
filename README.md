# Kisten-Verwaltungs API 📦

Dies ist ein einfaches Schulungsprojekt für eine REST API zur Verwaltung von Lagerkisten.

## Funktionen
- **GET /boxes**: Zeigt alle Kisten an.
- **POST /boxes**: Erstellt eine neue Kiste.
- **PUT /boxes/<code\>**: Ändert den Inhalt oder Ort einer Kiste.
- **DELETE /boxes/<code\>**: Löscht eine Kiste.

## Installation & Start

1. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **API starten:**
   ```bash
   python app.py
   ```
   Die API läuft dann unter `http://127.0.0.1:5000`.

## API Beispiele (mit `curl` testen)

Wenn die API läuft, kannst du sie in einem neuen Terminal-Fenster testen:

### 1. Eine Kiste hinzufügen (POST)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"code": "K-001", "location": "Keller", "content": "Werkzeug"}' http://127.0.0.1:5000/boxes
```

### 2. Alle Kisten abrufen (GET)
```bash
curl http://127.0.0.1:5000/boxes
```

### 3. Kiste ändern (PUT)
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"content": "Altes Werkzeug"}' http://127.0.0.1:5000/boxes/K-001
```

### 4. Kiste löschen (DELETE)
```bash
curl -X DELETE http://127.0.0.1:5000/boxes/K-001
```

## Datenbank
Die Daten werden in der lokalen Datei `boxes.db` (SQLite) gespeichert.
