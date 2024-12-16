import math


class Maze:
    def __init__(self, maze_fp: str):
        self.grid: dict[complex, str] = {}
        self.start, self.end = 0, 0
        self.dist: dict[complex:int] = {}
        self.path: dict[complex:complex] = {}
        for imag, line in enumerate(open(maze_fp).read().split("\n")):
            for real, chr in enumerate(line):
                self.grid[complex(real, imag)] = chr
                if chr == "S":
                    self.start = complex(real, imag)
                if chr == "E":
                    self.end = complex(real, imag)
                if chr != "#":
                    self.dist[complex(real, imag)] = math.inf

    def _dijkstra(self) -> int | None:
        queue = set(self.dist)
        self.dist[self.start] = 0
        self.path[self.start] = 1 + 0j  # We always start by facing east
        priority = sorted(list(queue), key=lambda w: self.dist[w])
        while queue:
            z = priority.pop(0)
            cur_dxn = self.path[z]
            queue.remove(z)
            for dxn in {1, -1, 1j, -1j}:
                if self.grid.get(z + dxn, "#") != "#" and z + dxn in queue and (z == self.start or dxn != -cur_dxn):
                    dxn_ratio = cur_dxn / dxn
                    jump = 1 + 1000 * int(dxn_ratio.imag != 0) + 1000 * 1000 * int(dxn_ratio == -1)
                    new_dist = self.dist[z] + jump
                    if new_dist < self.dist[z + dxn]:
                        self.dist[z + dxn] = new_dist
                        self.path[z + dxn] = dxn
                        priority.sort(key=lambda w: self.dist[w])

    def get_best_score(self):
        self._dijkstra()
        return self.dist[self.end]


# Test
test_maze = Maze("inputs/day16/test.txt")
assert test_maze.get_best_score() == 7036

# Main
maze = Maze("inputs/day16/main.txt")
print(f"Day 1: {maze.get_best_score()}")
