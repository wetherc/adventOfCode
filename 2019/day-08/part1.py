import numpy as np


def load_input():
    pixels = []
    with open('./input.txt', 'r') as f:
        for line in f:
            pixels = pixels + [int(pixel) for pixel in line.strip()]
    return pixels


def pixels_to_layers(pixels, width, height):
    batch = width * height
    layers = []
    while pixels:
        layers.append(np.array(pixels[0:batch]))
        del pixels[0:batch]
    return layers


def get_checksum(layers):
    checksum_layer = None
    count_nonzeroes = np.inf * -1
    for layer in layers:
        if np.count_nonzero(layer) > count_nonzeroes:
            checksum_layer = layer
            count_nonzeroes = np.count_nonzero(layer)

    flat = checksum_layer.flatten()
    checksum = (
        sum(np.where(flat == 1, True, False)) *
        sum(np.where(flat == 2, True, False))
    )

    return checksum


def main():
    pixels = load_input()
    layers = pixels_to_layers(pixels, 25, 6)
    checksum = get_checksum(layers)

    print(f'Checksum for least empty layer is {checksum}')


if __name__ == '__main__':
    main()
