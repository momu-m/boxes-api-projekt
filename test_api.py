import unittest
import json
from app import app, db, Box

class BoxApiTestCase(unittest.TestCase):
    def setUp(self):
        """
        Vorbereitung vor JEDEM Test:
        Hier setzen wir die Datenbank zurück, damit jeder Test leer startet.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Test-Datenbank im Speicher (Memory)
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Aufräumen nach JEDEM Test.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_1_create_box(self):
        """Test 1: Kann ich eine neue Kiste erstellen?"""
        # Daten vorbereiten
        payload = {"code": "K-001", "location": "Keller", "content": "Bücher"}
        
        # POST-Request senden
        response = self.app.post('/boxes', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        # Prüfen ob Antwort Code 201 (Erstellt) ist
        self.assertEqual(response.status_code, 201)
        
        # Prüfen ob die Antwort die richtigen Daten enthält
        data = json.loads(response.data)
        self.assertEqual(data['code'], "K-001")
        self.assertEqual(data['location'], "Keller")

    def test_2_get_box(self):
        """Test 2: Kann ich eine Kiste abrufen?"""
        # Zuerst eine Kiste erstellen
        with app.app_context():
            neue_kiste = Box(code="K-002", location="Dachboden", content="Alte Kleidung")
            db.session.add(neue_kiste)
            db.session.commit()

        # GET-Request senden um die Kiste K-002 zu holen
        response = self.app.get('/boxes/K-002')
        
        # Prüfen ob Antwort 200 (OK) ist
        self.assertEqual(response.status_code, 200)
        
        # Inhalt prüfen
        data = json.loads(response.data)
        self.assertEqual(data['content'], "Alte Kleidung")

    def test_3_update_box(self):
        """Test 3: Kann ich eine Kiste ändern?"""
        # Kiste erstellen
        with app.app_context():
            db.session.add(Box(code="K-003", location="Büro", content="Papier"))
            db.session.commit()

        # Update-Request (PUT) senden: Standort ändern
        update_data = {"location": "Archiv"}
        response = self.app.put('/boxes/K-003',
                                data=json.dumps(update_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Prüfen ob Änderung übernommen wurde
        data = json.loads(response.data)
        self.assertEqual(data['location'], "Archiv") 

    def test_4_delete_box(self):
        """Test 4: Kann ich eine Kiste löschen?"""
        # Kiste erstellen
        with app.app_context():
            db.session.add(Box(code="K-004", location="Garage", content="Werkzeug"))
            db.session.commit()
            
        # DELETE-Request senden
        response = self.app.delete('/boxes/K-004')
        self.assertEqual(response.status_code, 200)
        
        # Prüfen ob sie wirklich weg ist (GET sollte 404 Fehler geben)
        check_response = self.app.get('/boxes/K-004')
        self.assertEqual(check_response.status_code, 404)

    def test_5_filter_boxes(self):
        """Test 5: Funktioniert der Filter beim Suchen?"""
        with app.app_context():
            db.session.add(Box(code="A-1", location="Keller", content="A"))
            db.session.add(Box(code="A-2", location="Dach", content="B"))
            db.session.add(Box(code="A-3", location="Keller", content="C"))
            db.session.commit()
            
        # Suche alle Kisten im 'Keller'
        response = self.app.get('/boxes?location=Keller')
        data = json.loads(response.data)
        
        # Es sollten genau 2 Kisten sein
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['location'], "Keller")

if __name__ == '__main__':
    unittest.main()
