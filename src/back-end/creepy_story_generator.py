import os
import re
import shutil
from base64 import b64decode
from contextlib import suppress
from pathlib import Path
from typing import List

import images_to_video
import openai
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

# import uuid


class InputPayload(BaseModel):
    input_text: str
    openai_key: str


app = FastAPI()


current_path = Path(__file__).resolve().parent
IMAGE_DIR = current_path / "png_images"


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

    prompt = f"Generate five bullet points to narrate a horror story of: {text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=2,
        stop=None,
        top_p=1,
        temperature=0.4,
    )

    bullet_dict = generate_output_dictionary(response.choices[0].text.lstrip())

    return bullet_dict


def generate_imgs_using_dalle2(count: int, text: str):
    prompt = f"Create an unsettling analog horror story for: {text}"

    response = openai.Image.create(
        prompt=prompt,
        n=3,  # Generate 3 images
        size="256x256",
        response_format="b64_json",
    )

    # Construct the file path for the image file
    file_path = Path(IMAGE_DIR) / f"best_{count}.png"

    for i, image_dict in enumerate(response["data"]):
        # Save only the third photo's JSON as a PNG
        # since the third generation is usually better
        # than the previous two
        if i == 2:
            image_data = b64decode(image_dict["b64_json"])

            with open(file_path, mode="wb") as png:
                png.write(image_data)


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
async def create_creepy_story(payload: InputPayload = Body(None)):
    """
    Process the data and generate the video file
    Save the video file on the server with a unique name or identifier
    Return the unique identifier to the client
    """

    try:
        # Set the API key as a global variable
        openai.api_key = payload.openai_key

        # Check if directory exists and delete it if it does
        with suppress(FileNotFoundError):
            shutil.rmtree(IMAGE_DIR)
        Path(IMAGE_DIR).mkdir(parents=True)

        # Generate bullet points
        bullet_dict = generate_bullet_points_using_gpt3(payload.input_text)

        # Generate creepy imgs
        for i, bullet_point in enumerate(bullet_dict):
            generate_imgs_using_dalle2(i, bullet_point["sentence"])

        # # Generate a UUID for the video file
        # video_id = str(uuid.uuid4())

        # Generate output video
        finale = images_to_video.Video((1024, 768))
        finale.shape_changer()
        finale.video_creator()
    except openai.error.Timeout as e:
        return {"error": f"OpenAI API request timed out: {e}"}
    except openai.error.APIError as e:
        return {"error": f"OpenAI API returned an API Error: {e}"}
    except openai.error.APIConnectionError as e:
        return {"error": f"OpenAI API request failed to connect: {e}"}
    except openai.error.InvalidRequestError as e:
        return {"error": f"OpenAI API request was invalid: {e}"}
    except openai.error.AuthenticationError as e:
        return {"error": f"OpenAI API request was not authorized: {e}"}
    except openai.error.PermissionError as e:
        return {"error": f"OpenAI API request was not permitted: {e}"}
    except openai.error.RateLimitError as e:
        return {"error": f"OpenAI API request exceeded rate limit: {e}"}
    except openai.error.ServiceUnavailableError:
        return {"error": f"Issue on OpenAI's servers:{e}"}

    return {"video_id": "final_video"}


@app.get("/create-creepy-story/videos/{video_id}")
async def serve_video(video_id: str):
    """
    Locate the video file on the server using the video_id
    Read the video file in binary mode
    Set the content type to "video/mp4"
    Return the video bytes to the client
    """

    try:
        # Set the video file path based on whether the code is running in a Docker container or locally
        base_path = (
            "/code/src/back-end"
            if os.environ.get("DOCKER_CONTAINER")
            else os.path.dirname(__file__)
        )
        video_file_path = os.path.join(base_path, "videos", video_id)

        # Open the video file in binary mode
        with open(video_file_path, "rb") as video_file:
            # Read the video file
            video_bytes = video_file.read()
    except openai.error.Timeout as e:
        return {"error": f"OpenAI API request timed out: {e}"}
    except openai.error.APIError as e:
        return {"error": f"OpenAI API returned an API Error: {e}"}
    except openai.error.APIConnectionError as e:
        return {"error": f"OpenAI API request failed to connect: {e}"}
    except openai.error.InvalidRequestError as e:
        return {"error": f"OpenAI API request was invalid: {e}"}
    except openai.error.AuthenticationError as e:
        return {"error": f"OpenAI API request was not authorized: {e}"}
    except openai.error.PermissionError as e:
        return {"error": f"OpenAI API request was not permitted: {e}"}
    except openai.error.RateLimitError as e:
        return {"error": f"OpenAI API request exceeded rate limit: {e}"}
    except openai.error.ServiceUnavailableError:
        return {"error": f"Issue on OpenAI's servers:{e}"}

    headers = {"Content-Type": "video/mp4"}

    return Response(video_bytes, headers=headers)
