# Kisten-Verwaltungs API 📦

Eine REST-API zur Verwaltung von Lagerkisten, entwickelt als Semesterarbeit "Software Engineering".

---

## 👥 Team

**Entwickelt von:**
- Momu M.
- Arjan
- Andrin

**Repository:** https://github.com/momu-m/boxes-api-projekt.git

---

## 📁 Projekt-Struktur

```
boxes-api-projekt/
├── app.py                 # Haupt-Anwendung (Flask + SQLAlchemy)
├── test_pytest.py         # Automatisierte Tests (Pytest)
├── boxes.db               # SQLite-Datenbank
├── requirements.txt       # Python-Abhängigkeiten
└── README.md              # Diese Datei
```

---

## 🚀 Installation & Start

### 1. Repository klonen
```bash
git clone https://github.com/momu-m/boxes-api-projekt.git
cd boxes-api-projekt
```

### 2. Virtuelle Umgebung erstellen & aktivieren
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. API starten
```bash
python app.py
```

Die API läuft dann unter: **`http://127.0.0.1:5006`**

---

## 📚 API-Endpunkte & Beispiele

### **1. Kiste erstellen (CREATE)**
```bash
# Kiste mit Code, Location und Inhalt erstellen
curl -X POST http://127.0.0.1:5006/boxes \
  -H "Content-Type: application/json" \
  -d '{"code":"A1", "location":"Lager Ost", "content":"Schrauben"}'

# Antwort (201 Created):
{
  "code": "A1",
  "location": "Lager Ost",
  "content": "Schrauben",
  "_links": {
    "self": "/boxes/A1",
    "collection": "/boxes"
  }
}
```

### **2. Alle Kisten anzeigen (READ Collection)**
```bash
curl http://127.0.0.1:5006/boxes

# Antwort (200 OK):
[
  {
    "code": "A1",
    "location": "Lager Ost",
    "content": "Schrauben",
    "_links": {...}
  },
  {...}
]
```

### **3. Eine spezifische Kiste anzeigen (READ)**
```bash
curl http://127.0.0.1:5006/boxes/A1

# Antwort (200 OK):
{
  "code": "A1",
  "location": "Lager Ost",
  "content": "Schrauben",
  "_links": {...}
}
```

### **4. Kiste aktualisieren (UPDATE)**
```bash
# Location ändern
curl -X PUT http://127.0.0.1:5006/boxes/A1 \
  -H "Content-Type: application/json" \
  -d '{"location":"Lager West"}'

# Inhalt ändern
curl -X PUT http://127.0.0.1:5006/boxes/A1 \
  -H "Content-Type: application/json" \
  -d '{"content":"Nägel"}'
```

### **5. Kiste löschen (DELETE)**
```bash
curl -X DELETE http://127.0.0.1:5006/boxes/A1

# Antwort (200 OK):
{"message": "Kiste A1 wurde gelöscht"}
```

### **6. Zusätzliche Endpunkte**

#### Filter nach Location
```bash
curl http://127.0.0.1:5006/boxes?location=Lager%20Ost
```

#### Statistik
```bash
curl http://127.0.0.1:5006/stats

# Antwort:
{
  "total_boxes": 5,
  "total_locations": 3
}
```

#### Alle Locations
```bash
curl http://127.0.0.1:5006/locations

# Antwort:
["Lager Ost", "Lager West", "Keller"]
```

#### Alle Codes
```bash
curl http://127.0.0.1:5006/boxes/codes

# Antwort:
["A1", "B2", "C3"]
```

---

## ✅ Erfüllung der Anforderungen

### **REST-Prinzipien (60 von 80 Punkten)**

#### 1. **Zustandslosigkeit** (5 Punkte)
- ✅ Die API speichert **keine Session-Daten** zwischen Requests
- ✅ Jeder Request ist **vollständig** und unabhängig
- ✅ Keine serverseitigen Benutzer-Informationen

#### 2. **Caching** (5 Punkte)
- ✅ Implementiert in `app.py` Zeile 49-53
- ✅ GET-Requests erhalten Header: `Cache-Control: max-age=60`
- ✅ Browser können Antworten 60 Sekunden lang zwischenspeichern

**Code:**
```python
@app.after_request
def add_header(response):
    if request.method == 'GET':
        response.cache_control.max_age = 60
    return response
```

#### 3. **Identification of Resources** (5 Punkte)
- ✅ Jede Kiste hat eine **eindeutige URI**: `/boxes/{code}`
- ✅ Beispiel: `/boxes/A1`, `/boxes/B2`

#### 4. **Manipulation of Resources through Representations** (5 Punkte)
- ✅ Alle Daten sind im **JSON-Format**
- ✅ Content-Type: `application/json`

#### 5. **Self-Descriptive Messages** (10 Punkte)
- ✅ Korrekte **HTTP-Methoden**: GET, POST, PUT, DELETE
- ✅ Korrekte **Status-Codes**:
  - `200 OK` - Erfolgreiche GET/PUT/DELETE
  - `201 Created` - Neue Kiste erstellt
  - `404 Not Found` - Kiste existiert nicht
  - `400 Bad Request` - Ungültige Daten

#### 6. **HATEOAS - Hypermedia as the Engine of Application State** (10 Punkte)
- ✅ Implementiert in `app.py` Zeile 24-40 (Methode `to_dict()`)
- ✅ Jede JSON-Antwort enthält `_links` mit:
  - `self`: Link zur eigenen Ressource
  - `collection`: Link zur gesamten Collection

**Beispiel:**
```json
{
  "code": "A1",
  "location": "Lager Ost",
  "content": "Schrauben",
  "_links": {
    "self": "/boxes/A1",
    "collection": "/boxes"
  }
}
```

### **Datenbank (10 Punkte)**
- ✅ Daten werden in **SQLite-Datenbank** (`boxes.db`) persistiert
- ✅ Verwendung von **SQLAlchemy** ORM
- ✅ Daten bleiben erhalten, auch nach Server-Neustart

### **Testing (10 Punkte)**
- ✅ Vollständige automatisierte Tests in `test_pytest.py`
- ✅ Testet alle CRUD-Operationen:
  - `test_create_item` - Kiste erstellen
  - `test_get_all_items` - Alle Kisten abrufen
  - `test_get_specific_item` - Eine Kiste abrufen
  - `test_update_item` - Kiste aktualisieren
  - `test_delete_item` - Kiste löschen
- ✅ Nutzt **Pytest Fixtures** für Setup/Teardown

**Tests ausführen:**
```bash
python -m pytest test_pytest.py -v
```

### **Vollständigkeit CRUD (10 Punkte)**
- ✅ **Create:** `POST /boxes`
- ✅ **Read Collection:** `GET /boxes`
- ✅ **Read Single:** `GET /boxes/{code}`
- ✅ **Update:** `PUT /boxes/{code}`
- ✅ **Delete:** `DELETE /boxes/{code}`

---

## 🔐 Business-Logik & Validierung

### **Code-Regeln:**
- ✅ Maximale Länge: **4 Zeichen**
- ✅ Erlaubte Zeichen: **A-Z** (Großbuchstaben) und **0-9** (Zahlen)
- ✅ Validierung in `app.py` Zeile 91-95

**Beispiele:**
- ✅ Gültig: `A1`, `B2`, `XY12`, `Z999`
- ❌ Ungültig: `ABCDE` (zu lang), `abc` (Kleinbuchstaben), `A-1` (Sonderzeichen)

**Fehlermeldung:**
```json
{
  "error": "Ungültiger Code! Erlaubt: Max 4 Zeichen, nur Großbuchstaben (A-Z) und Zahlen (0-9)."
}
```

---

## 🧪 Testen

### **Automatisierte Tests**
```bash
# Alle Tests ausführen
python -m pytest test_pytest.py

# Tests mit Details
python -m pytest test_pytest.py -v

# Tests mit Coverage
python -m pytest test_pytest.py --cov=app
```

### **Manuelle Tests mit curl**
Siehe Abschnitt "API-Endpunkte & Beispiele" oben.

---

## 📊 Bewertung (Selbsteinschätzung)

| Kriterium | Punkte | Status |
|-----------|--------|--------|
| REST: Zustandslosigkeit | 5 | ✅ |
| REST: Caching | 5 | ✅ |
| REST: Identification of Resources | 5 | ✅ |
| REST: Manipulation through Representations | 5 | ✅ |
| REST: Self-Descriptive Messages | 10 | ✅ |
| REST: HATEOAS | 10 | ✅ |
| Datenbank: Persistenz | 10 | ✅ |
| Testing: Vollständig | 10 | ✅ |
| Vollständigkeit CRUD | 10 | ✅ |
| Dokumentation (README) | 10 | ✅ |
| **GESAMT** | **80** | **80/80** |

---

## 📝 Weitere Informationen

- **Python Version:** 3.8+
- **Flask Version:** 3.0.0
- **SQLAlchemy Version:** 3.1.1
- **Pytest Version:** 8.3.4

---

## 📧 Kontakt

Bei Fragen zum Projekt: Siehe Team-Mitglieder oben.

**Repository:** https://github.com/momu-m/boxes-api-projekt.git
