from lab01 import lab01 as l1

from PIL import Image

IMAGE_SOURCE = "test_photo.jpg"

if __name__ == "__main__":
    image = Image.open(IMAGE_SOURCE)
    remaker = l1.ImageRemaker(image)
    #remaker.color_correction(red=1.5, green=2.5, blue=3.8)
    #remaker.add_noise(intns=120)
    remaker.monotone(area_size=9)
