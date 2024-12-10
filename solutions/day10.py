class TopoMap:
    def __init__(self, map_fp: str):
        self.grid: dict[tuple[int, int], int] = {}
        self.peaks: dict[tuple[int, int], set[tuple[int, int]]] = {}
        self.trails: dict[tuple[int, int], int] = {}
        self.trail_heads: list[tuple[int, int]] = []
        for r, line in enumerate(open(map_fp).read().split("\n")):
            for c, chr in enumerate(line):
                self.grid[(r, c)] = int(chr)
                if chr == "0":
                    self.trail_heads.append((r, c))

    def get_neighbors(self, coord: tuple[int, int]) -> list[tuple[int, int]]:
        return [
            (r, c)
            for (r, c) in [(coord[0] + d[0], coord[1] + d[1]) for d in {(1, 0), (-1, 0), (0, 1), (0, -1)}]
            if self.grid.get((r, c), -1) - 1 == self.grid.get(coord, -10)
        ]

    def _get_peaks_and_trails_dfs(self, start_coord: tuple[int, int]) -> tuple[set[tuple[int, int]], int]:
        # Peaks and trails update concurrently so empty iff other is empty
        match (bool(self.peaks.get(start_coord, set())), self.grid[start_coord]):
            case (True, _):
                return self.peaks[start_coord], self.trails[start_coord]
            case (False, 9):
                self.peaks[start_coord] = {start_coord}
                self.trails[start_coord] = 1
                return self.peaks[start_coord], self.trails[start_coord]
            case (False, _):
                self.peaks[start_coord], self.trails[start_coord] = set(), 0
                for nb in self.get_neighbors(start_coord):
                    peaks, trails = self._get_peaks_and_trails_dfs(nb)
                    self.peaks[start_coord].update(peaks)
                    self.trails[start_coord] += trails
                return self.peaks[start_coord], self.trails[start_coord]
        return set(), 0  # This will never happen, but linter angry there is no return statement

    def count_all_peaks_and_trails(self) -> tuple[int, int]:
        for coord in self.trail_heads:
            self._get_peaks_and_trails_dfs(coord)
        return sum(len(self.peaks[cd]) for cd in self.trail_heads), sum(self.trails[cd] for cd in self.trail_heads)


# Test
test_map = TopoMap("inputs/day10/test.txt")
peaks, trails = test_map.count_all_peaks_and_trails()
assert peaks == 36
assert trails == 81

# Main
map = TopoMap("inputs/day10/main.txt")
peaks, trails = map.count_all_peaks_and_trails()
print(f"Part 1: {peaks}")
print(f"Part 1: {trails}")
