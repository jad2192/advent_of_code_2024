def load_antenna_grid_and_locations(document_path: str) -> tuple[list[str], dict[str, list[tuple[int, int]]]]:
    grid = open(document_path).read().split("\n")
    antenna_locations: dict[str, list[tuple[int, int]]] = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            cur_char = grid[r][c]
            match (cur_char, cur_char in antenna_locations):
                case (".", _):
                    pass
                case (_, True):
                    antenna_locations[cur_char].append((r, c))
                case (_, False):
                    antenna_locations[cur_char] = [(r, c)]
    return grid, antenna_locations


def get_anti_node_pairs_from_antennae(n1: tuple[int, int], n2: tuple[int, int]) -> list[tuple[int, int]]:
    rise = n2[0] - n1[0]
    run = n2[1] - n1[1]
    return [(n2[0] + rise, n2[1] + run), (n1[0] - rise, n1[1] - run)]


def get_all_anti_node_pairs(
    grid: list[str], antenna_locations: dict[str, list[tuple[int, int]]]
) -> set[tuple[int, int]]:
    anti_nodes: set[tuple[int, int]] = set()
    for nodes in antenna_locations.values():
        if len(nodes) < 2:
            continue
        else:
            for k, n1 in enumerate(nodes):
                for n2 in nodes[k + 1 :]:
                    anti_nodes.update(
                        n
                        for n in get_anti_node_pairs_from_antennae(n1, n2)
                        if (0 <= n[0] <= len(grid) - 1) and (0 <= n[1] <= len(grid[0]) - 1)
                    )
    return anti_nodes


class AffineEq:
    # AX + BY + C = 0
    def __init__(self, n1: tuple[int, int], n2: tuple[int, int]):
        self.A = n1[0] - n2[0]  # A is the negative of "rise"
        self.B = n2[1] - n1[1]  # B is the run
        self.C = -n1[1] * self.A - n1[0] * self.B  # C = -AX -BY for all X, Y on line

    def on_line(self, coord: tuple[int, int]) -> bool:
        # coord  = (row, column) = (y, x)
        return self.A * coord[1] + self.B * coord[0] + self.C == 0


def get_all_anti_nodes(grid: list[str], antenna_locations: dict[str, list[tuple[int, int]]]) -> list[tuple[int, int]]:
    equations: list[AffineEq] = []
    for nodes in antenna_locations.values():
        if len(nodes) < 2:
            continue
        else:
            for k, n1 in enumerate(nodes):
                for n2 in nodes[k + 1 :]:
                    equations.append(AffineEq(n1, n2))
    anti_nodes = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if any(eq.on_line((r, c)) for eq in equations):
                anti_nodes.append((r, c))
    return anti_nodes


# Test
test_grid, test_locations = load_antenna_grid_and_locations("inputs/day08/test.txt")
anti_node_pairs_test = get_all_anti_node_pairs(test_grid, test_locations)
anti_nodes_test = get_all_anti_nodes(test_grid, test_locations)
assert len(anti_node_pairs_test) == 14
assert len(anti_nodes_test) == 34

# Main
grid, locations = load_antenna_grid_and_locations("inputs/day08/main.txt")
anti_node_pairs = get_all_anti_node_pairs(grid, locations)
anti_nodes = get_all_anti_nodes(grid, locations)
print(f"Part 1: {len(anti_node_pairs)}")
print(f"Part 2: {len(anti_nodes)}")
