def load_disk_map(document_path: str) -> str:
    return open(document_path).read().strip()


class FreeSpaceQueue:
    def __init__(self):
        self.stack_dict = {k: [] for k in range(1, 10)}
        self.stack_priority = list(range(1, 10))

    def update_priority(self):
        self.stack_priority = sorted(
            [k for k in self.stack_dict if len(self.stack_dict[k]) > 0], key=lambda k: self.stack_dict[k][0][0]
        )

    def push(self, index_block: list[int], sort=False):
        if len(index_block) > 0:
            self.stack_dict[len(index_block)].append(index_block)
            if sort:
                self.stack_dict[len(index_block)].sort(key=lambda b: b[0])
            self.update_priority()

    def pop(self, file_index_block: list[int]) -> list[int] | None:
        index_block = None
        for k in self.stack_priority:
            if k >= len(file_index_block) and self.stack_dict[k][0][0] < file_index_block[0]:
                index_block = self.stack_dict[k].pop(0)
                break
        if index_block is not None:
            if len(index_block) > len(file_index_block):
                new_block = index_block[len(file_index_block) :]
                self.push(new_block, sort=True)
            else:
                self.update_priority()
        return index_block


def parse_disk(disk_map: str) -> tuple[list[int], FreeSpaceQueue, list[str]]:
    free_space_locs, free_space_queue, file = [], FreeSpaceQueue(), []  # type:ignore
    for k, char in enumerate(disk_map):
        start_ix = len(file)
        if k % 2 == 0:
            file.extend([f"{k // 2}"] * int(char))
        else:
            file.extend(["."] * int(char))
            free_space_locs.extend(range(start_ix, len(file)))
            free_space_queue.push(list(range(start_ix, len(file))))
    return free_space_locs, free_space_queue, file


def rearrange_file(free_space_locs: list[int], file: list[str]) -> list[str]:
    for k in range(len(file) - 1, 0, -1):
        if (k > free_space_locs[0]) and file[k] != ".":
            new_mem_ix = free_space_locs.pop(0)
            file[k], file[new_mem_ix] = file[new_mem_ix], file[k]
            free_space_locs.append(k)
    return file


def rearrange_file_by_blocks(free_space_queue: FreeSpaceQueue, file: list[str]) -> list[str]:
    file_blocks, index_blocks = [], []
    cur_block, curr_ix_block = [file[0]], [0]
    for k in range(1, len(file)):
        if file[k] == cur_block[-1]:
            cur_block.append(file[k])
            curr_ix_block.append(k)
        else:
            file_blocks.append(cur_block)
            index_blocks.append(curr_ix_block)
            cur_block, curr_ix_block = [file[k]], [k]
    if cur_block[0] != file_blocks[0][0]:
        file_blocks.append(cur_block)
        index_blocks.append(curr_ix_block)
    for file_bk, ix_bk in zip(file_blocks[::-1], index_blocks[::-1]):
        if file_bk[0] != ".":
            free_bk = free_space_queue.pop(ix_bk)
            if free_bk:
                # Track block start / end indices
                ix1, ix2, ix3, ix4 = free_bk[0], free_bk[0] + len(ix_bk), ix_bk[0], ix_bk[-1] + 1
                file[ix1:ix2], file[ix3:ix4] = file[ix3:ix4], file[ix1:ix2]  # Swap locs in file
    return file


def file_system_checksum(file: list[str]) -> int:
    return sum(k * int(chr) for k, chr in enumerate(file) if chr.isdigit())


# Test
disk_map_test = load_disk_map("inputs/day09/test.txt")
free_space_locs_test, free_blocks_test, test_file = parse_disk(disk_map_test)
test_ordered_file = rearrange_file(free_space_locs_test, list(test_file))
assert file_system_checksum(test_ordered_file) == 1928
assert file_system_checksum(rearrange_file_by_blocks(free_blocks_test, test_file)) == 2858

# Main
disk_map = load_disk_map("inputs/day09/main.txt")
free_space_locs, free_blocks, file = parse_disk(disk_map)
ordered_file = rearrange_file(free_space_locs, list(file))  # wrap in list so original file object is protected
ordered_file_by_blocks = rearrange_file_by_blocks(free_blocks, file)
print(f"Part 1: {file_system_checksum(ordered_file)}")
print(f"Part 2: {file_system_checksum(ordered_file_by_blocks)}")
