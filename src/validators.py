import re
from typing import Any


def isValidEmail(email: str | None) -> bool:
    if not email:
        return False
    # Vérifie qu'il y a du texte, un @, du texte, un point, et du texte.
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def isValidPassword(password: str | None) -> dict[str, Any]:
    if password is None:
        password = ""

    errors = []

    if len(password) < 8:
        errors.append("Minimum 8 caracteres")
    if not any(c.isupper() for c in password):
        errors.append("Au moins 1 majuscule")
    if not any(c.islower() for c in password):
        errors.append("Au moins 1 minuscule")
    if not any(c.isdigit() for c in password):
        errors.append("Au moins 1 chiffre")
    if not any(c in "!@#$%^&*" for c in password):
        errors.append("Au moins 1 caractere special (!@#$%^&*)")

    return {"valid": len(errors) == 0, "errors": errors}


def isValidAge(age: Any) -> bool:
    if age is None:
        return False
    # En Python, les booléens sont une sous-classe des entiers. Il faut les exclure.
    if isinstance(age, bool):
        return False
    if not isinstance(age, int):
        return False

    return 0 <= age <= 150
