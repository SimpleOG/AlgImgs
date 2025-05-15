from PIL import Image
import numpy as np
import json
import pickle


def compress_image(img_path):
    img = Image.open(img_path)
    pixels = np.array(img)
    #сжатые пиксели
    compressed = []
    #в принципе весь алгоритм сводится к тому чтоб собрать все одинаковые пиксели вместе
    # в итоге как раз и получается динамическая map где ключ:значение это значение пикселя: его кол-во
    #условно если было [ [1,1,1],[2,2,2],[1,1,1]] , то станет [[1,1,1]:2,[2,2,2]:1"
    for row in pixels:
        #пробежимся по строкам пикселей
        compressed_row = []
        #запоминаем первый пиксель
        current = row[0].tolist()
        count = 1
        #пробежимся по всем остальным пикселям
        for i,pixel in enumerate(row[1:]) :
            #разложим пиксель в массив
            pixel = pixel.tolist()
            #сравним с первым
            if pixel == current:
                count += 1
            #если пиксель другой, теперь будем искать пиксели как этот
            else:
                compressed_row.append([current, count])
                current = pixel
                count = 1
        #пересобранные данные вернём в общий массив
        compressed_row.append([current, count])
        compressed.append(compressed_row)

    return compressed


def save_compressed(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_compressed(filename):

    with open(filename, 'rb') as f:
        return pickle.load(f)


def decompress_image(compressed_data):
    #обратный процесс разборки
    #сюда собираем итоговые пиксели
    pixels = []
    #пробегаемся по сжатым данным и распаковываем их
    # (то есть умножаем кол-во на пиксель [[2,2,2],3] -> [2,2,2][2,2,2][2,2,2]
    for row in compressed_data:
        decompressed_row = []
        for item in row:
            pixel, count = item
            decompressed_row.extend([pixel] * count)
        pixels.append(decompressed_row)
    #превращаем в 8битный массив
    img_array = np.array(pixels, dtype=np.uint8)
    #восстанавливаем итоговое изображение
    return Image.fromarray(img_array)

