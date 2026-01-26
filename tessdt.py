import sqlite3
from flask import Flask, request, jsonify
import threading
import random
import string
 
 
# ========================================
# 1. DATENBANK SETUP
# ========================================
 
def init_database():
    """Erstellt die Datenbank mit der definierten Struktur"""
    conn = sqlite3.connect('boxes.db')
    cursor = conn.cursor()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boxes (
            CODE TEXT PRIMARY KEY NOT NULL,
            Location TEXT,
            Content TEXT
        )
    ''')
   
    conn.commit()
    conn.close()
    print("✓ Datenbank erstellt")
 
def generate_unique_code():
    """Generiert einen eindeutigen, zufälligen Code aus Buchstaben und Zahlen"""
    code = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=2))
    return code
 
# ========================================
# 2. FLASK REST API
# ========================================
 
app = Flask(__name__)
 
def get_db():
    """Hilfsfunktion für Datenbankverbindung"""
    conn = sqlite3.connect('boxes.db')
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/api/boxes', methods=['POST'])
def create_box():
    data = request.get_json()
    code = data.get('CODE', generate_unique_code())
    location = data.get('Location', '')
    content = data.get('Content', '')
   
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO boxes (CODE, Location, Content) VALUES (?, ?, ?)', (code, location, content))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Kiste erstellt', 'CODE': code}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'CODE existiert bereits'}), 400
 
@app.route('/api/boxes', methods=['GET'])
def get_all_boxes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boxes')
    boxes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(boxes), 200
 
@app.route('/api/boxes/<code>', methods=['GET'])
def get_box(code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM boxes WHERE CODE = ?', (code,))
    box = cursor.fetchone()
    conn.close()
   
    if box:
        return jsonify(dict(box)), 200
    return jsonify({'error': 'Kiste nicht gefunden'}), 404
 
@app.route('/api/boxes/<code>', methods=['PUT'])
def update_box(code):
    data = request.get_json()
    location = data.get('Location')
    content = data.get('Content')
   
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE boxes SET Location = ?, Content = ? WHERE CODE = ?', (location, content, code))
    conn.commit()
   
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Kiste nicht gefunden'}), 404
   
    conn.close()
    return jsonify({'message': 'Kiste aktualisiert'}), 200
 
@app.route('/api/boxes/<code>', methods=['DELETE'])
def delete_box(code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM boxes WHERE CODE = ?', (code,))
    conn.commit()
   
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Kiste nicht gefunden'}), 404
   
    conn.close()
    return jsonify({'message': 'Kiste gelöscht'}), 200
 
# ========================================
# 3. SERVER STARTEN
# ========================================
 
def start_server():
    """Startet den Flask-Server in einem separaten Thread"""
    app.run(host='0.0.0.0', port=5006, debug=False, use_reloader=False)
 
init_database()
 
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
 
print("✓ Server läuft auf http://0.0.0.0:5006")
print("  Zugriff aus Netzwerk: http://<deine-ip>:5006")
 