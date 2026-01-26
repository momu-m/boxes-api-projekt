import requests
import json
import time

# Das ist die Adresse deines Servers (muss in einem anderen Fenster laufen!)
BASE_URL = "http://127.0.0.1:5006"

def zeige_ergebnis(schritt_name, response):
    print(f"\n--- {schritt_name} ---")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code >= 200 and response.status_code < 300:
        print("✅ ALLES OK!")
        try:
            # Zeige die Antwort vom Server schön formatiert an
            print("Antwort vom Server:")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        except:
            pass
    else:
        print("❌ FEHLER!")
        print(response.text)
    
    print("-" * 40)
    input("[Drücke ENTER für den nächsten Schritt...]")

def main():
    print("\n📦 MEIN TEST-ABLAUF 📦")
    print("Dieser Test spielt einmal alles durch: Erstellen, Ansehen, Ändern, Löschen.")
    
    # 1. Alle anzeigen
    response = requests.get(f"{BASE_URL}/boxes")
    zeige_ergebnis("1. Ich schaue, welche Kisten schon da sind", response)

    # 2. Neu erstellen
    neue_kiste = {
        "code": "TEST-01",
        "location": "Mein Schreibtisch",
        "content": "Kugelschreiber"
    }
    print(f"Ich sende jetzt diese Daten: {neue_kiste}")
    response = requests.post(f"{BASE_URL}/boxes", json=neue_kiste)
    zeige_ergebnis("2. Ich erstelle eine neue Kiste", response)

    # 3. Kiste ändern
    aenderung = {"location": "Im Mülleimer"}
    print(f"Ich ändere den Ort zu: {aenderung['location']}")
    response = requests.put(f"{BASE_URL}/boxes/TEST-01", json=aenderung)
    zeige_ergebnis("3. Ich ändere die Kiste", response)
    
    # 4. Kiste löschen
    response = requests.delete(f"{BASE_URL}/boxes/TEST-01")
    zeige_ergebnis("4. Ich lösche die Kiste wieder", response)

    # 5. NEU: Liste der Orte abrufen
    response = requests.get(f"{BASE_URL}/locations")
    zeige_ergebnis("5. (NEU) Ich zeige alle Orte an", response)

    # 6. NEU: Nur Codes abrufen
    response = requests.get(f"{BASE_URL}/boxes/codes")
    zeige_ergebnis("6. (NEU) Ich zeige nur die Codes an", response)

    # 7. NEU: Statistik prüfen
    response = requests.get(f"{BASE_URL}/stats")
    zeige_ergebnis("7. Statistik (mit Anzahl Orten)", response)

    print("\n🏁 TEST FERTIG! Alles hat funktioniert.")

if __name__ == "__main__":
    try:
        main()
    except:
        print("\n⚠️ FEHLER: Dein Server läuft nicht!")
        print("Starte ihn zuerst in einem anderen Fenster mit: python app.py")
