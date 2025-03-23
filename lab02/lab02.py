import os

import numpy as np

import lab01.lab01 as l1
from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image


class VideoRemaker():
    def __init__(self, clip: VideoFileClip):
        self.clip = clip

    # сделаем функцию высшего порядка
    def change_video_while_playing(self,red,green,blue):
        # будем собирать фреймы видео пошагово
        # на основе проходящих через фильтр кадров
        new_frames = []
        # разберём текущее видео на фреймы
        frames = [frame for frame in self.clip.iter_frames()]
        for i, frame in enumerate(frames):
            print(f"Работаю с фреймом {i}")
            # Получим время фрейма в сек.
            time = i / self.clip.fps
            # превратим цифры в кадр изображения
            image = Image.fromarray(frame)
            after_filter = self.__change_func(image, time,red,green,blue)
            # кладём изображение после фильтра в new_frames
            new_frames.append(np.array(after_filter))
        new_clip = ImageSequenceClip(new_frames, fps=self.clip.fps)
        return new_clip

    def save_clip(self, clip, dstn):
        dstn = "output/" + dstn
        os.makedirs(os.path.dirname(dstn), exist_ok=True)
        clip.write_videofile(dstn, codec="libx264")

    def __change_func(self, image: Image, time: int,red,green,blue) -> Image:
        remaker = l1.ImageRemaker(image)
        time*=10
        filtered_image = remaker.color_correction(red=red * time, green=green * time, blue=blue * time)
        return filtered_image
