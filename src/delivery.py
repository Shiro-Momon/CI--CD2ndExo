def calculateDeliveryFee(distance: float, weight: float) -> float | None:
    if distance < 0 or weight < 0:
        raise ValueError("Distance and weight must be non-negative")

    if distance > 10:
        return None  # Livraison refusée

    fee = 2.00  # Frais de base

    if distance > 3:
        fee += (distance - 3) * 0.50

    if weight > 5:
        fee += 1.50

    return round(fee, 2)


def applyPromoCode(subtotal: float, promoCode: str | None, promoCodes: list) -> float:
    from datetime import date

    if subtotal < 0:
        raise ValueError("Le sous-total ne peut pas être négatif")

    if not promoCode:
        return subtotal

    promo = next((p for p in promoCodes if p["code"] == promoCode), None)

    if promo is None:
        raise ValueError(f"Code promo inconnu : {promoCode}")

    if date.fromisoformat(promo["expiresAt"]) < date.today():
        raise ValueError(f"Code promo expiré : {promoCode}")

    if subtotal < promo["minOrder"]:
        raise ValueError(f"Commande minimum de {promo['minOrder']}€ requise pour ce code")

    if promo["type"] == "percentage":
        total = subtotal * (1 - promo["value"] / 100)
    else:  # fixed
        total = subtotal - promo["value"]

    return round(max(total, 0.0), 2)


def calculateSurge(hour: float, dayOfWeek: int) -> float:
    """
    Retourne le multiplicateur de surge pricing.
    dayOfWeek: 0=Lundi, 1=Mardi, 2=Mercredi, 3=Jeudi, 4=Vendredi, 5=Samedi, 6=Dimanche
    hour: heure en float (ex: 12.5 = 12h30)
    """
    # Fermé avant 10h ou à partir de 22h
    if hour < 10.0 or hour >= 22.0:
        return 0

    # Dimanche toute la journée
    if dayOfWeek == 6:
        return 1.2

    # Vendredi (4) et Samedi (5) soir : 19h-22h
    if dayOfWeek in (4, 5) and hour >= 19.0:
        return 1.8

    # Lundi-Jeudi (0-3)
    if dayOfWeek <= 3:
        # Dîner : 19h-22h
        if hour >= 19.0:
            return 1.5
        # Déjeuner : 12h-13h30
        if 12.0 <= hour < 13.5:
            return 1.3
        # Normal : 10h-11h30 (inclus) et 14h-18h
        if (10.0 <= hour <= 11.5) or (14.0 <= hour < 18.0):
            return 1.0

    # Vendredi (4) et Samedi (5) hors soir : même grille que lun-jeu
    if dayOfWeek in (4, 5):
        if 12.0 <= hour < 13.5:
            return 1.3
        if (10.0 <= hour <= 11.5) or (14.0 <= hour < 18.0):
            return 1.0

    # Hors créneau défini (ex: 11h30-12h, 13h30-14h, 18h-19h) → fermé
    return 0


def calculateOrderTotal(
    items: list,
    distance: float,
    weight: float,
    promoCode: str | None,
    hour: float,
    dayOfWeek: int,
    promoCodes: list,
) -> dict:
    if not items:
        raise ValueError("Le panier ne peut pas être vide")

    for item in items:
        if item["price"] < 0:
            raise ValueError(f"Le prix de '{item['name']}' ne peut pas être négatif")

    # 1. Sous-total
    subtotal = round(sum(item["price"] * item["quantity"] for item in items), 2)

    # 2. Code promo → discount
    discounted = applyPromoCode(subtotal, promoCode, promoCodes)
    discount = round(subtotal - discounted, 2)

    # 3. Frais de livraison
    fee = calculateDeliveryFee(distance, weight)
    if fee is None:
        raise ValueError(f"La distance de {distance} km dépasse la zone de livraison (max 10 km)")

    # 4. Surge
    surge = calculateSurge(hour, dayOfWeek)
    if surge == 0:
        raise ValueError("La livraison n'est pas disponible en dehors des heures d'ouverture")

    delivery_fee = round(fee * surge, 2)

    # 5. Total
    total = round(discounted + delivery_fee, 2)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "deliveryFee": delivery_fee,
        "surge": surge,
        "total": total,
    }
