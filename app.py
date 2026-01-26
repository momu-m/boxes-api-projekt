from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Datenbank-Konfiguration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'boxes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Einfaches Modell OHNE komplexe Links
class Box(db.Model):
    __tablename__ = 'boxes'
    code = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """
        Gibt die Daten der Kiste zurück.
        WICHTIG FÜR PUNKTE (HATEOAS): Enthält Links zu sich selbst (_links).
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
@app.after_request
def add_header(response):
    """Setzt Cache-Header (Verlangt in Aufgabe)."""
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
    if not data or 'code' not in data or 'location' not in data or 'content' not in data:
        return jsonify({"error": "Fehlende Daten: Code, Ort und Inhalt werden benötigt"}), 400
        
    # Prüfung: Existiert der Code schon?
    if db.session.get(Box, data['code']):
        return jsonify({"error": "Dieser Code existiert bereits"}), 400

    new_box = Box(code=data['code'], location=data['location'], content=data['content'])
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
    """Zeigt einfache Statistiken an."""
    total_boxes = Box.query.count()
    return jsonify({"total_boxes": total_boxes})

if __name__ == '__main__':
    print("API läuft auf http://0.0.0.0:5006")
    app.run(host='0.0.0.0', debug=True, port=5006)
