from lab01 import lab01 as l1

from PIL import Image

IMAGE_SOURCE = "test_photo.jpg"

if __name__ == "__main__":
    image = Image.open(IMAGE_SOURCE)
    remaker = l1.ImageRemaker(image)
    remaker.color_correction(red=4.5, green=1.5, blue=2.0)
    remaker.add_noise(intns=140)
