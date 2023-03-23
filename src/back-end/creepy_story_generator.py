import json
import os
import re
import shutil
from base64 import b64decode
from pathlib import Path
from typing import List

import images_to_video
import openai
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel


class InputPayload(BaseModel):
    input_text: str
    openai_key: str


app = FastAPI()

current_path = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(current_path, "base64_code")
if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)  # Delete the directory and its contents
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

IMAGE_DIR = os.path.join(current_path, "png_images")
if os.path.exists(IMAGE_DIR):
    shutil.rmtree(IMAGE_DIR)  # Delete the directory and its contents
Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)


def generate_bullet_points_using_gpt3(text: str):
    def generate_output_dictionary(input_str: str) -> List[dict]:
        output_list = [
            re.sub(r"^[0-9]+\. ", "", s.strip()) for s in input_str.split("\n") if s
        ]

        bullet_dict = [
            {"number": i + 1, "sentence": sentence}
            for i, sentence in enumerate(output_list)
        ]

        return bullet_dict

    prompt = f"Generate 5 bullet points that would narrate an analog unsettling horror style movie from the following text: {text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=2,
        stop=None,
        temperature=0.5,
    )

    bullet_dict = generate_output_dictionary(response.choices[0].text.lstrip())

    return bullet_dict


def generate_imgs_using_dalle2(text: str):
    prompt = f"Create an analog horror unsettling style movie of '{text}'"

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        response_format="b64_json",
    )

    # Construct the file path for the image file
    file_path = os.path.join(DATA_DIR, f"{prompt[:5]}-{response['created']}.json")

    # Save the image as a base64 code in a JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(response, f)


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
def create_creepy_story(payload: InputPayload = Body(None)):
    # Set the API key as a global variable
    openai.api_key = payload.openai_key

    # Check if directories exist and delete them if they do
    for dir_path in (DATA_DIR, IMAGE_DIR):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        os.makedirs(dir_path)

    # Generate bullet points
    bullet_dict = generate_bullet_points_using_gpt3(payload.input_text)

    # Generate creepy imgs as basecode64 and add them to JSON files
    for bullet_point in bullet_dict:
        generate_imgs_using_dalle2(bullet_point["sentence"])

    # Loop through the files in the directory and get their names
    # Then decode the imgs from base64 to a PNG format
    count = 0
    for filename in os.listdir(DATA_DIR):
        JSON_FILE = Path(DATA_DIR) / filename

        with open(JSON_FILE, mode="r", encoding="utf-8") as file:
            response = json.load(file)

        for _, image_dict in enumerate(response["data"]):
            image_data = b64decode(image_dict["b64_json"])
            IMAGE_FILE = Path(IMAGE_DIR) / f"{JSON_FILE.stem}-{count}.png"
            with open(IMAGE_FILE, mode="wb") as png:
                png.write(image_data)

        count += 1

    # Generate output video
    finale = images_to_video.Video((1024, 768))
    finale.shape_changer()
    finale.video_creator()

    # Set the video URL based on whether the code is running in a Docker container or locally
    video_url = (
        "http://back-end:8000/create-creepy-story/videos/final_video.mp4"
        if os.environ.get("DOCKER_CONTAINER")
        else "http://localhost:8000/create-creepy-story/videos/final_video.mp4"
    )

    # Return the URL of the created video
    return {"video_url": video_url}


@app.get("/create-creepy-story/videos/final_video.mp4")
async def serve_video():
    # Set the video file path based on whether the code is running in a Docker container or locally
    video_file_path = (
        "/code/src/back-end/videos/final_video.mp4"
        if os.environ.get("DOCKER_CONTAINER")
        else os.path.join(os.path.dirname(__file__), "videos", "final_video.mp4")
    )

    # Open the video file in binary mode
    with open(video_file_path, "rb") as video_file:
        # Read the video file
        video_bytes = video_file.read()

    # Set the video content type
    headers = {"Content-Type": "video/mp4"}

    # Return the video bytes and set the content type
    return Response(video_bytes, headers=headers)
