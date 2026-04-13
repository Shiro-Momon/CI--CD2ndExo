import pytest
from src.delivery import calculateDeliveryFee, applyPromoCode, calculateSurge

# --- Happy paths ---

def test_should_return_base_fee_when_distance_zero_and_weight_zero():
    # Arrange
    distance = 0
    weight = 0
    expected = 2.00
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

def test_should_return_base_fee_when_distance_exactly_3km():
    # Arrange
    distance = 3
    weight = 0
    expected = 2.00
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

def test_should_return_extra_fee_when_distance_between_3_and_10km():
    # Arrange
    distance = 5        # 3 km free + 2 km * 0.50 = 1.00 extra
    weight = 0
    expected = 3.00     # 2.00 + 1.00
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

def test_should_return_max_fee_when_distance_exactly_10km():
    # Arrange
    distance = 10       # 7 km * 0.50 = 3.50 extra
    weight = 0
    expected = 5.50     # 2.00 + 3.50
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

def test_should_return_none_when_distance_exceeds_10km():
    # Arrange
    distance = 11
    weight = 0
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result is None

def test_should_add_weight_supplement_when_weight_exceeds_5kg():
    # Arrange
    distance = 2
    weight = 6          # > 5 kg → +1.50
    expected = 3.50     # 2.00 + 1.50
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

def test_should_combine_distance_and_weight_fees():
    # Arrange
    distance = 5        # +1.00
    weight = 6          # +1.50
    expected = 4.50     # 2.00 + 1.00 + 1.50
    # Act
    result = calculateDeliveryFee(distance, weight)
    # Assert
    assert result == expected

# --- Error cases ---

def test_should_raise_error_when_distance_is_negative():
    # Arrange
    distance = -1
    weight = 0
    # Act & Assert
    with pytest.raises(ValueError):
        calculateDeliveryFee(distance, weight)

def test_should_raise_error_when_weight_is_negative():
    # Arrange
    distance = 2
    weight = -1
    # Act & Assert
    with pytest.raises(ValueError):
        calculateDeliveryFee(distance, weight)


# ─── applyPromoCode ────────────────────────────────────────────────────────────

PROMO_CODES = [
    {"code": "BIENVENUE20", "type": "percentage", "value": 20, "minOrder": 15.00, "expiresAt": "2026-12-31"},
    {"code": "FIXED5",      "type": "fixed",      "value": 5,  "minOrder": 10.00, "expiresAt": "2026-12-31"},
    {"code": "EXPIRED",     "type": "percentage", "value": 10, "minOrder": 0.00,  "expiresAt": "2020-01-01"},
    {"code": "HIGHMIN",     "type": "fixed",      "value": 3,  "minOrder": 100.00,"expiresAt": "2026-12-31"},
    {"code": "FULL100",     "type": "percentage", "value": 100,"minOrder": 0.00,  "expiresAt": "2026-12-31"},
    {"code": "BIGFIXED",    "type": "fixed",      "value": 10, "minOrder": 0.00,  "expiresAt": "2026-12-31"},
    {"code": "TODAY",       "type": "fixed",      "value": 1,  "minOrder": 0.00,  "expiresAt": "2026-04-13"},
]

# --- Cas normaux ---

def test_should_apply_percentage_discount_when_valid_code_provided():
    # Arrange
    subtotal = 50.00
    expected = 40.00  # 20% de 50€
    # Act
    result = applyPromoCode(subtotal, "BIENVENUE20", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_apply_fixed_discount_when_valid_code_provided():
    # Arrange
    subtotal = 30.00
    expected = 25.00  # 30 - 5
    # Act
    result = applyPromoCode(subtotal, "FIXED5", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_apply_discount_when_minorder_exactly_met():
    # Arrange
    subtotal = 10.00  # exactement le minOrder de FIXED5
    expected = 5.00
    # Act
    result = applyPromoCode(subtotal, "FIXED5", PROMO_CODES)
    # Assert
    assert result == expected

# --- Refus du code ---

def test_should_refuse_code_when_expired():
    # Arrange
    subtotal = 50.00
    # Act & Assert
    with pytest.raises(ValueError):
        applyPromoCode(subtotal, "EXPIRED", PROMO_CODES)

def test_should_refuse_code_when_subtotal_below_minorder():
    # Arrange
    subtotal = 5.00  # < minOrder 10.00 de FIXED5
    # Act & Assert
    with pytest.raises(ValueError):
        applyPromoCode(subtotal, "FIXED5", PROMO_CODES)

def test_should_raise_error_when_code_unknown():
    # Arrange
    subtotal = 50.00
    # Act & Assert
    with pytest.raises(ValueError):
        applyPromoCode(subtotal, "INEXISTANT", PROMO_CODES)

# --- Cas limites dangereux ---

def test_should_not_return_negative_total_when_fixed_discount_exceeds_subtotal():
    # Arrange
    subtotal = 5.00   # BIGFIXED retire 10€ → ne doit pas descendre sous 0
    expected = 0.00
    # Act
    result = applyPromoCode(subtotal, "BIGFIXED", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_return_zero_when_percentage_is_100():
    # Arrange
    subtotal = 30.00
    expected = 0.00
    # Act
    result = applyPromoCode(subtotal, "FULL100", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_return_zero_when_subtotal_is_zero_and_no_minorder():
    # Arrange
    subtotal = 0.00
    expected = 0.00
    # Act
    result = applyPromoCode(subtotal, "FULL100", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_accept_code_expiring_today():
    # Arrange
    subtotal = 10.00
    expected = 9.00  # TODAY: fixed -1€
    # Act
    result = applyPromoCode(subtotal, "TODAY", PROMO_CODES)
    # Assert
    assert result == expected

# --- Entrées invalides ---

def test_should_return_subtotal_unchanged_when_promo_code_is_none():
    # Arrange
    subtotal = 30.00
    expected = 30.00
    # Act
    result = applyPromoCode(subtotal, None, PROMO_CODES)
    # Assert
    assert result == expected

def test_should_return_subtotal_unchanged_when_promo_code_is_empty_string():
    # Arrange
    subtotal = 30.00
    expected = 30.00
    # Act
    result = applyPromoCode(subtotal, "", PROMO_CODES)
    # Assert
    assert result == expected

def test_should_raise_error_when_subtotal_is_negative():
    # Arrange
    subtotal = -5.00
    # Act & Assert
    with pytest.raises(ValueError):
        applyPromoCode(subtotal, "BIENVENUE20", PROMO_CODES)


# ─── calculateSurge ────────────────────────────────────────────────────────────
# dayOfWeek: 0=Lundi, 1=Mardi, ..., 4=Jeudi, 5=Vendredi, 6=Samedi, 7=Dimanche
# hour: float (ex: 12.5 = 12h30)

# --- Chaque multiplicateur ---

def test_should_return_normal_rate_when_tuesday_afternoon():
    # Arrange - Mardi 15h → créneau normal 14h-18h
    # Act
    result = calculateSurge(15.0, 1)
    # Assert
    assert result == 1.0

def test_should_return_lunch_rate_when_wednesday_midday():
    # Arrange - Mercredi 12h30 → déjeuner
    # Act
    result = calculateSurge(12.5, 2)
    # Assert
    assert result == 1.3

def test_should_return_dinner_rate_when_thursday_evening():
    # Arrange - Jeudi 20h → dîner semaine
    # Act
    result = calculateSurge(20.0, 3)
    # Assert
    assert result == 1.5

def test_should_return_weekend_evening_rate_when_friday_night():
    # Arrange - Vendredi 21h → vendredi-samedi soir
    # Act
    result = calculateSurge(21.0, 4)
    # Assert
    assert result == 1.8

def test_should_return_sunday_rate_when_sunday_afternoon():
    # Arrange - Dimanche 14h
    # Act
    result = calculateSurge(14.0, 6)
    # Assert
    assert result == 1.2

def test_should_return_weekend_evening_rate_when_saturday_night():
    # Arrange - Samedi 20h → vendredi-samedi soir
    # Act
    result = calculateSurge(20.0, 5)
    # Assert
    assert result == 1.8

# --- Transitions et limites ---

def test_should_return_normal_rate_when_hour_is_exactly_11h30():
    # Arrange - 11h30 pile → encore dans le créneau normal (déjeuner commence à 12h)
    # Act
    result = calculateSurge(11.5, 1)
    # Assert
    assert result == 1.0

def test_should_return_dinner_rate_when_hour_is_exactly_19h():
    # Arrange - 19h00 pile → début créneau dîner
    # Act
    result = calculateSurge(19.0, 2)
    # Assert
    assert result == 1.5

def test_should_return_closed_when_hour_is_exactly_22h():
    # Arrange - 22h00 pile → fermé
    # Act
    result = calculateSurge(22.0, 1)
    # Assert
    assert result == 0

def test_should_return_closed_when_hour_is_before_10h():
    # Arrange - 9h59 → fermé
    # Act
    result = calculateSurge(9.99, 1)
    # Assert
    assert result == 0

def test_should_return_normal_rate_when_hour_is_exactly_10h():
    # Arrange - 10h00 pile → ouvert, créneau normal
    # Act
    result = calculateSurge(10.0, 1)
    # Assert
    assert result == 1.0
