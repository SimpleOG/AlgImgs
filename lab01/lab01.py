import os
import random
from collections import defaultdict
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
        #сепия. работает, но без параметра. В любом случае, это был уже доп фильтр, так что пусть просто останется
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

    # Монотонность на изображении, переделанная!!!

    # Монотонность на изображении, переделанная!!!

    # и так, пробуем изменить монотонность. Прошлый вариант замыливал область. Поэтому наша задача определить общий/средний цвет области и внутренний пиксель
    # закрасить таким же цветом.
    def monotone(self, area_size, color_step):
        new_image = self.image.copy()
        pixels = new_image.load()
        # избегаем выхода за пределы краёв фотки
        half_size = area_size // 2

        for w in range(half_size, self.width - half_size):
            for h in range(half_size, self.height - half_size):
                # посчитаем цвета в области
                counts = defaultdict(int)
                # поищем все пиксели вокруг центрального. Для примера в area=3 получаем
                # (w - 1, h - 1) | (w, h - 1) | (w + 1, h - 1)
                # (w - 1, h)     |   (x, h)   | (w + 1, h)
                # (w - 1, h + 1) | (w, h + 1) | (w + 1, h + 1)
                for i in range(-half_size, half_size + 1):
                    for j in range(-half_size, half_size + 1):
                        r, g, b = pixels[w + i, h + j]
                        # работаем с самими цветами. Для этого нам нужен color_step. Округляем цвета до ближайших, которые делятся на color_step.
                        # то есть делаем их более похожими
                        # чем больше брать размер области, тем более монотонным становится изображение.
                        r = (r // color_step) * color_step
                        g = (g // color_step) * color_step
                        b = (b // color_step) * color_step
                        new_color = (r, g, b)
                        counts[new_color] += 1

                # Вычисляем самый встречающийся цвет
                dominant_color = max(counts.items(), key=lambda item: item[1])[0]
                pixels[w, h] = dominant_color

        return new_image