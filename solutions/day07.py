def load_equations(document_path: str) -> list[tuple[int, list[int]]]:
    equations = []
    for line in open(document_path).read().split("\n"):
        split_line = line.split(":")
        equations.append((int(split_line[0]), [int(d) for d in split_line[1].split()]))
    return equations


def check_equation(equation: tuple[int, list[int]], inc_concat: bool = False) -> bool:
    value, comps = equation
    if len(comps) == 1:
        return value == comps[0]
    elif len(comps) == 2:
        two_op = (value == sum(comps)) or (value == comps[0] * comps[1])
        return two_op or (inc_concat and str(value) == f"{comps[0]}{comps[1]}")
    if value % comps[-1] == 0:
        if check_equation((value // comps[-1], comps[:-1]), inc_concat):
            return True
    if inc_concat and str(value).endswith(str(comps[-1])) and value != comps[-1]:
        sub_value = int(str(value)[: -len(str(comps[-1]))])
        if check_equation((sub_value, comps[:-1]), inc_concat):
            return True
    return check_equation((value - comps[-1], comps[:-1]), inc_concat)


# Test
test_equations = load_equations("inputs/day07/test.txt")
valid_equations_all = [eq for eq in test_equations if check_equation(eq, inc_concat=True)]
valid_equations_add_mult_val = [eq[0] for eq in valid_equations_all if check_equation(eq)]
assert sum(valid_equations_add_mult_val) == 3749
assert sum(eq[0] for eq in valid_equations_all) == 11387

# Main
equations = load_equations("inputs/day07/main.txt")
valid_equations_all = [eq for eq in equations if check_equation(eq, inc_concat=True)]
valid_equations_vals = [eq[0] for eq in valid_equations_all if check_equation(eq)]
print(f"Part 1: {sum(valid_equations_vals)}")
print(f"Part 2: {sum(eq[0] for eq in valid_equations_all)}")
