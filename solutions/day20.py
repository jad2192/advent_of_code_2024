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

    def neighbors(self, z: complex) -> set[complex]:
        return {z + w for w in {1, -1, 1j, -1j} if z + w in self.track_spaces}

    def path_length(self, cheat_pos: complex | None = None) -> int:
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
        while path is not None:
            reverse -= 1
            path = parents.get(path)
            self.dists[path] = reverse
            length += path is not None
        self.dists = {k: v + length for k, v in self.dists.items()}
        return self.dists[self.end]

    def count_fast_cheats(self, cut_off: int) -> int:
        count = 0
        self.path_length()
        for skips in self.cheat_loci.values():
            count += abs(self.dists[skips[0]] - self.dists[skips[1]]) >= cut_off + 2
        return count


# Test
test_track = RaceTrack("inputs/day20/test.txt")
assert test_track.count_fast_cheats(4) == 30

# Main
track = RaceTrack("inputs/day20/main.txt")
print(f"Part 1: {track.count_fast_cheats(100)}")
