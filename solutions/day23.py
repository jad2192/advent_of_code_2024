class NetWorkMap:
    def __init__(self, network_fp: str):
        self.edges: dict[str, set[str]] = {}
        for line in open(network_fp).read().split("\n"):
            n1, n2 = tuple(line.split("-"))
            if n1 in self.edges:
                self.edges[n1].add(n2)
            else:
                self.edges[n1] = {n2}
            if n2 in self.edges:
                self.edges[n2].add(n1)
            else:
                self.edges[n2] = {n1}

    def get_triplets(self) -> int:
        triplets = set(
            tuple(sorted([n1, n2, n3]))
            for n1 in self.edges
            for n2 in self.edges
            for n3 in self.edges
            if n1 in self.edges[n2]
            and n1 in self.edges[n3]
            and n2 in self.edges[n3]
            and any([n.startswith("t") for n in {n1, n2, n3}])
        )
        return len(triplets)

    def get_lan_party(self) -> str:
        lan_party = set()
        for node, edges in self.edges.items():
            cur_party = set()
            for n2 in edges:
                potential_party = {node, n2}
                for n3 in edges.difference(n2):
                    if all([n3 in self.edges[n] for n in potential_party]):
                        potential_party.add(n3)
                if len(potential_party) > len(cur_party):
                    cur_party = potential_party
            if len(cur_party) > len(lan_party):
                lan_party = cur_party
        return ",".join(sorted(lan_party))


# Test
test_network = NetWorkMap("inputs/day23/test.txt")
assert test_network.get_triplets() == 7
assert test_network.get_lan_party() == "co,de,ka,ta"

# Main
network = NetWorkMap("inputs/day23/main.txt")
print(f"Part 1: {network.get_triplets()}")
print(f"Part 2: {network.get_lan_party()}")
