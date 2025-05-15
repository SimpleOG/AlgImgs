import wave

import numpy as np

from lab03 import lab03 as l3
from lab04 import lab04 as l4

if __name__ == "__main__":
    # soundDstn="sound.mp3"
    # newDstn="sound.wav"
    # base_factor = 1.1 #на сколько сильно изначально меняется звук(условно с 400 гц на 400*110%=440 гц)
    # smoothness_coef = 0.3 # чтоб накинуть плавность вокруг фактора и туда сюда звук менялся
    # modulation_speed = 0.5 # надстройка над плавностью чтобы контролировать как быстро происходит амплитуда
    # l3.change_pitch(soundDstn, newDstn, base_factor, smoothness_coef, modulation_speed)

    # lab04

    compressed = l4.compress_image("test_photo.jpg")
    l4.save_compressed(compressed, "compressed.bmp")
    loaded_data = l4.load_compressed("compressed.bmp")
    img = l4.decompress_image(loaded_data)
    img.save("restored.jpg")