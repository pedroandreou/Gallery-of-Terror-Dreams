import os

import numpy as np
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)
from PIL import Image


class Video:
    def __init__(self, size):
        self.size = size
        self.current_path = current_path = os.path.dirname(os.path.abspath(__file__))
        self.image_dir = os.path.join(current_path, "png_images/")
        self.audio_file = os.path.join(current_path, "audio/audio.mp3")
        self.flash_video_file = os.path.join(current_path, "videos/flash_video.mp4")
        self.final_video_file = os.path.join(current_path, "videos/final_video.mp4")

    def shape_changer(self):
        for filename in os.listdir(self.image_dir):
            if filename.endswith(".png"):
                filepath = os.path.join(self.image_dir, filename)
                with Image.open(filepath) as img:
                    img = img.resize(self.size)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(filepath)

    def video_creator(self):
        image_files = [f for f in os.listdir(self.image_dir) if f.endswith(".png")]
        duration = 1.25

        clips = []
        for f in image_files:
            filepath = os.path.join(self.image_dir, f)
            with Image.open(filepath) as img:
                clips.append(ImageClip(np.array(img)).set_duration(duration))
                clip = VideoFileClip(self.flash_video_file).resize(self.size)
                clips.append(clip.set_duration(1.25))

        video_clip = concatenate_videoclips(clips, method="compose")

        audio_clip = AudioFileClip(self.audio_file).set_duration(video_clip.duration)
        new_audioclip = CompositeAudioClip([audio_clip])
        video_clip = video_clip.set_audio(new_audioclip)
        video_clip.write_videofile(self.final_video_file, fps=24)
