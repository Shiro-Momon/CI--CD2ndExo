import pytest
from fastapi.testclient import TestClient
from src.main import app
from src import main as main_module

client = TestClient(app)

# ─── Fixture : reset des commandes avant chaque test ──────────────────────────

@pytest.fixture(autouse=True)
def reset_orders():
    main_module.orders.clear()
    yield
    main_module.orders.clear()

# ─── Helpers ──────────────────────────────────────────────────────────────────

VALID_PAYLOAD = {
    "items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
    "distance": 5,
    "weight": 1,
    "promoCode": None,
    "hour": 15.0,
    "dayOfWeek": 1,
}
# subtotal=25.00, deliveryFee=3.00, surge=1.0, discount=0, total=28.00

# ─── Tests existants ──────────────────────────────────────────────────────────

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

# ─── POST /orders/simulate ────────────────────────────────────────────────────

def test_simulate_should_return_200_with_correct_totals_for_normal_order():
    # Arrange - subtotal=25, fee=3.00, surge=1.0, total=28.00
    # Act
    response = client.post("/orders/simulate", json=VALID_PAYLOAD)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == 25.00
    assert data["deliveryFee"] == 3.00
    assert data["surge"] == 1.0
    assert data["discount"] == 0.00
    assert data["total"] == 28.00

def test_simulate_should_apply_promo_discount_when_valid_code_provided():
    # Arrange - BIENVENUE20: 20% sur 25€ → discount=5, total=25-5+3=23
    payload = {**VALID_PAYLOAD, "promoCode": "BIENVENUE20"}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["discount"] == 5.00
    assert data["total"] == 23.00

def test_simulate_should_return_400_when_promo_code_is_expired():
    # Arrange
    payload = {**VALID_PAYLOAD, "promoCode": "EXPIRED"}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 400

def test_simulate_should_return_400_when_items_list_is_empty():
    # Arrange
    payload = {**VALID_PAYLOAD, "items": []}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 400

def test_simulate_should_return_400_when_distance_out_of_zone():
    # Arrange
    payload = {**VALID_PAYLOAD, "distance": 15}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 400

def test_simulate_should_return_400_when_closed_hour():
    # Arrange
    payload = {**VALID_PAYLOAD, "hour": 23.0}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 400

def test_simulate_should_apply_surge_on_delivery_fee_when_friday_evening():
    # Arrange - vendredi 20h → surge=1.8, fee=3.00*1.8=5.40
    payload = {**VALID_PAYLOAD, "hour": 20.0, "dayOfWeek": 4}
    # Act
    response = client.post("/orders/simulate", json=payload)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["surge"] == 1.8
    assert data["deliveryFee"] == 5.40
    assert data["total"] == 30.40

# ─── POST /orders ─────────────────────────────────────────────────────────────

def test_create_order_should_return_201_with_id_when_valid():
    # Act
    response = client.post("/orders", json=VALID_PAYLOAD)
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["total"] == 28.00

def test_create_order_should_be_retrievable_via_get():
    # Arrange
    post_response = client.post("/orders", json=VALID_PAYLOAD)
    order_id = post_response.json()["id"]
    # Act
    get_response = client.get(f"/orders/{order_id}")
    # Assert
    assert get_response.status_code == 200
    assert get_response.json()["id"] == order_id

def test_create_order_two_orders_should_have_different_ids():
    # Act
    id1 = client.post("/orders", json=VALID_PAYLOAD).json()["id"]
    id2 = client.post("/orders", json=VALID_PAYLOAD).json()["id"]
    # Assert
    assert id1 != id2

def test_create_order_should_return_400_when_invalid():
    # Arrange
    payload = {**VALID_PAYLOAD, "hour": 23.0}
    # Act
    response = client.post("/orders", json=payload)
    # Assert
    assert response.status_code == 400

def test_create_order_should_not_store_order_when_invalid():
    # Arrange
    payload = {**VALID_PAYLOAD, "distance": 15}
    # Act
    client.post("/orders", json=payload)
    # Assert
    assert len(main_module.orders) == 0

# ─── GET /orders/:id ──────────────────────────────────────────────────────────

def test_get_order_should_return_200_when_id_exists():
    # Arrange
    order_id = client.post("/orders", json=VALID_PAYLOAD).json()["id"]
    # Act
    response = client.get(f"/orders/{order_id}")
    # Assert
    assert response.status_code == 200

def test_get_order_should_return_404_when_id_not_found():
    # Act
    response = client.get("/orders/nonexistent-id")
    # Assert
    assert response.status_code == 404

def test_get_order_should_return_correct_structure():
    # Arrange
    order_id = client.post("/orders", json=VALID_PAYLOAD).json()["id"]
    # Act
    response = client.get(f"/orders/{order_id}")
    # Assert
    data = response.json()
    assert set(data.keys()) == {"id", "subtotal", "discount", "deliveryFee", "surge", "total"}

# ─── POST /promo/validate ─────────────────────────────────────────────────────

def test_promo_validate_should_return_200_with_new_amount_when_valid():
    # Arrange - BIENVENUE20: 20% sur 50€ → newAmount=40, discount=10
    payload = {"code": "BIENVENUE20", "amount": 50.0}
    # Act
    response = client.post("/promo/validate", json=payload)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["newAmount"] == 40.0
    assert data["discount"] == 10.0

def test_promo_validate_should_return_400_when_code_is_expired():
    # Arrange
    payload = {"code": "EXPIRED", "amount": 50.0}
    # Act
    response = client.post("/promo/validate", json=payload)
    # Assert
    assert response.status_code == 400

def test_promo_validate_should_return_400_when_amount_below_minimum():
    # Arrange - FIXED5 exige minOrder=10, on envoie 5€
    payload = {"code": "FIXED5", "amount": 5.0}
    # Act
    response = client.post("/promo/validate", json=payload)
    # Assert
    assert response.status_code == 400

def test_promo_validate_should_return_404_when_code_unknown():
    # Arrange
    payload = {"code": "INEXISTANT", "amount": 50.0}
    # Act
    response = client.post("/promo/validate", json=payload)
    # Assert
    assert response.status_code == 404

def test_promo_validate_should_return_422_when_code_missing_from_body():
    # Arrange - champ obligatoire absent → erreur de validation Pydantic
    payload = {"amount": 50.0}
    # Act
    response = client.post("/promo/validate", json=payload)
    # Assert
    assert response.status_code == 422
