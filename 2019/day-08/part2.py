import numpy as np
from PIL import Image


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


def composite_layers(layers, width, height):
    out = np.full((height, width, 3), [0, 0, 0], dtype=np.uint8)

    # Layers are rendered with the first in front, last in back
    # so we'll iterate through them back-to-front here
    for layer in layers[::-1]:
        for idx, val in enumerate(layer):
            row = idx // 25
            col = idx - (25 * row)
            if val == 0:
                out[row, col] = [0, 0, 0]
            if val == 1:
                out[row, col] = [255, 255, 255]
    img = Image.fromarray(out, 'RGB')
    img.save('decoded.png')
    return True


def main():
    pixels = load_input()
    layers = pixels_to_layers(pixels, 25, 6)
    checksum = get_checksum(layers)

    print(f'Checksum for least empty layer is {checksum}')
    print('Compositing layers and rendering image...')
    composite_layers(layers, 25, 6)
    print('Image rendered and saved to decoded.png')


if __name__ == '__main__':
    main()
