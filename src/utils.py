import re
from typing import Any


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

#def sortStudents(students: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
def sortStudents(students: list[dict[str, Any]] | None, 
        sortBy: str, 
        order: str = "asc"
    ) -> list[dict[str, Any]]:
    # Règle 5 et 6 : Si null ou vide, retourner []
    if not students:
        return []

    # Règle 7 : On crée une copie pour ne pas modifier l'original
    arr = list(students)
    n = len(arr)

    # Algorithme de tri à bulles
    for i in range(n):
        for j in range(0, n - i - 1):
            val1 = arr[j].get(sortBy, 0)
            val2 = arr[j + 1].get(sortBy, 0)

            # Déterminer si on doit échanger les éléments
            swap = False
            if order == "asc" and val1 > val2:
                swap = True
            elif order == "desc" and val1 < val2:
                swap = True

            if swap:
                # Échange (Swap)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr
#    return sorted(students, key=lambda student: student["name"])