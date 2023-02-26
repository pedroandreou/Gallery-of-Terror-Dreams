import json
import os
import re
import shutil
from base64 import b64decode
from pathlib import Path
from typing import List

import openai
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, BaseSettings, validator


class Settings(BaseSettings):
    OPENAI_API_KEY: str = "OPENAI_API_KEY"

    class Config:
        env_file = ".env_vars"

    @validator("OPENAI_API_KEY")
    def key_must_not_be_empty(cls, value):
        if value:
            return value
        raise ValueError("API key cannot be empty.")


settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


class InputPayload(BaseModel):
    input_text: str


app = FastAPI()


DATA_DIR = Path.cwd() / "responses"
DATA_DIR.mkdir(exist_ok=True)

IMAGE_DIR = Path.cwd() / "images"
DATA_DIR.mkdir(exist_ok=True)


def generate_bullet_points_using_gpt3(text: str):
    def generate_output_dictionary(input: str) -> List[dict]:
        output_list = [
            re.sub(r"^[0-9]+\. ", "", sentence.strip())
            for sentence in input.split("\n")
        ]

        bullet_dict = [
            {"number": i + 1, "sentence": sentence}
            for i, sentence in enumerate(output_list)
        ]

        return bullet_dict

    prompt = f"Generate 2 bullet points that would narrate a horror, creepy, frightening, scaring, terrifying movie from the following text: {text} "

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
    prompt = f"Create a fictional creepy old unexplained story, based on the following description: '{text}'"

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
        response_format="b64_json",
    )
    file_name = DATA_DIR / f"{prompt[:5]}-{response['created']}.json"

    # Save the img as a base64 code in a JSON file
    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
def create_creepy_story(payload: InputPayload = Body(None)):
    # Check if the directory exists and delete it if it does
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(DATA_DIR)

    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)
    os.makedirs(IMAGE_DIR)

    # Generate bullet points
    bullet_dict = generate_bullet_points_using_gpt3(payload.input_text)

    # Generate creepy imgs as basecode64 and add them to JSON files
    for item in bullet_dict:
        generate_imgs_using_dalle2(item["sentence"])

    # Loop through the files in the directory and get their names
    # Then decode the imgs from base64 to a PNG format
    count = 0
    for filename in os.listdir(DATA_DIR):
        JSON_FILE = DATA_DIR / filename

        with open(JSON_FILE, mode="r", encoding="utf-8") as file:
            response = json.load(file)

        for _, image_dict in enumerate(response["data"]):
            image_data = b64decode(image_dict["b64_json"])
            IMAGE_FILE = IMAGE_DIR / f"{JSON_FILE.stem}-{count}.png"
            with open(IMAGE_FILE, mode="wb") as png:
                png.write(image_data)

        count += 1


if __name__ == "__main__":
    import subprocess

    subprocess.Popen(["start", "chrome", "http://127.0.0.1:8000/docs"], shell=True)

    import uvicorn

    uvicorn.run("creepy_story_generator:app", host="0.0.0.0", port=8000, reload=True)
