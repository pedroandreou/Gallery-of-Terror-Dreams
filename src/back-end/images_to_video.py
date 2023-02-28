import os

import numpy as np
from moviepy.editor import *
from PIL import Image


class Video:
    def __init__(self, size):
        self.size = size

    def shape_changer(self):
        directory = "./images/"

        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                filepath = os.path.join(directory, filename)
                with Image.open(filepath) as img:
                    img = img.resize(self.size)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(filepath)

    def video_creator(self):
        image_dir = "./images/"
        audio_file = "./audio/audio.mp3"
        video_dir = "./video/video.mp4"

        image_files = [f for f in os.listdir(image_dir) if f.endswith(".png")]
        duration = 1.25

        clips = []
        for f in image_files:
            filepath = os.path.join(image_dir, f)
            with Image.open(filepath) as img:
                clips.append(ImageClip(np.array(img)).set_duration(duration))
                clip = VideoFileClip(video_dir).resize(self.size)
                clips.append(clip.set_duration(1.25))

        video_clip = concatenate_videoclips(clips, method="compose")

        audio_clip = AudioFileClip(audio_file).set_duration(video_clip.duration)
        new_audioclip = CompositeAudioClip([audio_clip])
        video_clip = video_clip.set_audio(new_audioclip)
        video_clip.write_videofile("output.mp4", fps=24)


finale = Video((1024, 768))
finale.shape_changer()
finale.video_creator()
