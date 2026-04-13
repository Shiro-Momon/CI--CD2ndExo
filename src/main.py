from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
from src.utils import capitalize, calculateAverage, slugify, clamp
from src.validators import isValidEmail, isValidPassword, isValidAge

app = FastAPI(title="Mon API de Validation et Utilitaires")

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