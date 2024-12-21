import math


class RaceTrack:
    def __init__(self, track_fp: str):
        self.track_spaces: set[complex] = set()
        self.track_walls: set[complex] = set()
        for imag, line in enumerate(open(track_fp).read().split("\n")):
            for real, chr in enumerate(line):
                if chr == "#":
                    self.track_walls.add(complex(real, imag))
                else:
                    self.track_spaces.add(complex(real, imag))
                    if chr == "S":
                        self.start = complex(real, imag)
                    if chr == "E":
                        self.end = complex(real, imag)
        self.cheat_loci = {}
        for z in self.track_walls:
            if z + 1 in self.track_spaces and z - 1 in self.track_spaces:
                self.cheat_loci[z] = [z + 1, z - 1]
            if z + 1j in self.track_spaces and z - 1j in self.track_spaces:
                self.cheat_loci[z] = [z + 1j, z - 1j]
        self.dists: dict[complex, int] = {}
        self.path = []

    def neighbors(self, z: complex) -> set[complex]:
        return {z + w for w in {1, -1, 1j, -1j} if z + w in self.track_spaces}

    def _compute_distances(self) -> int:
        parents = {self.start: None}
        queue = [self.start]
        while queue:
            z = queue.pop(0)
            if z == self.end:
                break
            for w in self.neighbors(z):
                if w not in parents:
                    parents[w] = z
                    queue.append(w)
        length, reverse = 0, 0
        path = self.end
        self.dists[path] = reverse
        self.path = [path]
        while path is not None:
            reverse -= 1
            path = parents.get(path)
            self.path = ([path] if path is not None else []) + self.path
            self.dists[path] = reverse
            length += path is not None
        self.dists = {k: v + length for k, v in self.dists.items()}
        return self.dists[self.end]

    def count_fast_cheats(self, cut_off: int) -> int:
        count = 0
        self._compute_distances()
        for skips in self.cheat_loci.values():
            count += abs(self.dists[skips[0]] - self.dists[skips[1]]) >= cut_off + 2
        return count

    def get_longer_cheats(self, cheat_duration: int, cut_off) -> int:
        if self.dists.get(self.end) is None:
            self._compute_distances()
        count = 0
        for k, z_entry in enumerate(self.path[:-cut_off]):
            for z_end in self.path[k + cut_off :]:
                d_l1 = abs(z_entry.real - z_end.real) + abs(z_entry.imag - z_end.imag)
                time_delt = self.dists[z_end] - self.dists[z_entry]
                count += d_l1 <= cheat_duration and d_l1 <= time_delt - cut_off
        return count


# Test
test_track = RaceTrack("inputs/day20/test.txt")
assert test_track.count_fast_cheats(4) == 30
assert test_track.get_longer_cheats(cheat_duration=2, cut_off=4) == 30

# Main
track = RaceTrack("inputs/day20/main.txt")
print(f"Part 1: {track.count_fast_cheats(100)}")
print(f"Part 2: {track.get_longer_cheats(cheat_duration=20, cut_off=100)}")
