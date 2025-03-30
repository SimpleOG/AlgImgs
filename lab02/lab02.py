import numpy as np

from lab01 import lab01 as l1
from moviepy import VideoFileClip, ImageSequenceClip, VideoClip, CompositeVideoClip, concatenate_videoclips

from PIL import Image
from moviepy.video.fx import FadeIn, FadeOut, Resize, CrossFadeIn, CrossFadeOut

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



