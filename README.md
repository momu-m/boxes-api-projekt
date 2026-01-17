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
   Die API läuft unter `http://127.0.0.1:5000`.

## API Beispiele (mit `curl` testen)
*(Siehe Beispiele im vorherigen Abschnitt oder in der app.py Kommentare)*
