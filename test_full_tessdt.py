import unittest
import requests
import time
import threading
import sys
import string

# Wir importieren das Skript des Users. 
# Achtung: Da tessdt.py den Server beim Import sofort startet (Zeile 126), 
# läuft der Server dann bereits im Hintergrund!
try:
    import tessdt
except ImportError:
    # Falls das Skript anders heißt oder nicht gefunden wird
    pass

BASE_URL = "http://127.0.0.1:5006/api/boxes"

class TestBoxApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Wird EINMAL vor allen Tests ausgeführt.
        Wir warten kurz, bis der Server aus 'tessdt.py' sicher läuft.
        """
        print("\n--- Start der Test-Suite ---\n")
        time.sleep(2) # Warten bis Server Thread bereit ist

    # ==========================
    # 1. UNIT TEST (Isolierter Test einer Funktion)
    # ==========================
    def test_unit_generate_unique_code(self):
        """
        UNIT TEST: Testet die Funktion 'generate_unique_code' isoliert.
        Prüft, ob der Code das richtige Format hat (2 Buchstaben, 2 Zahlen).
        """
        code = tessdt.generate_unique_code()
        print(f"[Unit-Test] Generierter Code: {code}")
        
        self.assertEqual(len(code), 4)
        self.assertTrue(code[0] in string.ascii_uppercase)
        self.assertTrue(code[1] in string.ascii_uppercase)
        self.assertTrue(code[2] in string.digits)
        self.assertTrue(code[3] in string.digits)

    # ==========================
    # 2. INTEGRATION / E2E TEST (Testet API + Datenbank + Server)
    # ==========================
    def test_integration_create_and_get_box(self):
        """
        INTEGRATION TEST: Erstellt eine Kiste via API und holt sie wieder.
        Testet das Zusammenspiel von Flask Route -> Datenbank -> Rückgabe.
        """
        # 1. Erstellen
        new_box = {
            "CODE": "XX99", 
            "Location": "Testlabor", 
            "Content": "Test-Objekt"
        }
        response = requests.post(BASE_URL, json=new_box)
        
        # Erwartung: Status 201 (Created)
        self.assertEqual(response.status_code, 201)
        print(f"[Int-Test] Kiste erstellt: {response.json()}")

        # 2. Abrufen (Prüfen ob wirklich in DB gespeichert)
        response = requests.get(f"{BASE_URL}/XX99")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['Location'], "Testlabor")
        self.assertEqual(data['Content'], "Test-Objekt")
        print(f"[Int-Test] Kiste abgerufen: {data}")

        # Aufräumen (Löschen)
        requests.delete(f"{BASE_URL}/XX99")

    def test_e2e_full_workflow(self):
        """
        E2E (End-to-End) TEST: Simuliert einen kompletten User-Ablauf.
        Erstellen -> Ändern -> Prüfen -> Löschen.
        """
        # A. User erstellt Kiste
        code = tessdt.generate_unique_code()
        box_data = {"CODE": code, "Location": "Regal 1", "Content": "Bücher"}
        requests.post(BASE_URL, json=box_data)
        
        # B. User ändert den Ort (Kiste wird umgeräumt)
        update_data = {"Location": "Regal 2", "Content": "Bücher"}
        requests.put(f"{BASE_URL}/{code}", json=update_data)
        
        # C. User prüft, ob Änderung geklappt hat
        resp = requests.get(f"{BASE_URL}/{code}")
        self.assertEqual(resp.json()['Location'], "Regal 2")
        
        # D. User löscht die Kiste
        requests.delete(f"{BASE_URL}/{code}")
        
        # E. User versucht sie nochmal zu finden (Sollte weg sein)
        resp = requests.get(f"{BASE_URL}/{code}")
        self.assertEqual(resp.status_code, 404)
        print(f"[E2E-Test] Kompletter Ablauf für {code} erfolgreich durchlaufen.")

if __name__ == '__main__':
    unittest.main()
