from src.validators import isValidEmail, isValidPassword, isValidAge

# ==========================================
# Tests pour la fonction isValidEmail
# ==========================================


def test_should_return_true_when_standard_email_provided():
    # Arrange
    email = "user@example.com"
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is True


def test_should_return_true_when_complex_email_provided():
    # Arrange
    email = "user.name+tag@domain.co"
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is True


def test_should_return_false_when_invalid_string_provided():
    # Arrange
    email = "invalid"
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is False


def test_should_return_false_when_local_part_missing():
    # Arrange
    email = "@domain.com"
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is False


def test_should_return_false_when_domain_part_missing():
    # Arrange
    email = "user@"
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is False


def test_should_return_false_when_empty_email_provided():
    # Arrange
    email = ""
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is False


def test_should_return_false_when_null_email_provided():
    # Arrange
    email = None
    # Act
    result = isValidEmail(email)
    # Assert
    assert result is False


# ==========================================
# Tests pour la fonction isValidPassword
# ==========================================


def test_should_return_valid_when_perfect_password_provided():
    # Arrange
    password = "Passw0rd!"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_should_return_invalid_and_multiple_errors_when_short_password_provided():
    # Arrange
    password = "short"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert "Minimum 8 caracteres" in result["errors"]
    assert "Au moins 1 majuscule" in result["errors"]
    assert "Au moins 1 chiffre" in result["errors"]
    assert "Au moins 1 caractere special (!@#$%^&*)" in result["errors"]


def test_should_return_invalid_when_uppercase_missing():
    # Arrange
    password = "alllowercase1!"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 majuscule" in result["errors"]
    assert len(result["errors"]) == 1


def test_should_return_invalid_when_lowercase_missing():
    # Arrange
    password = "ALLUPPERCASE1!"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 minuscule" in result["errors"]
    assert len(result["errors"]) == 1


def test_should_return_invalid_when_digit_missing():
    # Arrange
    password = "NoDigits!here"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 chiffre" in result["errors"]
    assert len(result["errors"]) == 1


def test_should_return_invalid_when_special_char_missing():
    # Arrange
    password = "NoSpecial1here"
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert "Au moins 1 caractere special (!@#$%^&*)" in result["errors"]
    assert len(result["errors"]) == 1


def test_should_return_invalid_and_all_errors_when_empty_password_provided():
    # Arrange
    password = ""
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert len(result["errors"]) == 5


def test_should_return_invalid_and_all_errors_when_null_password_provided():
    # Arrange
    password = None
    # Act
    result = isValidPassword(password)
    # Assert
    assert result["valid"] is False
    assert len(result["errors"]) == 5


# ==========================================
# Tests pour la fonction isValidAge
# ==========================================


def test_should_return_true_when_normal_age_provided():
    # Arrange
    age = 25
    # Act
    result = isValidAge(age)
    # Assert
    assert result is True


def test_should_return_true_when_minimum_age_provided():
    # Arrange
    age = 0
    # Act
    result = isValidAge(age)
    # Assert
    assert result is True


def test_should_return_true_when_maximum_age_provided():
    # Arrange
    age = 150
    # Act
    result = isValidAge(age)
    # Assert
    assert result is True


def test_should_return_false_when_negative_age_provided():
    # Arrange
    age = -1
    # Act
    result = isValidAge(age)
    # Assert
    assert result is False


def test_should_return_false_when_age_above_maximum_provided():
    # Arrange
    age = 151
    # Act
    result = isValidAge(age)
    # Assert
    assert result is False


def test_should_return_false_when_float_age_provided():
    # Arrange
    age = 25.5
    # Act
    result = isValidAge(age)
    # Assert
    assert result is False


def test_should_return_false_when_string_age_provided():
    # Arrange
    age = "25"
    # Act
    result = isValidAge(age)
    # Assert
    assert result is False


def test_should_return_false_when_null_age_provided():
    # Arrange
    age = None
    # Act
    result = isValidAge(age)
    # Assert
    assert result is False
