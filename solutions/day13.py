class ClawGame:
    def __init__(self, game_str: str):
        game_lines = [line.split(",") for line in game_str.split("\n")]
        self.x1, self.y1 = int(game_lines[0][0].split("+")[-1]), int(game_lines[0][1].split("+")[-1])
        self.x2, self.y2 = int(game_lines[1][0].split("+")[-1]), int(game_lines[1][1].split("+")[-1])
        self.x_p, self.y_p = int(game_lines[2][0].split("=")[-1]), int(game_lines[2][1].split("=")[-1])
        self.d = self.x1 * self.y2 - self.x2 * self.y1
        self.a_num = self.x_p * self.y2 - self.y_p * self.x2
        self.b_num = self.x_p * self.y1 - self.y_p * self.x1

    def solve(self, w_error: bool = False) -> int:
        a_num, b_num = int(self.a_num), int(self.b_num)
        if w_error:
            a_num += 10000000000000 * (self.y2 - self.x2)
            b_num += 10000000000000 * (self.y1 - self.x1)
        if any([self.d == 0, a_num % self.d != 0, b_num % self.d != 0]):
            return 0
        a, b = a_num // self.d, -b_num // self.d
        if w_error:
            return 3 * a + b
        else:
            return 3 * a + b if max(a, b) <= 100 else 0


def load_games(game_fp: str) -> list[str]:
    return open(game_fp).read().split("\n\n")


# Test
test_games_strings = load_games("inputs/day13/test.txt")
test_games: list[ClawGame] = [ClawGame(game_str) for game_str in test_games_strings]
assert sum([g.solve() for g in test_games]) == 480

# Main
games = [ClawGame(game_str) for game_str in load_games("inputs/day13/main.txt")]
print(f"Part 1: {sum([g.solve() for g in games])}")
print(f"Part 2: {sum([g.solve(w_error=True) for g in games])}")
