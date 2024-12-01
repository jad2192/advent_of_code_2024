from collections import defaultdict


def load_id_lists(docuemnt_path: str) -> list[str]:
    return open(docuemnt_path).read().split("\n")


def get_ordered_id_lists(raw_id_list: list[str]) -> tuple[list[int], list[int]]:
    list_l, list_r = [], []
    for id_pair in [l.split() for l in raw_id_list]:
        list_l.append(int(id_pair[0]))
        list_r.append(int(id_pair[1]))
        list_l.sort()
        list_r.sort()
    return list_l, list_r


def get_total_distance(list1: list[int], list2: list[int]) -> int:
    return sum(abs(x - y) for x, y in zip(list1, list2))


def get_total_similarity(list_l: list[int], list_r: list[int]) -> int:
    multiplicity_dict: dict[int, int] = defaultdict(int)
    set_l = set(list_l)
    for id_r in list_r:
        if id_r in set_l:
            multiplicity_dict[id_r] += id_r
    return sum(multiplicity_dict[id_l] for id_l in list_l)


# Test
test_list_raw = load_id_lists("inputs/day01/test.txt")
test_list_l, test_list_r = get_ordered_id_lists(test_list_raw)
assert get_total_distance(test_list_l, test_list_r) == 11
assert get_total_similarity(test_list_l, test_list_r) == 31


# Main Solution
list_raw = load_id_lists("inputs/day01/main.txt")
list_l, list_r = get_ordered_id_lists(list_raw)
print(f"Part 1: {get_total_distance(list_l, list_r)}")
print(f"Part 2: {get_total_similarity(list_l, list_r)}")
