@staticmethod
def london_outward_codes() -> list[str]:
    outward_code_ranges = {
            "E": [x for x in range(1, 21) if x not in [19]],  # E19 does not exist, E20 is olympic village
            "EC": range(1, 5),
            "N": range(1, 23),
            "NW": range(1, 12),
            "SE": range(1, 29),
            "SW": range(1, 11),
            "W": range(1, 15),
            "WC": range(1, 3),
        }
    return [
        f"{area}{num}" for area, numbers in outward_code_ranges.items() for num in numbers
    ]
