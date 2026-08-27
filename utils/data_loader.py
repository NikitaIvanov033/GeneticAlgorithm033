from typing import List, Tuple


def load_tsp_data(filename: str) -> List[Tuple[float, float]]:
    coords = []

    with open(filename, 'r') as f:
        in_section = False

        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("NODE_COORD_SECTION"):
                in_section = True
                continue

            if line.startswith("EOF"):
                break

            if in_section:
                parts = line.split()
                if len(parts) >= 3:
                    _, x, y = parts[0], float(parts[1]), float(parts[2])
                    coords.append((x, y))

    return coords