class Node:
    def __init__(self, name, superorbits=[], num_parents=0):
        self.name = name
        self.suborbits = []
        self.superorbits = superorbits 
        self.num_parents = num_parents

    def has_children(self):
        if self.suborbits:
            return True
        return False


def load_input() -> list:
    orbits = []
    with open('./input.txt', 'r') as f:
        for line in f:
           orbital = line.strip().split(')')
           orbits.append(orbital)
    return orbits


def build_branch(parent: Node, orbits: list) -> Node:
    children = [orbit for orbit in orbits if orbit[0] == parent.name]
    if children:
        for child in children:
            node = Node(
                name=child[1],
                superorbits=(parent.superorbits + [parent.name]),
                num_parents=(parent.num_parents + 1)
            )
            node = build_branch(node, orbits)
            parent.suborbits.append(node)
    return parent 


def count_nodes(parent: Node) -> int:
    num_orbits = 0
    if parent.has_children:
        for child in parent.suborbits:
            num_orbits += count_nodes(child)
    return num_orbits + parent.num_parents


def get_closest_ancestor(src: str, dst: str, tree: Node) -> Node:
    def flatten_tree(tree):
        out = [tree]
        for node in tree.suborbits:
            out = out + flatten_tree(node)
        return out

    flattened = flatten_tree(tree)
    transit_nodes = [
        node.superorbits for node in flattened if node.name in [src, dst]]

    for node in transit_nodes[0][::-1]:
        if node in transit_nodes[1]:
            common_ancestor = node
            break

    print(
        len(transit_nodes[0][transit_nodes[0].index(common_ancestor):]) + \
        len(transit_nodes[1][transit_nodes[1].index(common_ancestor):]) - 2)


def main():
    orbits = load_input()
    com = Node(name='COM')
    com = build_branch(com, orbits)

    get_closest_ancestor('YOU', 'SAN', com)


if __name__ == '__main__':
    main()
