import os
import threading

import numpy as np

from lab01 import lab01 as l1
from moviepy import VideoFileClip, ImageSequenceClip, CompositeVideoClip, vfx, VideoClip, concatenate_videoclips

from PIL import Image


class VideoRemaker():
    def __init__(self, clip: VideoFileClip):
        self.clip = clip

    # сделаем функцию высшего порядка
    def change_video_while_playing(self, clip, red, green, blue, intns, area_size, funcNum):
        # будем собирать фреймы видео пошагово
        # на основе проходящих через фильтр кадров
        new_frames = []
        # разберём текущее видео на фреймы
        frames = [frame for frame in clip.iter_frames()]
        for i, frame in enumerate(frames):
            print(f"Работаю с фреймом {i}")
            # Получим время фрейма в сек.
            time = i / clip.fps
            # превратим цифры в кадр изображения
            image = Image.fromarray(frame)
            after_filter = self.__change_func(image, time, red, green, blue, intns, area_size, funcNum)
            # кладём изображение после фильтра в new_frames
            new_frames.append(np.array(after_filter))
        new_clip = ImageSequenceClip(new_frames, fps=clip.fps)
        return new_clip

    def save_clip(self, clip, dstn):
        dstn = "output/" + dstn
        os.makedirs(os.path.dirname(dstn), exist_ok=True)
        clip.write_videofile(dstn, codec="libx264")

    def __change_func(self, image: Image, time: int, red, green, blue, intns, area_size, funcNum) -> Image:
        remaker = l1.ImageRemaker(image)
        time *= 10
        if funcNum == 1:
            filtered_image = remaker.color_correction(red=red * time, green=green * time, blue=blue * time)
        elif funcNum == 2:
            filtered_image = remaker.add_noise(int(intns * time))
        elif funcNum == 3:
            filtered_image = remaker.monotone(int(area_size * time))
        return filtered_image

    def combination(self, clip2: VideoFileClip, red, green, blue, intns, area_size):
        # Создаем потоки

        clip1 = self.change_video_while_playing(self.clip, red, green, blue, intns, area_size, 2)
        clip2 = self.change_video_while_playing(clip2, red, green, blue, intns, area_size, 1)

        # Сохраняем результат
        final_clip.write_videofile("output_crossfade.mp4", fps=24)
