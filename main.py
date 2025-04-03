from lab01 import lab01 as l1

from PIL import Image

IMAGE_SOURCE = "test_photo.jpg"

if __name__ == "__main__":
    image = Image.open(IMAGE_SOURCE)
    remaker = l1.ImageRemaker(image)

    img1 = remaker.color_correction(red=1.5, green=2.5, blue=1.8)
    remaker.save_image(img1,"color_corrected.jpg")

    img2 = remaker.add_noise(intns=120)
    remaker.save_image(img2, "noisy.jpg")

    img3 = remaker.sepia()
    remaker.save_image(img3, "sepia.jpg")

    img4 = remaker.monotone(area_size = 3, color_step= 40)
    remaker.save_image(img4,"mono_img.jpg")