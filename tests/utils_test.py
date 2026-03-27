from src.utils import capitalize, calculateAverage, slugify, clamp

# ==========================================
# Tests pour la fonction capitalize
# ==========================================


def test_should_return_capitalized_when_lowercase_provided():
    # Arrange
    input_text = "hello"
    expected = "Hello"
    # Act
    result = capitalize(input_text)
    # Assert
    assert result == expected


def test_should_return_capitalized_when_uppercase_provided():
    # Arrange
    input_text = "WORLD"
    expected = "World"
    # Act
    result = capitalize(input_text)
    # Assert
    assert result == expected


def test_should_return_empty_string_when_empty_string_provided():
    # Arrange
    input_text = ""
    expected = ""
    # Act
    result = capitalize(input_text)
    # Assert
    assert result == expected


def test_should_return_empty_string_when_none_provided():
    # Arrange
    input_text = None
    expected = ""
    # Act
    result = capitalize(input_text)
    # Assert
    assert result == expected


# ==========================================
# Tests pour la fonction calculateAverage
# ==========================================


def test_should_return_average_when_multiple_numbers_provided():
    # Arrange
    numbers = [10, 12, 14]
    expected = 12
    # Act
    result = calculateAverage(numbers)
    # Assert
    assert result == expected


def test_should_return_single_value_when_one_number_provided():
    # Arrange
    numbers = [15]
    expected = 15
    # Act
    result = calculateAverage(numbers)
    # Assert
    assert result == expected


def test_should_return_zero_when_empty_list_provided():
    # Arrange
    numbers = []
    expected = 0
    # Act
    result = calculateAverage(numbers)
    # Assert
    assert result == expected


def test_should_return_zero_when_none_provided():
    # Arrange
    numbers = None
    expected = 0
    # Act
    result = calculateAverage(numbers)
    # Assert
    assert result == expected


def test_should_return_rounded_average_when_decimals_present():
    # Arrange (10+11+12 = 33 / 3 = 11.0, mais testons avec un cas qui génère beaucoup de décimales)
    # Ex: 10 + 11 + 13 = 34 / 3 = 11.333333...
    numbers = [10, 11, 13]
    expected = 11.33
    # Act
    result = calculateAverage(numbers)
    # Assert
    assert result == expected


# ==========================================
# Tests pour la fonction slugify
# ==========================================


def test_should_return_slug_when_normal_string_provided():
    # Arrange
    text = "Hello World"
    expected = "hello-world"
    # Act
    result = slugify(text)
    # Assert
    assert result == expected


def test_should_return_stripped_slug_when_spaces_everywhere_provided():
    # Arrange
    text = " Spaces Everywhere "
    expected = "spaces-everywhere"
    # Act
    result = slugify(text)
    # Assert
    assert result == expected


def test_should_return_clean_slug_when_special_chars_provided():
    # Arrange
    text = "C'est l'ete !"
    expected = "cest-lete"
    # Act
    result = slugify(text)
    # Assert
    assert result == expected


def test_should_return_empty_string_when_empty_slug_input_provided():
    # Arrange
    text = ""
    expected = ""
    # Act
    result = slugify(text)
    # Assert
    assert result == expected


def test_should_return_empty_string_when_none_slug_input_provided():
    # Arrange
    text = None
    expected = ""
    # Act
    result = slugify(text)
    # Assert
    assert result == expected


# ==========================================
# Tests pour la fonction clamp
# ==========================================


def test_should_return_value_when_value_is_within_bounds():
    # Arrange
    value, min_val, max_val = 5, 0, 10
    expected = 5
    # Act
    result = clamp(value, min_val, max_val)
    # Assert
    assert result == expected


def test_should_return_min_when_value_is_below_min():
    # Arrange
    value, min_val, max_val = -5, 0, 10
    expected = 0
    # Act
    result = clamp(value, min_val, max_val)
    # Assert
    assert result == expected


def test_should_return_max_when_value_is_above_max():
    # Arrange
    value, min_val, max_val = 15, 0, 10
    expected = 10
    # Act
    result = clamp(value, min_val, max_val)
    # Assert
    assert result == expected


def test_should_return_zero_when_all_args_are_zero():
    # Arrange
    value, min_val, max_val = 0, 0, 0
    expected = 0
    # Act
    result = clamp(value, min_val, max_val)
    # Assert
    assert result == expected
