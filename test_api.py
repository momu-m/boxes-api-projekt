import unittest
import json
from app import app, db, Box

class BoxApiTestCase(unittest.TestCase):
    def setUp(self):
        """Wird vor jedem Test ausgeführt: Test-Konfiguration laden."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Nutzt Datenbank im RAM
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Wird nach jedem Test ausgeführt."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_and_get_box(self):
        """Testet POST und GET einer Kiste."""
        # 1. Erstellen
        payload = {"code": "T-100", "location": "Testraum", "content": "Testinhalt"}
        response = self.app.post('/boxes', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # 2. Abrufen
        response = self.app.get('/boxes/T-100')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['location'], "Testraum")
        # Testet HATEOAS Link
        self.assertIn('_links', data)

    def test_delete_box(self):
        """Testet das Löschen einer Kiste."""
        # Kiste anlegen
        with app.app_context():
            b = Box(code="D-1", location="Hier", content="Weg")
            db.session.add(b)
            db.session.commit()
            
        response = self.app.delete('/boxes/D-1')
        self.assertEqual(response.status_code, 200)
        
        # Prüfen ob weg
        response = self.app.get('/boxes/D-1')
        self.assertEqual(response.status_code, 404)

    def test_filter_boxes(self):
        """Testet die Filterung nach Location."""
        with app.app_context():
            db.session.add(Box(code="F-1", location="Keller", content="A"))
            db.session.add(Box(code="F-2", location="Dach", content="B"))
            db.session.add(Box(code="F-3", location="Keller", content="C"))
            db.session.commit()
            
        # Filtern nach 'Keller' -> Sollte 2 Ergebnisse liefern
        response = self.app.get('/boxes?location=Keller')
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['location'], "Keller")

    def test_stats_endpoint(self):
        """Testet den Statistik-Endpunkt."""
        with app.app_context():
            db.session.add(Box(code="S-1", location="Lager", content="X"))
            db.session.add(Box(code="S-2", location="Lager", content="Y"))
            db.session.commit()
            
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_boxes'], 2)
        self.assertEqual(data['locations']['Lager'], 2)

if __name__ == '__main__':
    unittest.main()
