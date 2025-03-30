import os
import threading

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
        # for i, frame in enumerate(frames):
        #     print(f"Работаю с фреймом {i}")
        #     # Получим время фрейма в сек.
        #     time = i / clip.fps
        #     # превратим цифры в кадр изображения
        #     image = Image.fromarray(frame)
        #     after_filter = self.__change_func(image, time, red, green, blue, intns, area_size, funcNum)
        #     # кладём изображение после фильтра в new_frames
        #     new_frames.append(np.array(after_filter))
        new_clip = ImageSequenceClip(frames, fps=clip.fps)
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

    def combination(self, clip2: VideoFileClip, duration=1.0):
            clip1 = self.change_video_while_playing(self.clip, 0, 0, 0, 0, 0, 0)
            clip2 = self.change_video_while_playing(clip2, 0, 0, 0, 0, 0, 0)
            

            final_clip = self.page_flip_transition(clip1, clip2, duration)
            
            self.save_clip(final_clip, "output_transition.mp4")

    def page_flip_transition(self, clip1, clip2, duration):
        # Собираем все кадры для итогового видео
        frames = []
        fps = clip1.fps  # Используем FPS первого клипа
        
        # 1. Добавляем кадры первого клипа ДО перехода
        frames_before_transition = int((clip1.duration - duration) * fps)
        for i in range(frames_before_transition):
            t = i / fps
            frames.append(clip1.get_frame(t))
        
        # 2. Создаем кадры перехода
        transition_frames = int(duration * fps)
        for i in range(transition_frames):
            t_transition = i / fps  # Время внутри перехода
            t_clip1 = clip1.duration - duration + t_transition  # Время в первом клипе
            t_clip2 = t_transition  # Время во втором клипе
            
            alpha = t_transition / duration  # Прогресс перехода (0..1)
            frame1 = clip1.get_frame(t_clip1)
            frame2 = clip2.get_frame(t_clip2)
            
            # Эффект "перелистывания" (можно модифицировать)
            transition_frame = (1-alpha)*frame1 + alpha*frame2
            frames.append(transition_frame)
        
        # 3. Добавляем оставшиеся кадры второго клипа ПОСЛЕ перехода
        frames_after_transition = int((clip2.duration - duration) * fps)
        for i in range(frames_after_transition):
            t = duration + (i / fps)
            frames.append(clip2.get_frame(t))
        
        # Создаем итоговый клип
        return ImageSequenceClip(frames, fps=fps)
