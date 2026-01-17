from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Datenbank-Konfiguration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'boxes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modell mit HATEOAS Unterstützung
class Box(db.Model):
    __tablename__ = 'boxes'
    code = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """Erzeugt eine Repräsentation inklusive Hypermedia-Links (HATEOAS)."""
        return {
            "code": self.code,
            "location": self.location,
            "content": self.content,
            "_links": {
                "self": {"href": f"/boxes/{self.code}"},
                "collection": {"href": "/boxes"}
            }
        }

with app.app_context():
    db.create_all()

# --- REST PRINZIP: CACHING ---
@app.after_request
def add_header(response):
    """Setzt korrekte Caching-Header für alle GET Requests."""
    if request.method == 'GET':
        # Erlaubt das Caching für 60 Sekunden
        response.cache_control.max_age = 60
        response.cache_control.public = True
    return response

# --- DIE API ROUTEN ---

@app.route('/boxes', methods=['GET'])
def get_boxes():
    all_boxes = Box.query.all()
    return jsonify([box.to_dict() for box in all_boxes])

@app.route('/boxes/<string:code>', methods=['GET'])
def get_box(code):
    box = db.session.get(Box, code)
    if box:
        return jsonify(box.to_dict())
    return jsonify({"error": "Kiste nicht gefunden"}), 404

@app.route('/boxes', methods=['POST'])
def add_box():
    data = request.get_json()
    if not data or 'code' not in data or 'location' not in data or 'content' not in data:
        return jsonify({"error": "Fehlende Daten"}), 400
        
    if db.session.get(Box, data['code']):
        return jsonify({"error": "Code existiert bereits"}), 400

    new_box = Box(code=data['code'], location=data['location'], content=data['content'])
    db.session.add(new_box)
    db.session.commit()
    
    return jsonify({"message": "Kiste erstellt", "box": new_box.to_dict()}), 201

@app.route('/boxes/<string:code>', methods=['PUT'])
def update_box(code):
    box = db.session.get(Box, code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
        
    data = request.get_json()
    if 'location' in data: box.location = data['location']
    if 'content' in data: box.content = data['content']
        
    db.session.commit()
    return jsonify(box.to_dict())

@app.route('/boxes/<string:code>', methods=['DELETE'])
def delete_box(code):
    box = db.session.get(Box, code)
    if not box:
        return jsonify({"error": "Kiste nicht gefunden"}), 404
        
    db.session.delete(box)
    db.session.commit()
    return jsonify({"message": f"Kiste {code} gelöscht"})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    print("API läuft auf http://127.0.0.1:5006")
    app.run(debug=True, port=5006)
