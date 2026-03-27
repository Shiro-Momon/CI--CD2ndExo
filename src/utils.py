import re


def capitalize(text: str | None) -> str:
    if not text:
        return ""
    return text.capitalize()


def calculateAverage(numbers: list[float | int] | None) -> float | int:
    if not numbers:
        return 0
    return round(sum(numbers) / len(numbers), 2)


def slugify(text: str | None) -> str:
    if not text:
        return ""

    # Passage en minuscules
    text = text.lower()
    # Suppression des caractères spéciaux (garde uniquement l'alphanumérique, les espaces et les tirets)
    text = re.sub(r"[^\w\s-]", "", text)
    # Remplacement des espaces (et éventuels tirets multiples) par un seul tiret
    text = re.sub(r"[-\s]+", "-", text)

    # Suppression des tirets aux extrémités
    return text.strip("-")


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))
