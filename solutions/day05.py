def load_raw_rules_and_updates(document_path: str) -> tuple[list[str], list[str]]:
    init_split = open(document_path).read().split("\n\n")
    return init_split[0].split("\n"), init_split[1].split("\n")


def get_update_lists(raw_updates: list[str]) -> list[list[int]]:
    return [[int(k) for k in line.split(",")] for line in raw_updates]


def get_ordered_rules(raw_rules: list[str]) -> set[str]:
    return set(raw_rules)  # X < Y iff "X|Y" in rule_set


def sort_bad_update(bad_update: list[int], order_rules: set[str]) -> list[int]:
    # run insertion sort
    for k in range(1, len(bad_update)):
        cur_val = bad_update[k]
        j = k - 1
        while j >= 0 and f"{cur_val}|{bad_update[j]}" in order_rules:
            bad_update[j + 1] = bad_update[j]
            j -= 1
        bad_update[j + 1] = cur_val
    return bad_update


def get_valid_updates(updates: list[list[int]], order_rules: set[str]) -> list[list[int]]:
    return [upd for upd in updates if all(f"{upd[k+1]}|{upd[k]}" not in order_rules for k in range(len(upd) - 1))]


def get_middle_digit(rule: list[int]) -> int:
    return rule[(len(rule) - 1) // 2]


# Test
raw_rules_test, raw_updates_test = load_raw_rules_and_updates("inputs/day05/test.txt")
rules_test = get_ordered_rules(raw_rules_test)
updates_test = get_update_lists(raw_updates_test)
valid_rules_test = get_valid_updates(updates_test, rules_test)
sorted_invalid_rules_test = [sort_bad_update(upd, rules_test) for upd in updates_test if upd not in valid_rules_test]
assert sum(get_middle_digit(rule) for rule in valid_rules_test) == 143
assert sum(get_middle_digit(rule) for rule in sorted_invalid_rules_test) == 123


# Main
raw_rules, raw_updates = load_raw_rules_and_updates("inputs/day05/main.txt")
rules = get_ordered_rules(raw_rules)
updates = get_update_lists(raw_updates)
valid_rules = get_valid_updates(updates, rules)
sorted_invalid_rules = [sort_bad_update(upd, rules) for upd in updates if upd not in valid_rules]
print(f"Part 1: {sum(get_middle_digit(rule) for rule in valid_rules)}")
print(f"Part 2: {sum(get_middle_digit(rule) for rule in sorted_invalid_rules)}")
