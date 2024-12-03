class MulXY:
    def __init__(self):
        self.x = ""
        self.y = ""
        self.ins_str = ""

    def update(self, ch: str):
        self.ins_str += ch
        match (ch.isdigit(), bool(self.x), bool(self.y)):
            case (False, _, _):
                pass
            case (True, False, _):
                self.x += ch
            case (True, True, True):
                self.y += ch
            case (True, True, False):
                if self.ins_str[-2] == ",":
                    self.y += ch
                else:
                    self.x += ch

    def execute(self):
        return 0 if not self.x or not self.y else int(self.x) * int(self.y)


def check_valid_character(active_scan: bool, mul_obj: "MulXY", ch: str):
    instruction_map = {
        "m": lambda ch: ch == "u",
        "u": lambda ch: ch == "l",
        "l": lambda ch: ch == "(",
        "(": lambda ch: ch.isdigit(),
    }
    if not active_scan:
        return ch == "m"
    elif not mul_obj.x:
        return instruction_map[mul_obj.ins_str[-1]](ch)
    elif not mul_obj.y:
        if mul_obj.ins_str[-1] == ",":
            return ch.isdigit()
        elif len(mul_obj.x) == 3:
            return ch == ","
        else:
            return ch == "," or ch.isdigit()
    else:
        if len(mul_obj.y) == 3:
            return ch == ")"
        else:
            return ch == ")" or ch.isdigit()


def get_all_valid_instructions(raw_signal: str) -> list[MulXY]:
    valid_instructions = []
    active_scan = False
    cur_instruciton = MulXY()
    for ch in raw_signal:
        active_scan = check_valid_character(active_scan, cur_instruciton, ch)
        if active_scan:
            cur_instruciton.update(ch)
            if ch == ")":
                valid_instructions.append(cur_instruciton)
                cur_instruciton = MulXY()
                active_scan = False
        else:
            cur_instruciton = MulXY()
    return valid_instructions


def get_gated_valid_instructions(raw_signal: str) -> list[MulXY]:
    valid_instructions = []
    signal_blocks = raw_signal.split("don't()")
    # gates start opem
    valid_instructions += get_all_valid_instructions(signal_blocks[0])
    if len(signal_blocks) == 1:
        return valid_instructions
    for signal_block in signal_blocks[1:]:
        do_blocks = signal_block.split("do()")
        if len(do_blocks) > 1:
            valid_instructions += get_all_valid_instructions("".join(do_blocks[1:]))
    return valid_instructions


# Test
raw_signal_test = open("inputs/day03/test.txt").read()
raw_signal_test2 = open("inputs/day03/test2.txt").read()
valid_instructions_test = get_all_valid_instructions(raw_signal_test)
gated_valid_instructions_test = get_gated_valid_instructions(raw_signal_test2)
assert sum(ins.execute() for ins in valid_instructions_test) == 161
assert sum(ins.execute() for ins in gated_valid_instructions_test) == 48

# Main
raw_signal = open("inputs/day03/main.txt").read()
valid_instructions = get_all_valid_instructions(raw_signal)
gated_valid_instructions = get_gated_valid_instructions(raw_signal)
print(f"Part 1: {sum(ins.execute() for ins in valid_instructions)}")
print(f"Part 2: {sum(ins.execute() for ins in gated_valid_instructions)}")
