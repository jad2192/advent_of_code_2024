import math


class MemoryGrid:
    def __init__(self, memory_fp: str, bytes: int, grid_max: int):
        self.corrupted_memory: dict[int : set[complex]] = {}
        self.bytes, self.grid_max = bytes, grid_max
        for k, byte in enumerate(open(memory_fp).read().split("\n")):
            z = complex(int(byte.split(",")[0]), int(byte.split(",")[1]))
            self.corrupted_memory[k + 1] = self.corrupted_memory.get(k, set()).union({z})
        max_range = range(grid_max + 1)
        self.dist: dict[complex, int] = {complex(r, i): math.inf for r in max_range for i in max_range}

    def _reset_dist(self):
        self.dist = {complex(r, i): math.inf for r in range(self.grid_max + 1) for i in range(self.grid_max + 1)}

    def _dijkstra(self, bytes: int | None = None) -> int | None:
        bytes = bytes or self.bytes
        queue = set(self.dist).difference(self.corrupted_memory[bytes])
        self.dist[0] = 0
        priority = sorted(list(queue), key=lambda w: self.dist[w])
        while queue:
            z = priority.pop(0)
            queue.remove(z)
            for dxn in {1, -1, 1j, -1j}:
                if z + dxn in queue:
                    new_dist = self.dist[z] + 1
                    if new_dist < self.dist[z + dxn]:
                        self.dist[z + dxn] = new_dist
                        priority.sort(key=lambda w: self.dist[w])

    def get_shortest_path(self):
        self._dijkstra()
        return self.dist[complex(self.grid_max, self.grid_max)]

    def get_blocker(self, start_byte: int):
        reachable = True
        bytes = start_byte
        self._reset_dist()
        while reachable and bytes <= max(self.corrupted_memory):
            self._dijkstra(bytes)
            if self.dist[complex(self.grid_max, self.grid_max)] < math.inf:
                bytes += 1
                self._reset_dist()
            else:
                reachable = False
        return list(self.corrupted_memory[bytes].difference(self.corrupted_memory[bytes - 1]))[0]


# Test
test_grid = MemoryGrid("inputs/day18/test.txt", 12, 6)
assert test_grid.get_shortest_path() == 22
assert test_grid.get_blocker(13) == 6 + 1j

# Main
grid = MemoryGrid("inputs/day18/main.txt", 1024, 70)
print(f"Part 1: {grid.get_shortest_path()}")
print(f"Part 2: {grid.get_blocker(2048)}")
