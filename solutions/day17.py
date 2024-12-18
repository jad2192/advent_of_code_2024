class Triplit:
    def __init__(self, base10: int):
        self.base10 = base10
        self.bits = (base10 % 2, base10 // 2 % 2, base10 // 4 % 2)

    def xor(self, bits: "Triplit") -> "Triplit":
        return Triplit(sum((self.bits[k] + bits[k]) % 2 * 2**k for k in range(3)))


class Compooter:
    def __init__(self, program_fp: str):
        register_str, program_str = tuple(open(program_fp).read().split("\n\n"))
        registers = register_str.split("\n")
        self.reg_a = Triplit(int(registers[0].split("A: ")[-1]))
        self.reg_b = Triplit(int(registers[1].split("B: ")[-1]))
        self.reg_c = Triplit(int(registers[2].split("C: ")[-1]))
        self.program = [Triplit(int(d)) for d in program_str.split(": ")[-1].split(",")]

    def _operand(self, operand: Triplit) -> Triplit:
        if 0 <= operand.base10 <= 3:
            return operand
        elif operand.base10 == 4:
            return self.reg_a
        elif operand.base10 == 5:
            return self.reg_b
        elif operand.base10 == 6:
            return self.reg_c
        else:
            raise ValueError("Operand 7 not valid in program")

    def _opcode(self, code: Triplit, operand: Triplit) -> str | None:
        if code.base10 == 0:
            self.reg_a = Triplit(self.reg_a.base10 // 2 ** (self._operand(operand).base10))
        elif code.base10 == 1:
            self.reg_b = self.reg_b.xor(operand)
        elif code.base10 == 1:
            self.reg_b = self.reg_b.xor(operand)
        elif code.base10 == 2:
            self.reg_b = self.reg_b.xor(operand)


# Test
test_puter = Compooter("inputs/day17/test.txt")
print(test_puter.reg_a, test_puter.reg_b, test_puter.reg_c, test_puter.program)
