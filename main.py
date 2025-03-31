from lab01 import lab01 as l1
from lab02 import lab02 as l2
from moviepy import VideoFileClip
from PIL import Image
IMAGE_SOURCE = "test_photo.jpg"
VIDEO1_SOURCE = "clip.mp4"
if __name__ == "__main__":
    # lab1
    image = Image.open(IMAGE_SOURCE)
    remaker = l1.ImageRemaker(image)
    red = 0.8
    green = 0.4
    blue = 0.2
    intns = 10
    area_size = 4
    duration = 1.5
    # img1 = remaker.color_correction( red, green, blue)
    # remaker.save_image(img1,"color_corrected.jpg")
    #
    # img2 = remaker.add_noise(intns)
    # remaker.save_image(img2, "noisy.jpg")
    #
    # img3 = remaker.sepia()
    # remaker.save_image(img3, "sepia.jpg")
    #
    # img4 = remaker.monotone(area_size)
    # remaker.save_image(img4,"mono_img.jpg")
    # lab2
    clip = VideoFileClip(VIDEO1_SOURCE)
    VideoMaker = l2.VideoRemaker(clip)
    clip1 = VideoMaker.change_video_while_playing(VideoMaker.clip, red, green, blue, intns, area_size, 1)
    VideoMaker.save_clip(clip1, "new_vid1.mp4")
    clip2 = VideoFileClip(VIDEO1_SOURCE)

    VideoMaker.combination(clip2, duration, red, green, blue, intns, area_size)