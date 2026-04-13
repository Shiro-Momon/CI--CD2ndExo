import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils import capitalize, slugify
from src.validators import isValidEmail, isValidPassword, isValidAge
from src.delivery import calculateOrderTotal, applyPromoCode

app = FastAPI(title="Mon API de Validation et Utilitaires")

# ─── Delivery ─────────────────────────────────────────────────────────────────

orders: dict = {}

PROMO_CODES = [
    {"code": "BIENVENUE20", "type": "percentage", "value": 20, "minOrder": 15.00, "expiresAt": "2026-12-31"},
    {"code": "FIXED5",      "type": "fixed",      "value": 5,  "minOrder": 10.00, "expiresAt": "2026-12-31"},
    {"code": "EXPIRED",     "type": "percentage", "value": 10, "minOrder": 0.00,  "expiresAt": "2020-01-01"},
]

class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int

class OrderRequest(BaseModel):
    items: list[OrderItem]
    distance: float
    weight: float
    promoCode: str | None = None
    hour: float
    dayOfWeek: int

class PromoValidateRequest(BaseModel):
    code: str
    amount: float

@app.post("/orders/simulate", status_code=200)
def simulate_order(req: OrderRequest):
    try:
        result = calculateOrderTotal(
            [i.model_dump() for i in req.items],
            req.distance, req.weight, req.promoCode,
            req.hour, req.dayOfWeek, PROMO_CODES
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders", status_code=201)
def create_order(req: OrderRequest):
    try:
        result = calculateOrderTotal(
            [i.model_dump() for i in req.items],
            req.distance, req.weight, req.promoCode,
            req.hour, req.dayOfWeek, PROMO_CODES
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    order_id = str(uuid.uuid4())
    order = {"id": order_id, **result}
    orders[order_id] = order
    return order

@app.get("/orders/{order_id}", status_code=200)
def get_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order

@app.post("/promo/validate", status_code=200)
def validate_promo(req: PromoValidateRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Code promo manquant")
    promo = next((p for p in PROMO_CODES if p["code"] == req.code), None)
    if promo is None:
        raise HTTPException(status_code=404, detail=f"Code promo inconnu : {req.code}")
    try:
        new_price = applyPromoCode(req.amount, req.code, PROMO_CODES)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "valid": True,
        "originalAmount": req.amount,
        "newAmount": new_price,
        "discount": round(req.amount - new_price, 2),
    }

# ─── Validators & Utils ───────────────────────────────────────────────────────

# Modèles de données pour les requêtes POST
class PasswordCheckRequest(BaseModel):
    password: str

class UserProfileRequest(BaseModel):
    email: str
    age: int

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FastAPI !"}

@app.get("/utils/capitalize")
def get_capitalize(text: str):
    return {"result": capitalize(text)}

@app.get("/utils/slugify")
def get_slugify(text: str):
    return {"result": slugify(text)}

@app.post("/validators/password")
def check_password(req: PasswordCheckRequest):
    result = isValidPassword(req.password)
    if not result["valid"]:
        raise HTTPException(status_code=400, detail=result["errors"])
    return {"status": "valide"}

@app.post("/validators/profile")
def validate_profile(req: UserProfileRequest):
    if not isValidEmail(req.email):
        raise HTTPException(status_code=400, detail="Email invalide")
    if not isValidAge(req.age):
        raise HTTPException(status_code=400, detail="Age invalide (doit être entre 0 et 150)")
    
    return {
        "message": "Profil valide",
        "data": {
            "email": req.email,
            "age": req.age,
            "slug": slugify(req.email.split('@')[0])
        }
    }