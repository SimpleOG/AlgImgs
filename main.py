import wave

import numpy as np

from lab03 import lab03 as l

if __name__ == "__main__":
    soundDstn="sound.mp3"
    newDstn="sound.wav"
    base_factor = 1.1 #на сколько сильно изначально меняется звук(условно с 400 гц на 400*110%=440 гц)
    smoothness_coef = 0.3 # чтоб накинуть плавность вокруг фактора и туда сюда звук менялся
    modulation_speed = 0.5 # надстройка над плавностью чтобы контролировать как быстро происходит амплитуда
    l.change_pitch(soundDstn, newDstn, base_factor, smoothness_coef, modulation_speed)




