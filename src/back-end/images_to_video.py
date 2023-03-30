from pathlib import Path

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
        self.current_path = Path(__file__).parent.absolute()
        self.image_dir = self.current_path / "png_images"
        self.audio_file = self.current_path / "audio" / "texas_trailer.mp3"
        self.flash_video_file = self.current_path / "videos" / "flash_video.mp4"
        self.final_video_file = self.current_path / "videos" / "final_video.mp4"

    def shape_changer(self):
        for filepath in Path(self.image_dir).glob('*.png'):
            with Image.open(filepath) as img:
                img = img.resize(self.size)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(filepath)

    def video_creator(self):
        image_files = [f for f in Path(self.image_dir).iterdir() if str(f).endswith(".png")]
        duration = 1.25

        clips = []
        for f in image_files:
            with Image.open(f) as img:
                clips.append(ImageClip(np.array(img)).set_duration(duration))
                clip = VideoFileClip(str(self.flash_video_file)).resize(self.size)
                clips.append(clip.set_duration(1.25))

        video_clip = concatenate_videoclips(clips, method="compose")

        audio_clip = AudioFileClip(str(self.audio_file)).set_duration(video_clip.duration)
        new_audioclip = CompositeAudioClip([audio_clip])
        video_clip = video_clip.set_audio(new_audioclip)
        video_clip.write_videofile(str(self.final_video_file), fps=24)
