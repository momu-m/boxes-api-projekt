import pytest
import requests

# Basis-URL deiner lokalen API
BASE_URL = "http://127.0.0.1:5006"

# Endpunkt für die Kisten
ENDPOINT = "boxes"

# Ein Test-Item (eine Kiste)
# WICHTIG: Code darf maximal 4 Zeichen lang sein!
ITEM = {"code": "T-01", "location": "Testlabor", "content": "Wichtige Proben"}

@pytest.fixture(scope="session")
def base_url():
    """Fixture to provide base URL"""
    return BASE_URL

@pytest.fixture(scope="session")
def items_endpoint(base_url):
    return f"{base_url}/{ENDPOINT}"

@pytest.fixture
def created_item_location(items_endpoint):
    """Fixture to create a test item and clean it up after test"""
    # Create Item
    response = requests.post(items_endpoint, json=ITEM)
    
    # In deinem Beispiel nutzt der Dozent den 'Location'-Header.
    # Da deine API REST-konform ist (wenn wir Location Header senden),
    # nutzen wir den Code aus der Antwort, um den Pfad zu bauen, oder den Header, wenn vorhanden.
    # Um sicher zu sein bei DEINER Api: Wir basteln den Pfad aus dem Code.
    
    # WICHTIG: Deine API gibt JSON zurück. Wir nehmen den Code daraus.
    try:
        data = response.json()
        code = data.get("code")
        location = f"/boxes/{code}"
    except:
         # Fallback falls Header genutzt würde (aber deine APi schickt JSON Body)
        location = f"/boxes/{ITEM['code']}"

    yield location  # Provide location path (e.g. /boxes/TEST-FYI) to test

    # Teardown: Delete the item
    try:
        requests.delete(f"{BASE_URL}{location}")
    except:
        pass


class TestItemsAPI:

    def test_create_item(self, items_endpoint, base_url):
        """Test POST - Create new item"""
        # Wir brauchen einen neuen Code für diesen speziellen Test, damit er nicht kollidiert
        test_item = ITEM.copy()
        test_item["code"] = "T-02"
        
        response = requests.post(items_endpoint, json=test_item)
        
        # REST Best Practice: Status 201 Created
        assert response.status_code == 201

        # Check if we got JSON back with the right content
        data = response.json()
        assert data["code"] == test_item["code"]
        assert data["location"] == test_item["location"]

        # Cleanup (Wichtig!)
        requests.delete(f"{base_url}/boxes/{test_item['code']}")

    def test_get_all_items(self, items_endpoint, created_item_location):
        """Test GET all items"""
        response = requests.get(items_endpoint)
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data, list)

        # Prüfen ob unser Test-Item in der Liste ist
        assert any(
            i["code"] == ITEM["code"] 
            for i in response_data
        )

    def test_get_specific_item(self, base_url, created_item_location):
        """Test GET specific item"""
        # created_item_location ist z.B. /boxes/TEST-FYI
        full_url = f"{base_url}{created_item_location}"
        response = requests.get(full_url)

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == ITEM["code"]
        assert "content" in data

    def test_update_item(self, base_url, created_item_location):
        """Test PUT - Update item"""
        new_location = "Neues Lager"
        new_content = "Geheim"

        updated_data = {"location": new_location, "content": new_content}
        
        # Update senden
        response = requests.put(f"{base_url}{created_item_location}", json=updated_data)
        assert response.status_code == 200

        # Verify (Prüfen ob es wirklich geändert wurde)
        get_response = requests.get(f"{base_url}{created_item_location}")
        server_data = get_response.json()

        assert server_data["location"] == new_location
        assert server_data["content"] == new_content

    def test_delete_item(self, base_url, created_item_location):
        """Test DELETE item"""
        # Wir löschen das Item, das durch die Fixture erstellt wurde
        # (Achtung: Die Fixture versucht am Ende nochmal zu löschen, das ist okay)
        
        response = requests.delete(f"{base_url}{created_item_location}")
        assert response.status_code == 200

        # Verify item is deleted (Sollte 404 sein)
        get_response = requests.get(f"{base_url}{created_item_location}")
        assert get_response.status_code == 404
