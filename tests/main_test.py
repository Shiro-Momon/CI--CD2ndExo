from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_should_return_200_when_root_accessed():
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API FastAPI !"}

def test_should_return_slug_when_text_provided():
    # Act
    response = client.get("/utils/slugify?text=Hello World")
    # Assert
    assert response.status_code == 200
    assert response.json()["result"] == "hello-world"

def test_should_return_400_when_password_is_weak():
    # Arrange
    payload = {"password": "123"}
    # Act
    response = client.post("/validators/password", json=payload)
    # Assert
    assert response.status_code == 400
    
    # CORRECTION ICI : On parse la réponse en JSON, puis on accède à la clé "detail"
    response_data = response.json()
    assert "Minimum 8 caracteres" in response_data["detail"]

def test_should_return_200_when_profile_is_valid():
    # Arrange
    payload = {"email": "test@example.com", "age": 25}
    # Act
    response = client.post("/validators/profile", json=payload)
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Profil valide"