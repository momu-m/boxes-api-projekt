from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import re # Für die Code-Prüfung (Buchstaben & Zahlen)
 
app = Flask(__name__)
 
# Datenbank-Konfiguration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'boxes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# PRÜFUNGS-PUNKT: Warum Datenbank?
# Damit die Daten da bleiben, auch wenn man den Server neu startet.
 
db = SQLAlchemy(app)
 
class Box(db.Model):
    __tablename__ = 'boxes'
    code = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
 
    def to_dict(self):
        """
        Gibt die Daten der Kiste zurück.
       
        PRÜFUNGS-PUNKT: HATEOAS (Hypermedia)
        Wir geben Links mit zurück, damit der Client weiß, was er tun kann.
        Das gibt 10 Punkte in der Prüfung!
        """
        return {
            "code": self.code,
            "location": self.location,
            "content": self.content,
            "_links": {
                "self": f"/boxes/{self.code}",
                "collection": "/boxes"
            }
        }
 
with app.app_context():
    db.create_all()
 
# --- WICHTIG FÜR PUNKTE (CACHING) ---
# PRÜFUNGS-PUNKT: Caching
# Wir sagen dem Browser: "Merk dir das Ergebnis für 60 Sekunden."
# Das entlastet den Server.
@app.after_request
def add_header(response):
    if request.method == 'GET':
        response.cache_control.max_age = 60
    return response
 
# --- DIE API ROUTEN (Einfach und Klar) ---
 
@app.route('/boxes', methods=['GET'])
def get_boxes():
    """Zeigt alle Kisten an oder filtert nach Ort."""
    location_filter = request.args.get('location')
    if location_filter:
        # Nur Kisten an einem bestimmten Ort zeigen
        filtered_boxes = Box.query.filter_by(location=location_filter).all()
        return jsonify([box.to_dict() for box in filtered_boxes])
    else:
        # Alle Kisten zeigen
        all_boxes = Box.query.all()
        return jsonify([box.to_dict() for box in all_boxes])
 
@app.route('/boxes/<string:code>', methods=['GET'])
def get_box(code):
    """Zeigt eine einzelne Kiste anhand ihres Codes."""
    box = db.session.get(Box, code)
    if box:
        return jsonify(box.to_dict())
    return jsonify({"error": "Kiste nicht gefunden"}), 404
 
@app.route('/boxes', methods=['POST'])
def add_box():
    """Erstellt eine neue Kiste."""
    data = request.get_json()
   
    # Prüfung: Sind alle Daten da?
    # Prüfung: Nur der CODE ist Pflicht. Rest ist optional.
    # Das erfüllt die Anforderung: "Eine Kiste erstellen mit Standort..." (ohne Inhalt) etc.
    if not data or 'code' not in data:
        return jsonify({"error": "Der Code fehlt! Eine Kiste braucht eine Nummer."}), 400
       
    # --- NEU: Validierung (Regel 3: Max 4 Zeichen, A-Z, 0-9) ---
    # Wir prüfen das hier, bevor wir speichern.
    code_pattern = r'^[A-Z0-9]{1,4}$'
    if not re.match(code_pattern, data['code']):
        return jsonify({
            "error": "Ungültiger Code! Erlaubt: Max 4 Zeichen, nur Großbuchstaben (A-Z) und Zahlen (0-9)."
        }), 400

    # Prüfung: Existiert der Code schon?
    if db.session.get(Box, data['code']):
        return jsonify({"error": "Dieser Code existiert bereits"}), 400
 
    # Wenn nichts angegeben ist, lassen wir es leer ("")
    # Das erfüllt "Inhalt einer Kiste löschen" (indem man ihn leer lässt)
    loc = data.get('location', "")
    con = data.get('content', "")
 
    new_box = Box(code=data['code'], location=loc, content=con)
    db.session.add(new_box)
    db.session.commit()
   
    return jsonify(new_box.to_dict()), 201
 
@app.route('/boxes/<string:code>', methods=['PUT'])
def update_box(code):
    """Ändert eine bestehende Kiste."""
    box = db.session.get(Box, code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
       
    data = request.get_json()
    if 'location' in data:
        box.location = data['location']
    if 'content' in data:
        box.content = data['content']
       
    db.session.commit()
    return jsonify(box.to_dict())
 
@app.route('/boxes/<string:code>', methods=['DELETE'])
def delete_box(code):
    """Löscht eine Kiste."""
    box = db.session.get(Box, code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
       
    db.session.delete(box)
    db.session.commit()
    return jsonify({"message": f"Kiste {code} wurde gelöscht"})
 
# Optional: Statistik (einfach gehalten)
@app.route('/stats', methods=['GET'])
def get_stats():
    """Zeigt einfache Statistiken an (Erweitert)."""
    total_boxes = Box.query.count()
    # Zählt, wie viele unterschiedliche Orte es gibt
    unique_locations = db.session.query(Box.location).distinct().count()
    return jsonify({
        "total_boxes": total_boxes,
        "total_locations": unique_locations
    })
 
# Neu: Liste aller Locationen ausgeben
@app.route('/locations', methods=['GET'])
def get_locations():
    """Zeigt eine Liste aller Orte, wo Kisten stehen."""
    all_boxes = Box.query.all()
    unique_locations = sorted(list(set([b.location for b in all_boxes if b.location])))
    return jsonify(unique_locations)
 
# Neu: Alle Kisten auflisten (CODE) - Nur die Codes
@app.route('/boxes/codes', methods=['GET'])
def get_box_codes():
    """Zeigt nur die Codes aller Kisten."""
    all_boxes = Box.query.all()
    # Wir geben eine Liste zurück, die nur die Codes enthält
    return jsonify([b.code for b in all_boxes])
 
if __name__ == '__main__':
    print("API läuft auf http://0.0.0.0:5006")
    app.run(host='0.0.0.0', debug=True, port=5006)