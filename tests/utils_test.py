from src.utils import capitalize, calculateAverage, slugify, clamp, sortStudents
#from src.utils import sortStudents

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

#-------

# Données de test réutilisables (Fixture manuelle)
def get_sample_students():
    return [
        {"name": "Zoe", "grade": 12, "age": 22},
        {"name": "Alice", "grade": 18, "age": 20},
        {"name": "Bob", "grade": 15, "age": 25}
    ]

# 1. should sort students by grade ascending
def test_should_sort_students_by_grade_ascending():
    students = get_sample_students()
    result = sortStudents(students, "grade", "asc")
    assert result[0]["name"] == "Zoe"   # 12
    assert result[1]["name"] == "Bob"   # 15
    assert result[2]["name"] == "Alice" # 18

# 2. should sort students by grade descending
def test_should_sort_students_by_grade_descending():
    students = get_sample_students()
    result = sortStudents(students, "grade", "desc")
    assert result[0]["name"] == "Alice" # 18
    assert result[1]["name"] == "Bob"   # 15
    assert result[2]["name"] == "Zoe"   # 12

# 3. should sort students by name ascending
def test_should_sort_students_by_name_ascending():
    students = get_sample_students()
    result = sortStudents(students, "name", "asc")
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    assert result[2]["name"] == "Zoe"

# 4. should sort students by age ascending
def test_should_sort_students_by_age_ascending():
    students = get_sample_students()
    result = sortStudents(students, "age", "asc")
    assert result[0]["name"] == "Alice" # 20
    assert result[1]["name"] == "Zoe"   # 22
    assert result[2]["name"] == "Bob"   # 25

# 5. should return empty array for null input
def test_should_return_empty_array_for_null_input():
    result = sortStudents(None, "grade")
    assert result == []

# 6. should return empty array for empty input
def test_should_return_empty_array_for_empty_input():
    result = sortStudents([], "grade")
    assert result == []

# 7. should not modify the original array
def test_should_not_modify_the_original_array():
    original = get_sample_students()
    # On fait une copie manuelle pour comparer plus tard
    snapshot = list(original) 
    
    result = sortStudents(original, "grade", "asc")
    
    # On vérifie que la liste retournée est un objet différent en mémoire
    assert result is not original
    # On vérifie que la liste originale n'a pas bougé
    assert original == snapshot

# 8. should default to ascending order
def test_should_default_to_ascending_order():
    students = get_sample_students()
    # On omet volontairement le 3ème paramètre
    result = sortStudents(students, sortBy="grade") 
    
    assert result[0]["name"] == "Zoe"   # 12 (ascendant par défaut)
    assert result[2]["name"] == "Alice" # 18