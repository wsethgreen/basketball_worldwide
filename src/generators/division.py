import random


class DivisionGenerator:
    _adjectives = [
        "Atlantic",
        "Central",
        "Coastal",
        "Frontier",
        "Heartland",
        "Lakes",
        "Metro",
        "Mountain",
        "Northern",
        "Pacific",
        "Plains",
        "Southern",
        "Southeast",
        "Southwest",
        "Western",
    ]
    _nouns = [
        "Division",
        "Group",
        "Conference",
        "Region",
    ]

    def generate_names(self, count: int) -> list[str]:
        if count <= 0:
            return []

        combos = [f"{adj} {noun}" for adj in self._adjectives for noun in self._nouns]
        random.shuffle(combos)
        if count <= len(combos):
            return combos[:count]

        names = combos[:]
        suffix = 1
        while len(names) < count:
            names.append(f"Division {suffix}")
            suffix += 1
        return names
