import argparse
from re import sub

parser = argparse.ArgumentParser(description='Recursive circus')
parser.add_argument('--input')
parser.add_argument('--part')
args = parser.parse_args()


def read_programs(input):
    with open(input) as programs:
        for program in programs:
            yield program


def get_base(input):
    prog_count = {}

    for program in input:
        # Let's do the laziest solution possible!
        program = str.split(sub('[^a-zA-Z ]','', program))
        for elem in program:
            if elem in prog_count:
                prog_count[elem] += 1
            else:
                prog_count[elem] = 1
    output = min(prog_count.keys(), key=(lambda k: prog_count[k]))
    return output


def parse_programs(input):
    programs = {}
    for program in input:
        program = program.split(' -> ')
        programs[sub(r'\n', '', sub(r'^([a-zA-Z]+).*$', r'\1', program[0]))] = {
            'weight': int(sub(r'^.*\(([0-9]+)\).*$', r'\1', program[0])),
            'dsts': [sub(r'\n', '', elem) for elem in program[1].split(', ')]
                     if 1 < len(program) else None
        }
    return programs


def get_node_weights(input):
    for src in input.keys():
        dsts = input[src]['dsts']
        dst_weights = []
        ii = 0

        while dsts and ii < len(dsts):
            weight = input[dsts[ii]]['weight']
            subdsts = input[dsts[ii]]['dsts']
            jj = 0

            while subdsts and jj < len(subdsts):
                if subdsts[jj] is not None:
                    weight += input[subdsts[jj]]['weight']
                    try:
                        subdsts = subdsts + input[subdsts[jj]]['dsts']
                    except:
                        pass
                jj += 1
            dst_weights.append(weight)
            ii += 1
        input[src]['dst_weights'] = dst_weights
    return input

if __name__ == '__main__':
    programs = read_programs(args.input)

    if args.part == '1':
        output = get_base(programs)
    else:
        programs = parse_programs(programs)
        imbalanced_nodes = get_node_weights(programs)
        # Subset to include only imbalanced nodes
        imbalanced_nodes = [
            imbalanced_nodes[key] for key in imbalanced_nodes.keys()
            if (imbalanced_nodes[key]['dst_weights'][1:] !=
                imbalanced_nodes[key]['dst_weights'][:-1])]

        # find the deepest nested inequality of those nodes
        output = imbalanced_nodes.pop(0)
        for node in imbalanced_nodes:
            if min(node['dst_weights']) < min(output['dst_weights']):
                output = node
        mode = max(set(output['dst_weights']), key=output['dst_weights'].count)
        outlier = min(set(output['dst_weights']), key=output['dst_weights'].count)

        output = zip(output['dsts'], output['dst_weights'])
        output = [node for node in output if node[1] == outlier]
        output = programs[output[0][0]]['weight'] + (mode - outlier)
    print(output)
