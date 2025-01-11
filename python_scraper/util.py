from pyproj import Transformer


LONDON_BOUNDARY_SW = (505000.0, 157000.0)
LONDON_BOUNDARY_NE = (555000.0, 182000.0)


def london_outward_codes() -> list[str]:
    outward_code_ranges = {
        "E": [
            x for x in range(1, 21) if x not in [19]
        ],  # E19 does not exist, E20 is olympic village
        "EC": range(1, 5),
        "N": range(1, 23),
        "NW": range(1, 12),
        "SE": range(1, 29),
        "SW": range(1, 11),
        "W": range(1, 15),
        "WC": range(1, 3),
    }
    return [
        f"{area}{num}"
        for area, numbers in outward_code_ranges.items()
        for num in numbers
    ]


def coordinates_to_bng(latitude: float, longitude: float) -> tuple[int, int]:
    t = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    return t.transform(longitude, latitude)
