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


DATA_DIR = Path.cwd() / "dir_of_creepy_imgs_saved_as_json"
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

    prompt = f"Generate 10 bullet points that would narrate a horror, creepy, frightening, scaring, terrifying movie from the following text: {text} "

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
    prompt = f"Creepy old unexplained photo of '{text}'"

    response = openai.Image.create(
        prompt=prompt,
        n=2,
        size="256x256",
        response_format="b64_json",
    )
    file_name = DATA_DIR / f"{prompt[:5]}-{response['created']}.json"

    # Save the img as a base64 code in a JSON file
    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    IMAGE_DIR = Path.cwd() / "images" / file_name.stem
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Convert the JSON file to a PNG img
    with open(file_name, mode="r", encoding="utf-8") as file:
        response = json.load(file)

    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{file_name.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
def create_creepy_story(payload: InputPayload = Body(None)):
    # Check if the directory exists before deleting it
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)

    # Generate bullet points
    bullet_dict = generate_bullet_points_using_gpt3(payload.input_text)

    # Generate creepy imgs
    for item in bullet_dict:
        generate_imgs_using_dalle2(item["sentence"])


if __name__ == "__main__":
    import subprocess

    subprocess.Popen(["start", "chrome", "http://127.0.0.1:8000/docs"], shell=True)

    import uvicorn

    uvicorn.run("creepy_story_generator:app", host="0.0.0.0", port=8000, reload=True)
