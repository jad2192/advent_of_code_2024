def load_reports(docuemnt_path: str) -> list[list[int]]:
    return [[int(k) for k in l.split()] for l in open(docuemnt_path).read().split("\n")]


def check_report_safety(report: list[int]) -> bool:
    prev_sign = 0
    for k in range(1, len(report)):
        sign = report[k] - report[k - 1]
        if sign * prev_sign < 0:
            return False  # Not monotone
        if not (1 <= abs(report[k] - report[k - 1]) <= 3):
            return False  # Must differ by at least 1 and at most 3
        prev_sign = sign
    return True


def check_dampened_report_safety(report: list[int]) -> bool:
    return check_report_safety(report) or max(
        check_report_safety(report[:k] + report[k + 1 :]) for k in range(len(report))
    )


# Test
test_reports = load_reports("inputs/day02/test.txt")
safe_test_reports = [rep for rep in test_reports if check_report_safety(rep)]
safe_test_reports_damp = [rep for rep in test_reports if check_dampened_report_safety(rep)]
assert len(safe_test_reports) == 2
assert len(safe_test_reports_damp) == 4

# Main Solution
reports = load_reports("inputs/day02/main.txt")
safe_reports = [rep for rep in reports if check_report_safety(rep)]
safe_reports_damp = [rep for rep in reports if check_dampened_report_safety(rep)]
print(f"Part 1: {len(safe_reports)}")
print(f"Part 2: {len(safe_reports_damp)}")
