from PIL import Image
import numpy as np
import json


def compress_image(img_path):
    img = Image.open(img_path)
    pixels = np.array(img)

    compressed = []
    for row in pixels:
        compressed_row = []
        current = row[0].tolist()
        count = 1
        for pixel in row[1:]:
            pixel = pixel.tolist()
            if pixel == current:
                count += 1
            else:
                compressed_row.append([current, count])
                current = pixel
                count = 1
        compressed_row.append([current, count])
        compressed.append(compressed_row)

    return compressed


def save_compressed(data, filename):

    with open(filename, 'w') as f:
        json.dump(data, f)


def load_compressed(filename):

    with open(filename, 'r') as f:
        return json.load(f)


def decompress_image(compressed_data):

    pixels = []

    for row in compressed_data:
        decompressed_row = []
        for item in row:
            pixel, count = item
            decompressed_row.extend([pixel] * count)
        pixels.append(decompressed_row)

    img_array = np.array(pixels, dtype=np.uint8)
    return Image.fromarray(img_array)

