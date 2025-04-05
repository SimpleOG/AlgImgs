
import os

import numpy as np

from lab01 import lab01 as l1
from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image




class VideoRemaker():
    def __init__(self, clip: VideoFileClip):
        self.clip = clip


    def change_video_while_playing(self, clip, red, green, blue, intns, area_size, funcNum):
        # будем собирать фреймы видео пошагово
        # на основе проходящих через фильтр кадров
        # разберём текущее видео на фреймы
        frames = [frame for frame in clip.iter_frames()]
        new_frames = []
        for i, frame in enumerate(frames):
            print(f"Работаю с фреймом {i}")
            # Получим время фрейма в сек.
            time = i / clip.fps
            # превратим цифры в кадр изображения
            image = Image.fromarray(frame)
            after_filter = self.change_func(image, time, red, green, blue, intns, area_size, funcNum)
            # кладём изображение после фильтра в new_frames
            new_frames.append(np.array(after_filter))

        new_clip = ImageSequenceClip(new_frames, fps=clip.fps)
        return new_clip

    def save_clip(self, clip, dstn):
        dstn = "output/" + dstn
        os.makedirs(os.path.dirname(dstn), exist_ok=True)
        clip.write_videofile(dstn, codec="libx264")

    def change_func(self, image: Image, time: int, red, green, blue, intns, area_size, funcNum) -> Image:
        remaker = l1.ImageRemaker(image)
        time *= 10
        filter_img=any
        if funcNum == 1:
            filter_img = remaker.color_correction(red=red * time, green=green * time, blue=blue * time)
        elif funcNum == 2:
            filter_img = remaker.add_noise(int(intns * time))
        elif funcNum == 3:
            filter_img = remaker.monotone(int(area_size * time))
        return filter_img

    def combination(self, clip2: VideoFileClip, duration, red, green, blue, intns, area_size):
        clip1 = self.change_video_while_playing(self.clip, red, green, blue, intns, area_size, 1)
        clip2 = self.change_video_while_playing(clip2, red, green, blue, intns, area_size, 2)
        final_clip = self.page_flip_transition(clip1, clip2, duration)
        self.save_clip(final_clip, "output_transition.mp4")

    # визуальный эффект
    def page_flip_transition(self, clip1, clip2, duration):
        frames = []
        fps = clip1.fps

        # добавим кадры первого клипа до перехода
        frames_before_transition = int((clip1.duration - duration) * fps)  # время до начала перехода
        for i in range(frames_before_transition):
            t = i / fps  # время в секундах
            frames.append(clip1.get_frame(t))  # получаем кадр в момент времени t

        # Создаем сам переход
        transition_frames = int(duration * fps)
        for i in range(transition_frames):
            t_transition = i / fps  # Время внутри перехода
            t_clip1 = clip1.duration - duration + t_transition  # Время в первом клипе
            t_clip2 = t_transition  # Время во втором клипе

            alpha = t_transition / duration  # Прогресс перехода от 1 клипа ко второму
            frame1 = clip1.get_frame(t_clip1)
            frame2 = clip2.get_frame(t_clip2)

            # Эффект "перелистывания", т.е. наш переход
            transition_frame = (1 - alpha) * frame1 + alpha * frame2
            frames.append(transition_frame)

        # Добавляем оставшиеся кадры второго клипа после перехода
        frames_after_transition = int((clip2.duration - duration) * fps)
        for i in range(frames_after_transition):
            t = duration + (i / fps)
            frames.append(clip2.get_frame(t))

        return ImageSequenceClip(frames, fps=fps)
