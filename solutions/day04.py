from typing import Optional

DIRECTIONS = ["NN", "NE", "EE", "SE", "SS", "SW", "WW", "NW"]


def load_grid(docuemnt_path: str) -> list[str]:
    return open(docuemnt_path).read().split("\n")


def get_next_coord(
    cur_row: int,
    cur_col: int,
    num_rows: int,
    num_cols: int,
    direction: str,
) -> Optional[tuple[int, int]]:
    new_row, new_col = cur_row, cur_col
    if "N" in direction:
        new_row -= 1
    if "S" in direction:
        new_row += 1
    if "E" in direction:
        new_col += 1
    if "W" in direction:
        new_col -= 1
    if (0 <= new_row <= num_rows - 1) and (0 <= new_col <= num_cols - 1):
        return new_row, new_col
    return None


def find_all_xmas(grid: list[str]) -> list[tuple[int, int, int, int]]:
    num_rows, num_cols = len(grid), len(grid[0])
    subseq_dict = {"X": "M", "M": "A", "A": "S"}
    # Will track (row_start, col_start, row_end, col_end) of found XMAS strings
    start_end_coords = set()
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r][c] == "X":
                for dxn in DIRECTIONS:
                    cont = True
                    cur_letter, cur_r, cur_c = grid[r][c], r, c
                    while cont:
                        sub_coord = get_next_coord(cur_r, cur_c, num_rows, num_cols, dxn)
                        if sub_coord is not None:
                            sub_letter = grid[sub_coord[0]][sub_coord[1]]
                            if sub_letter != subseq_dict[cur_letter]:
                                cont = False
                            else:
                                cur_letter = sub_letter
                                cur_r, cur_c = sub_coord
                        else:
                            cont = False
                        if cont and cur_letter == "S":
                            start_end_coords.add((r, c, cur_r, cur_c))
                            cont = False
    return list(start_end_coords)


def find_all_cross_mas(grid) -> list[tuple[int, int]]:
    num_rows, num_cols = len(grid), len(grid[0])
    # Will track (row, col) of found X-MAS crossses
    a_coords = set()
    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            if grid[r][c] == "A":
                nw = grid[r - 1][c - 1]
                se = grid[r + 1][c + 1]
                ne = grid[r - 1][c + 1]
                sw = grid[r + 1][c - 1]
                if {ne, sw} == {nw, se} and {ne, sw} == {"M", "S"}:
                    a_coords.add((r, c))
    return list(a_coords)


# Test
test_grid = load_grid("inputs/day04/test.txt")
test_grid2 = load_grid("inputs/day04/test2.txt")
assert len(find_all_xmas(test_grid)) == 18
print(find_all_cross_mas(test_grid2))
assert len(find_all_cross_mas(test_grid2)) == 9

# Main
grid = load_grid("inputs/day04/main.txt")
print(f"Part 1: {len(find_all_xmas(grid))}")
print(f"Part 1: {len(find_all_cross_mas(grid))}")
