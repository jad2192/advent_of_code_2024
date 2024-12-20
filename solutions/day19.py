class OnsenDesigns:
    def __init__(self, onsen_fp: str):
        self.cache: dict[str, int] = {}
        towel_str, pattern_str = open(onsen_fp).read().split("\n\n")
        self.towels: set[str] = towel_str.split(", ")
        self.patterns = pattern_str.split("\n")

    def count_orders(self, pattern: str) -> int:
        if pattern in self.cache:
            return self.cache[pattern]
        self.cache[pattern] = sum(
            self.count_orders(pattern[len(t) :]) for t in self.towels if pattern.startswith(t)
        ) + (pattern in self.towels)
        return self.cache[pattern]

    def count_possible(self) -> int:
        return sum(self.count_orders(pattern) > 0 for pattern in self.patterns)

    def count_all_options(self) -> int:
        return sum(self.count_orders(pattern) for pattern in self.patterns)


# Test
test_designs = OnsenDesigns("inputs/day19/test.txt")
assert test_designs.count_possible() == 6
assert test_designs.count_all_options() == 16

# Main
designs = OnsenDesigns("inputs/day19/main.txt")
print(f"Part 1: {designs.count_possible()}")
print(f"Part 2: {designs.count_all_options()}")
