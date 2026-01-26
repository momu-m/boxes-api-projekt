# 🎓 Spickzettel für deine Prüfung

Hier sind die einfachsten Erklärungen für deinen Code. Wenn der Dozent fragt, kannst du das antworten.

---

## 1. Was macht dein Projekt?
"Ich habe eine **Verwaltung für Lagerkisten** programmiert. Man kann Kisten erstellen, ansehen, ändern und löschen."
*(Fachbegriff: Das nennt man **CRUD** - Create, Read, Update, Delete)*

---

## 2. Die schwierigen Begriffe (Einfach erklärt)

### "Was ist REST?"
**Antwort:** "Das ist ein Regelwerk für meine App. Es bedeutet, dass mein Server nicht speichert, wer gerade angemeldet ist (**Zustandslosigkeit**) und dass wir alles mit Standard-Befehlen machen (GET, POST, DELETE)."

### "Was ist HATEOAS?" (Wichtig für Punkte!)
**Antwort:** "Das bedeutet, dass meine API dem Benutzer 'Links' gibt, damit er weiß, wo er als nächstes hinklicken kann. Wie ein Navigationssystem."
*   **Im Code:** Schau in `app.py` bei `def to_dict`. Da steht `_links`.

### "Was ist Caching?" (Wichtig für Punkte!)
**Antwort:** "Das hilft, Daten schneller zu laden. Mein Server sagt dem Browser: 'Du kannst dir diese Antwort für 60 Sekunden merken, du musst nicht sofort wieder fragen'."
*   **Im Code:** Schau in `app.py` bei `@app.after_request`.

---

## 3. Deine Dateien erklärt

### `app.py` (Der Chef)
Das ist dein Hauptprogramm.
*   **Flask:** Der Webserver (der Kellner).
*   **SQLAlchemy:** Die Verbindung zur Datenbank.
*   **@app.route:** Die Türen, durch die man reinkommt (z.B. `/boxes`).

### `boxes.db` (Das Gedächtnis)
Hier werden die Kisten wirklich gespeichert. Es ist eine einfache Datei, wie eine Excel-Tabelle, aber für Programme.

### `test_api.py` (Der Beweis)
Das ist ein automatischer Test.
*   **Warum hast du das?** "Um sicherzugehen, dass mein Code funktioniert, bevor ich ihn abgebe. Er prüft alle Funktionen automatisch."

### `mein_test_ablauf.py` (Dein Vorführ-Skript)
(Früher hieß es `demo_script.py`)
Das ist das Skript, das du startest, um dem Dozenten alles live zu zeigen. Es drückt quasi "automatisch" alle Knöpfe nacheinander.

---

## 4. Häufige Fragen vom Dozenten

**Dozent:** "Warum benutzen Sie `Methods=['GET']`?"
**Du:** "GET ist zum **Lesen** von Daten da. Ich will ja nur Daten holen, nichts ändern."

**Dozent:** "Warum benutzen Sie `Methods=['POST']`?"
**Du:** "POST ist zum **Erstellen** da. Damit sende ich neue Daten an den Server."

**Dozent:** "Was passiert bei Fehler 404?"
**Du:** "Das heißt 'Nicht gefunden'. Wenn ich eine Kiste suche, die es nicht gibt, sende ich diesen Code zurück."
