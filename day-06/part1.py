class Node:
    def __init__(self, name, num_parents):
        self.name = name
        self.suborbits = []
        self.num_parents = num_parents

    def has_children(self):
        if self.suborbits:
            return True
        return False


def load_input():
    orbits = []
    with open('./input.txt', 'r') as f:
        for line in f:
           orbital = line.strip().split(')')
           orbits.append(orbital)
    return orbits


def build_branch(parent: Node, orbits: list):
    children = [orbit for orbit in orbits if orbit[0] == parent.name]
    if children:
        for child in children:
            node = Node(
                name=child[1],
                num_parents=(parent.num_parents + 1)
            )
            node = build_branch(node, orbits)
            parent.suborbits.append(node)
    return parent 


def count_nodes(parent: Node):
    num_orbits = 0
    if parent.has_children:
        for child in parent.suborbits:
            num_orbits += count_nodes(child)
    return num_orbits + parent.num_parents


def main():
    orbits = load_input()
    com = Node(name='COM', num_parents=0)
    com = build_branch(com, orbits)

    orbit_count = count_nodes(com)
    print(orbit_count)


if __name__ == '__main__':
    main()
