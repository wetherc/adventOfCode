import os
from functools import reduce


def parse_input() -> str:
    parsed_input = []
    with open(
        os.path.dirname(os.path.abspath(__file__)) + '/input.txt',
        'r',
        encoding='utf-8') as f:
        for line in f:
            parsed_input.append([int(elem) for elem in line.strip()])
    return parsed_input

def check_tree_vis(x_coord, y_coord, forest):
    # If we're on the perimeter, the tree is visible
    if x_coord in [0, len(forest) - 1]:
        return True
    if y_coord in [0, len(forest[0]) - 1]:
        return True
    
    # If any tree in line-of-sight of the target is
    # taller than ours, we know th
    x_vis = all(
        tree < forest[y_coord][x_coord]
        for tree in forest[y_coord][0:x_coord]
    ) or all(
        tree < forest[y_coord][x_coord]
        for tree in forest[y_coord][(x_coord + 1):]
    )
    if x_vis:
        # print(x_vis)
        # print(x_coord, y_coord)
        return True
    
    y_vis = all(
        tree[x_coord] < forest[y_coord][x_coord]
        for tree in forest[0:y_coord]
    ) or all(
        tree[x_coord] < forest[y_coord][x_coord]
        for tree in forest[(y_coord + 1):]
    )
    if y_vis:
        # print(y_vis)
        # print(x_coord, y_coord)
        return True
    return False


def get_viewing_distance(x_coord, y_coord, forest):
    dist = [0, 0, 0, 0]

    # north
    for tree in range(y_coord, 0, -1):
        if forest[tree - 1][x_coord] >= forest[y_coord][x_coord]:
            dist[0] = y_coord - (tree - 1)
            break
        else:
            dist[0] = y_coord

    # east
    for tree in range(x_coord + 1, len(forest[0])):
        if forest[y_coord][tree] >= forest[y_coord][x_coord]:
            dist[1] = tree - x_coord
            break
        else:
            dist[1] = len(forest[0]) - 1 - x_coord

    # south
    for tree in range(y_coord + 1, len(forest)):
        if forest[tree][x_coord] >= forest[y_coord][x_coord]:
            dist[2] = tree - y_coord
            break
        else:
            dist[2] = len(forest) - 1 - y_coord

    # west
    for tree in range(x_coord , 0, -1):
        if forest[y_coord][tree - 1] >= forest[y_coord][x_coord]:
            dist[3] = x_coord - (tree - 1)
            break
        else:
            dist[3] = x_coord

    return reduce(lambda x, y: x * y, dist)


def main():
    parsed_input = parse_input()
    vis_trees = 0
    scenic_score = 0
    for x_idx in range(len(parsed_input[0])):
        for y_idx in range(len(parsed_input)):
            vis_trees = vis_trees + check_tree_vis(
                x_idx,
                y_idx,
                parsed_input)
            scenic_score = max(
                scenic_score,
                get_viewing_distance(
                    x_idx,
                    y_idx,
                    parsed_input)
            )
    print(f'Number of visible trees: {vis_trees}')
    print(f'Max scenic score: {scenic_score}')


if __name__ == '__main__':
    main()
    