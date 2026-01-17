# Kisten-Verwaltungs API 📦

Dies ist ein einfaches Schulungsprojekt für eine REST API zur Verwaltung von Lagerkisten.

## Funktionen
- **GET /boxes**: Zeigt alle Kisten an.
- **POST /boxes**: Erstellt eine neue Kiste.
- **PUT /boxes/<code\>**: Ändert den Inhalt oder Ort einer Kiste.
- **DELETE /boxes/<code\>**: Löscht eine Kiste.

## Installation & Start (Der Profi-Weg)

1. **Virtuelle Umgebung erstellen:**
   ```bash
   python3 -m venv venv
   ```

2. **Umgebung aktivieren:**
   - MacOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **API starten:**
   ```bash
   python app.py
   ```
   Die API läuft unter `http://127.0.0.1:5006`.

## API Beispiele (mit `curl` testen)

### 1. Eine Kiste hinzufügen (POST)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"code": "K-001", "location": "Keller", "content": "Werkzeug"}' http://127.0.0.1:5006/boxes
```

### 2. Alle Kisten abrufen (GET)
```bash
curl http://127.0.0.1:5006/boxes
```

### 3. Kiste ändern (PUT)
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"content": "Altes Werkzeug"}' http://127.0.0.1:5006/boxes/K-001
```

### 4. Kiste löschen (DELETE)
```bash
curl -X DELETE http://127.0.0.1:5006/boxes/K-001
```

## Datenbank
Die Daten werden in der lokalen Datei `boxes.db` (SQLite) gespeichert.
