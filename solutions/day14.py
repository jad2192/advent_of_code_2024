class Robot:
    def __init__(self, robo_line: str, torus_width: int, torus_height: int):
        init_split = robo_line.split("v=")
        self.x, self.y = int(init_split[0][2:].split(",")[0]), int(init_split[0][2:].split(",")[1])
        self.v_x, self.v_y = int(init_split[1].split(",")[0]), int(init_split[1].split(",")[1])
        self.torus_w, self.torus_h = torus_width, torus_height

    def update_position(self, time_steps: int):
        self.x = (self.x + time_steps * self.v_x) % self.torus_w
        self.y = (self.y + time_steps * self.v_y) % self.torus_h

    def current_quadrant(self) -> int:
        if self.y == self.torus_h // 2 or self.x == self.torus_w // 2:
            return -1
        match (self.y < self.torus_h // 2, self.x < self.torus_w // 2):
            case (True, True):
                return 1
            case (True, False):
                return 2
            case (False, True):
                return 3
        return 4


def safety_factor(robots: list[Robot], time_steps: int) -> int:
    q_count = {q: 0 for q in {-1, 1, 2, 3, 4}}
    for robot in robots:
        robot.update_position(time_steps)
        q_count[robot.current_quadrant()] += 1
    return q_count[1] * q_count[2] * q_count[3] * q_count[4]


def compactness_score(robots: list[Robot], time_steps: int) -> float:
    max_density = 0
    grid = {(x, y): 0 for y in range(robots[0].torus_h) for x in range(robots[0].torus_w)}
    for r in robots:
        r.update_position(time_steps)
        grid[(r.x, r.y)] += 1
    for coord in grid:
        x_range = range(coord[0] - 3, coord[0] + 3)
        y_range = range(coord[1] - 3, coord[1] + 3)
        density = len([(x, y) for x in x_range for y in y_range if grid.get((x, y), 0) > 0])
        max_density = max(density, max_density)
    return max_density


def display_grid(robots: list[Robot]):
    grid = {(r, c): "." for r in range(robots[0].torus_h) for c in range(robots[0].torus_w)}
    for robot in robots:
        grid[(robot.y, robot.x)] = "#"
    for r in range(robots[0].torus_h):
        print("".join([grid[(r, c)] for c in range(robots[0].torus_w)]))


# Test
test_robots = [Robot(l, torus_width=11, torus_height=7) for l in open("inputs/day14/test.txt").read().split("\n")]
assert safety_factor(test_robots, 100) == 12

# Main
robots = [Robot(l, torus_width=101, torus_height=103) for l in open("inputs/day14/main.txt").read().split("\n")]
print(f"Part 1: {safety_factor(robots, 1000)}")
c_score = compactness_score(robots, 0)
it = 0
while c_score < 25 and it < 10000:
    c_score = compactness_score(robots, 1)
    it += 1
display_grid(robots)
print(f"Part 2: {it}")
