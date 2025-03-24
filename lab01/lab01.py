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
        new_image = self.image.copy()
        pixels = new_image.load()
        # фактически картинка - матрица изпикселей, пробежимся по пикселю и изменим его
        # так как картинки совпадают, не надо снова искать w , h

        for w in range(self.width):
            for h in range(self.height):
                r, g, b = pixels[w, h]
                # if h%50==0:
                #     print(f"old pixels {pixels[w,h]}")
                # увеличиваем насыщение
                r = int(r * red)
                g = int(g * green)
                b = int(b * blue)
                # if h % 50 == 0:
                #     print(f"new_pixels {r},{g},{b}")
                # проверка чтоб не убежали за максимальное насыщение (255)
                r = min(r, 255)
                g = min(g, 255)
                b = min(b, 255)
                pixels[w, h] = r, g, b

        return new_image

    # Накладываем шум на изображение
    def add_noise(self, intns: int):
        # Опять же - создаем копию изображения и работаем с ней
        new_image = self.image.copy()
        pixels = new_image.load()
        # Опять же - картинка состоит из пикселей, представленных в виде матрицы,
        # поэтому пробегаемся по матрице и меняем
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

        return new_image
    #сепия
    def sepia(self):
        # вновь скопируем изображение
        new_image = self.image.copy()
        pixels = new_image.load() 
        #проходимся по всей матрице из писелей
        for w in range(self.width):
            for h in range(self.height):
                # берём текущие пиксели
                r, g, b = pixels[w, h]
                #Сепия - это теплый коричневатый оттенок, поэтому мы берем такие коэф., чтобы преобладали 
                #красный и зеленый, после "смешиваем" их
                r1 = 0.4 * r + 0.75 * g + 0.15 * b
                g2 = 0.35 * r + 0.7 * g + 0.15 * b
                b3 = 0.25 * r + 0.5 * g + 0.1 * b
                # проверка чтоб не убежали за максимальное насыщение (255)
                r1 = min(int(r1), 255)
                g2 = min(int(g2), 255)
                b3 = min(int(b3), 255)
                # Меняем изначальные пиксели изображения на полученные
                pixels[w, h] = r1, g2, b3
        return new_image

    # Монотонность на изображении

    # Что мы в принципе хотим?
    # Выбираем область размера area
    # внутри области уменьшаем значение каждого из цветов в соотв. с усред. значением
    def monotone(self, area_size):
        new_image = self.image.copy()
        pixels = new_image.load()

        half_size = area_size // 2
        # избегаем выхода за пределы краёв фотки
        for w in range(half_size, self.width - half_size):
            for h in range(half_size, self.height - half_size):
                # Собираем значения пикселей в области
                r_sum, g_sum, b_sum = 0, 0, 0
                count = 0
                # поищем все пиксели вокруг центрального. Для примера в area=3 получаем
                # (w - 1, h - 1) | (w, h - 1) | (w + 1, h - 1)
                # (w - 1, h)     |   (x, h)   | (w + 1, h)
                # (w - 1, h + 1) | (w, h + 1) | (w + 1, h + 1)
                for i in range(-half_size, half_size + 1):
                    for j in range(-half_size, half_size + 1):
                        r, g, b = pixels[w + i, h + j]
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        count += 1
                # Усредняем значения
                new_r = r_sum // count
                new_g = g_sum // count
                new_b = b_sum // count

                # Присваиваем усредненное значение центральному пикселю
                pixels[w, h] = (new_r, new_g, new_b)

        return new_image
