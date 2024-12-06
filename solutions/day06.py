def load_grid_and_get_guard_start(document_path: str) -> tuple[dict[tuple[int, int], str], tuple[int, int, str]]:
    map_grid, gaurd_pos = {}, (0, 0, "^")
    for r, line in enumerate(open(document_path).read().split("\n")):
        for c, ch in enumerate(line):
            if ch in {"^", ">", "<", "v"}:
                gaurd_pos = (r, c, ch)
                ch = "."
            map_grid[(r, c)] = ch
    return map_grid, gaurd_pos


class Guard:
    def __init__(self, start_position: tuple[int, int, str]):
        self.position = start_position
        self.on_grid = True
        self.cycle = {"^": ">", ">": "v", "v": "<", "<": "^"}

    def walk(self, grid: dict[tuple[int, int], str]):
        r, c, dxn = self.position
        r_n = r + (dxn == "v") - (dxn == "^")
        c_n = c + (dxn == ">") - (dxn == "<")
        match grid.get((r_n, c_n), "off_grid"):
            case "off_grid":
                self.on_grid = False
                self.position = (r_n, c_n, dxn)
            case "#":
                self.position = (r, c, self.cycle[dxn])
            case ".":
                self.position = (r_n, c_n, dxn)


def get_guard_positions(guard: Guard, map_grid: dict[tuple[int, int], str]) -> set[tuple[int, int, str]]:
    visited_positions = set()
    while guard.on_grid and guard.position not in visited_positions:
        visited_positions.add(guard.position)
        guard.walk(map_grid)
    return visited_positions


def count_obstacle_positions(
    start_position: tuple[int, int, str],
    guard_positions: set[tuple[int, int, str]],
    map_grid: dict[tuple[int, int], str],
) -> int:
    obs_pos = set()
    for r, c, _ in guard_positions - {start_position}:
        obstacle_grid = dict(map_grid) | {(r, c): "#"}
        deflected_guard = Guard(start_position)
        get_guard_positions(deflected_guard, obstacle_grid)
        if deflected_guard.on_grid:
            obs_pos.add((r, c))
    return len(obs_pos)


# Test
test_grid, guard_start_test = load_grid_and_get_guard_start("inputs/day06/test.txt")
test_guard = Guard(guard_start_test)
test_guard_positions = get_guard_positions(test_guard, test_grid)
assert len(set((p[0], p[1]) for p in test_guard_positions)) == 41
assert count_obstacle_positions(guard_start_test, test_guard_positions, test_grid) == 6

# Main
grid, guard_start = load_grid_and_get_guard_start("inputs/day06/main.txt")
guard = Guard(guard_start)
guard_positions = get_guard_positions(guard, grid)
print(f"Part 1: {len(set((p[0], p[1]) for p in guard_positions))}")
print(f"Part 2: {count_obstacle_positions(guard_start, guard_positions, grid)}")