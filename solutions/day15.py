class Warehouse:
    def __init__(self, warehouse_fp: str, expanded: bool = False):
        self.expanded = expanded
        grid_str, path_str = open(warehouse_fp).read().split("\n\n")
        self.walls: set[tuple[int, int]] = set()
        self.free_space: set[tuple[int, int]] = set()
        self.robot_loc: tuple[int, int] = (0, 0)
        split_grid = grid_str.split("\n")
        self.rows, self.cols = len(split_grid), (1 + expanded) * len(split_grid[0])
        for r, line in enumerate(split_grid):
            for c, chr in enumerate(line):
                if not expanded:
                    if chr == "#":
                        self.walls.add((r, c))
                    elif chr == "@":
                        self.robot_loc = (r, c)
                    elif chr == ".":
                        self.free_space.add((r, c))
                else:
                    self.boxes: dict[tuple[int, int], str] = {}
                    c *= 2
                    if chr == "#":
                        self.walls.update({(r, c), (r, c + 1)})
                    elif chr == "@":
                        self.free_space.add((r, c + 1))
                        self.robot_loc = (r, c)
                    elif chr == ".":
                        self.free_space.update({(r, c), (r, c + 1)})
                    else:
                        self.boxes[(r, c)] = "["
                        self.boxes[(r, c + 1)] = "]"
        self.robot_path = "".join(path_str.split("\n"))

    def _execute_robot_path_non_extended(self):
        for step in self.robot_path:
            cur_r, cur_c = tuple(self.robot_loc)
            match step:
                case "^":
                    coord_gen = ((r, cur_c) for r in range(cur_r, 0, -1))
                    dr, dc = -1, 0
                case "v":
                    coord_gen = ((r, cur_c) for r in range(cur_r + 1, self.rows))
                    dr, dc = 1, 0
                case ">":
                    coord_gen = ((cur_r, c) for c in range(cur_c + 1, self.cols))
                    dr, dc = 0, 1
                case "<":
                    coord_gen = ((cur_r, c) for c in range(cur_c, 0, -1))
                    dr, dc = 0, -1
            for r, c in coord_gen:
                if (r, c) in self.walls:
                    break
                elif (r, c) in self.free_space:
                    self.free_space.remove((r, c))
                    self.free_space.add((cur_r, cur_c))
                    self.robot_loc = (cur_r + dr, cur_c + dc)
                    break

    def _execute_robot_path_extended(self):
        for step in self.robot_path:
            cur_r, cur_c = tuple(self.robot_loc)
            if step in {"<", ">"}:
                if step == ">":
                    coord_gen = ((cur_r, c) for c in range(cur_c + 1, self.cols))
                    dc = 1
                if step == "<":
                    coord_gen = ((cur_r, c) for c in range(cur_c, 0, -1))
                    dc, -1
            for r, c in coord_gen:
                if (r, c) in self.walls:
                    break
                elif (r, c) in self.free_space:
                    self.free_space.remove((r, c))
                    self.free_space.add((cur_r, cur_c))
                    self.robot_loc = (cur_r, cur_c + dc)
                    break
            else:  # Vertically much harder, create a tree of boxes above.
                dr = -1 if step == "^" else 1
                if (cur_r + dr, cur_c) in self.walls:
                    pass
                elif (cur_r + dr, cur_c) in self.free_space:
                    self.robot_loc = (cur_r + dr, cur_c)
                    self.free_space.add((cur_r, cur_c))
                    self.free_space.remove((cur_r + dr, cur_c))
                else:  # DFS per usual
                    level = int(dr)
                    nodes_becoming_free = {(cur_r, cur_c)}
                    free_nodes_leaving = set()
                    node_stack = [(cur_r, cur_c)]  # track robot / left box edges
                    while node_stack:
                        if (cur_r + dr, cur_c) in self.box_left_edges:
                            pass

    def gps_sums(self) -> int:
        if not self.extended:
            self._execute_robot_path_non_extended()
            box_comp = self.free_space.union(self.walls).union({self.robot_loc})  # complement of set of box coords
            return sum(100 * r + c for r in range(self.rows) for c in range(self.cols) if (r, c) not in box_comp)
        else:
            self._execute_robot_path_extended()


# Test
test_warehouse = Warehouse("inputs/day15/test.txt")
test_warehouse2 = Warehouse("inputs/day15/test2.txt")
assert test_warehouse.gps_sums() == 10092
assert test_warehouse2.gps_sums() == 2028

# Main
warehouse = Warehouse("inputs/day15/main.txt")
print(f"Part 1: {warehouse.gps_sums()}")
