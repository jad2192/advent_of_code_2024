class MagicStones:
    def __init__(self, stone_document: str):
        self.stones = open(stone_document).read().strip().split()
        self.stone_tracker: dict[tuple[str, int], int] = {}

    @staticmethod
    def _stone_ops(stone: str) -> list[str]:
        match (stone, len(stone) % 2):
            case ("0", 1):
                return ["1"]
            case (_, 0):
                return [stone[: len(stone) // 2], stone[len(stone) // 2 :].lstrip("0") or "0"]
        return [str(int(stone) * 2024)]

    def _stone_evolution(self, stone: str, blinks: int) -> int:
        if (stone, blinks) in self.stone_tracker:
            return self.stone_tracker[(stone, blinks)]
        elif blinks == 1:
            self.stone_tracker[(stone, blinks)] = len(self._stone_ops(stone))
            return self.stone_tracker[(stone, blinks)]
        else:
            self.stone_tracker[(stone, blinks)] = sum(
                self._stone_evolution(st, blinks - 1) for st in self._stone_ops(stone)
            )
            return self.stone_tracker[(stone, blinks)]

    def count_stone_line_evolution(self, blinks: int = 25) -> int:
        return sum(self._stone_evolution(stone, blinks) for stone in self.stones)


# Test
test_stones = MagicStones("inputs/day11/test.txt")
assert test_stones.count_stone_line_evolution(25) == 55312

# Main
stones = MagicStones("inputs/day11/main.txt")
print(f"Part 1: {stones.count_stone_line_evolution(25)}")
print(f"Part 2: {stones.count_stone_line_evolution(75)}")
