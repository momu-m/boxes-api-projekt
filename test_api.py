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

if __name__ == '__main__':
    unittest.main()
