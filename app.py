from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Datenbank-Konfiguration: Wir nutzen SQLite und die Datei boxes.db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'boxes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank-Objekt erstellen
db = SQLAlchemy(app)

# Das Modell: So sieht unsere Tabelle "boxes" aus
class Box(db.Model):
    __tablename__ = 'boxes'
    code = db.Column(db.String(50), primary_key=True) # Der eindeutige Code (z.B. K-100)
    location = db.Column(db.String(100), nullable=False) # Der Ort (z.B. Keller)
    content = db.Column(db.String(200), nullable=False) # Der Inhalt (z.B. Kleidung)

    def to_dict(self):
        """Hilfsfunktion: Wandelt das Datenbank-Objekt in ein Format (Dictionary) um, das JSON versteht."""
        return {
            "code": self.code,
            "location": self.location,
            "content": self.content
        }

# Datenbank und Tabelle erstellen, falls sie noch nicht existieren
with app.app_context():
    db.create_all()

# --- DIE API ROUTEN ---

# 1. Alle Kisten abrufen (GET)
@app.route('/boxes', methods=['GET'])
def get_boxes():
    all_boxes = Box.query.all()
    # Wir wandeln alle Kisten in eine Liste von Dictionaries um
    return jsonify([box.to_dict() for box in all_boxes])

# 2. Eine einzelne Kiste abrufen (GET)
@app.route('/boxes/<string:code>', methods=['GET'])
def get_box(code):
    box = Box.query.get(code)
    if box:
        return jsonify(box.to_dict())
    return jsonify({"error": "Kiste nicht gefunden"}), 404

# 3. Eine neue Kiste erstellen (POST)
@app.route('/boxes', methods=['POST'])
def add_box():
    data = request.get_json()
    
    # Prüfen, ob alle Daten da sind
    if not data or 'code' not in data or 'location' not in data or 'content' not in data:
        return jsonify({"error": "Fehlende Daten (code, location, content werden benötigt)"}), 400
        
    # Prüfen, ob der Code schon existiert
    if Box.query.get(data['code']):
        return jsonify({"error": "Eine Kiste mit diesem Code existiert bereits"}), 400

    new_box = Box(
        code=data['code'],
        location=data['location'],
        content=data['content']
    )
    
    db.session.add(new_box)
    db.session.commit()
    
    return jsonify({"message": "Kiste erfolgreich hinzugefügt", "box": new_box.to_dict()}), 201

# 4. Eine Kiste aktualisieren (PUT)
@app.route('/boxes/<string:code>', methods=['PUT'])
def update_box(code):
    box = Box.query.get(code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
        
    data = request.get_json()
    if 'location' in data:
        box.location = data['location']
    if 'content' in data:
        box.content = data['content']
        
    db.session.commit()
    return jsonify({"message": "Kiste aktualisiert", "box": box.to_dict()})

# 5. Eine Kiste löschen (DELETE)
@app.route('/boxes/<string:code>', methods=['DELETE'])
def delete_box(code):
    box = Box.query.get(code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
        
    db.session.delete(box)
    db.session.commit()
    return jsonify({"message": f"Kiste {code} wurde gelöscht"})

if __name__ == '__main__':
    # Server starten
    app.run(debug=True, port=5000)
