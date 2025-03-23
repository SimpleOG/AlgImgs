import os
import random

from PIL import Image


class ImageRemaker:
    def __init__(self, image: Image):
        self.image = image
        self.width, self.height = image.size  # длина ширина картинки

    def save_image(self, image: Image, dstn: str):
        dstn = "output/" + dstn
        os.makedirs(os.path.dirname(dstn), exist_ok=True)
        image.save(dstn)

    # цветокоррекция
    # будем настраивать интенсивность цветов через аргументы
    def color_correction(self, red: float, green: float, blue: float):
        # скопируем изображение, чтобы не менять изначальное
        # будем производить все операции на копии
        corrected_image = self.image.copy()
        pixels = corrected_image.load()
        # фактически картинка - матрица изпикселей, пробежимся по пикселю и изменим его
        # так как картинки совпадают, не надо снова искать w , h

        for w in range(self.width):
            for h in range(self.height):
                r, g, b = pixels[w, h]
                # увеличиваем насыщение
                r = int(r * red)
                g = int(g * green)
                b = int(b * blue)
                # проверка чтоб не убежали за максимальное насыщение (255)
                r = min(r, 255)
                g = min(g, 255)
                b = min(b, 255)
                pixels[w, h] = r, g, b

        # сохраняем изображение в папку
        self.save_image(corrected_image, "color_corrected.jpg")

    # Накладываем шум на изображение
    def add_noise(self, intns: int):
        # Опять же - создаем копию изображения и работаем с ней
        new_image = self.image.copy()
        pixels = new_image.load()
        # Опять же - картинка состоит из пикселей, представленных в виде матрицы, поэтому пробегаемся по матрице и меняем
        # пиксели
        for w in range(self.width):

            for h in range(self.height):
                # берём текущие пиксели
                r, g, b = pixels[w, h]

                # Рандомно изменяем шум в цветовых каналах
                # проверяем чтоб не улетели за пределы 255
                r = max(0, min(r + random.randint(-intns, intns), 255))
                g = max(0, min(g + random.randint(-intns, intns), 255))
                b = max(0, min(b + random.randint(-intns, intns), 255))

                # Меняем изначальные пиксели изображения на новые
                pixels[w, h] = r, g, b

        # сохраняем новую картинку в папке
        self.save_image(new_image, "noisy.jpg")
    def Sepia(self, r: float, g: float, b: float):
        pass