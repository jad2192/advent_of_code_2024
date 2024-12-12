MAP = {1j: "d", -1j: "u", 1: "r", -1: "l"}


class GardenMap:
    def __init__(self, map_fp: str):
        self.grid: dict[complex, str] = {
            complex(c, r): chr for r, list in enumerate(open(map_fp).read().split("\n")) for c, chr in enumerate(list)
        }
        self.plot_perimeters: dict[complex, list[complex]] = {}
        self.connected_components: list[set[complex]] = []

    def _get_neighbors(self, z: complex) -> list[complex]:
        directions = {1, -1, 1j, -1j}
        nbrs = [z + w for w in directions if self.grid.get(z + w, "oob") == self.grid[z]]
        self.plot_perimeters[z] = [w for w in directions if self.grid.get(z + w, "oob") != self.grid[z]]
        return nbrs

    def _get_plot_perimeter(self, z: complex) -> list[complex]:
        if z in self.plot_perimeters:
            return self.plot_perimeters[z]
        self.plot_perimeters[z] = [w for w in {1, -1, 1j, -1j} if self.grid.get(z + w, "oob") != self.grid[z]]
        return self.plot_perimeters[z]

    def _get_connected_components(self):
        if self.connected_components:
            pass
        else:
            visited_coords = set()
            for z in self.grid:
                component = set()
                dfs_stack = [z] if z not in visited_coords else []
                while dfs_stack:
                    w = dfs_stack.pop(0)
                    if w not in component:
                        component.add(w)
                        dfs_stack += self._get_neighbors(w)
                if component:
                    visited_coords.update(component)
                    self.connected_components.append(component)

    def _get_connected_line(self, z: complex, dxn: complex, component: set[complex]) -> set[complex]:
        line = set()
        while z + dxn in component:
            line.add(z + dxn)
            z += dxn
        return line

    def _get_discount_perimeter(self, component: set[complex]) -> int:
        boundary = {z for z in component if len(self._get_plot_perimeter(z)) > 0}
        z_stack, perimeter, fences = sorted(list(boundary), key=lambda w: (w.imag, w.real)), 0, {}  # type:ignore
        while z_stack:
            z = z_stack.pop(0)
            if z not in fences:
                nbrs = boundary.intersection(self._get_neighbors(z))
                perimeters = self.plot_perimeters[z]
                new_fences = [w for w in perimeters if all([w not in fences.get(nb, []) for nb in nbrs])]
                perimeter += len(new_fences)
                fences[z] = perimeters
                z_stack.extend(nb for nb in nbrs if nb not in fences)
        return perimeter

    def calculate_fencing_cost(self, bulk_discount: bool = False) -> int:
        self._get_connected_components()
        if not bulk_discount:
            return sum(len(c) * sum(len(self._get_plot_perimeter(z)) for z in c) for c in self.connected_components)
        else:
            return sum(len(comp) * self._get_discount_perimeter(comp) for comp in self.connected_components)


# Test
test_garden1 = GardenMap("inputs/day12/test.txt")
test_garden2 = GardenMap("inputs/day12/test2.txt")
test_garden3 = GardenMap("inputs/day12/test3.txt")
test_garden4 = GardenMap("inputs/day12/test4.txt")
assert test_garden1.calculate_fencing_cost() == 140
assert test_garden2.calculate_fencing_cost() == 1930
assert test_garden1.calculate_fencing_cost(bulk_discount=True) == 80
assert test_garden2.calculate_fencing_cost(bulk_discount=True) == 1206
assert test_garden3.calculate_fencing_cost(bulk_discount=True) == 236
assert test_garden4.calculate_fencing_cost(bulk_discount=True) == 368

# Main
garden = GardenMap("inputs/day12/main.txt")
print(f"Part 1: {garden.calculate_fencing_cost()}")
print(f"Part 2: {garden.calculate_fencing_cost(bulk_discount=True)}")
