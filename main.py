from lab01 import lab01 as l1
from lab02 import lab02 as l2
from moviepy import VideoFileClip, ImageSequenceClip
from PIL import Image

IMAGE_SOURCE = "test_photo.jpg"
VIDEO1_SOURCE = "clip.mp4"
if __name__ == "__main__":
    # lab1
    # image = Image.open(IMAGE_SOURCE)
    # remaker = l1.ImageRemaker(image)
    # img1 = remaker.color_correction(red=1.5, green=2.5, blue=3.8)
    # remaker.save_image(img1,"color_corrected.jpg")
    # img2 = remaker.add_noise(intns=120)
    # remaker.save_image(img2, "noisy.jpg")
    # img3 = remaker.monotone(area_size=9)
    # remaker.save_image(img3,"mono_img.jpg")
    # lab2
    clip = VideoFileClip(VIDEO1_SOURCE)
    VideoMaker=l2.VideoRemaker(clip)
    clip1=VideoMaker.change_video_while_playing(red=1.5, green=2.5, blue=3.8)
    VideoMaker.save_clip(clip1,"noisy_vid.mp4")