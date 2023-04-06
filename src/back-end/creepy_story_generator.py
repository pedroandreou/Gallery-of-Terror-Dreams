import os
import shutil
from contextlib import suppress
from functools import wraps
from pathlib import Path

import openai
from chatgpt.chatgpt import generate_bullet_points_using_chatgpt
from dalle2.dalle2 import generate_imgs_using_dalle2
from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from video_generation.images_to_video import Video

# import uuid


class InputPayload(BaseModel):
    input_text: str
    openai_key: str


app = FastAPI()


CURR_PATH = Path(__file__).resolve().parent
IMAGE_DIR = CURR_PATH / "dalle2" / "png_images"


def handle_openai_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
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

    return wrapper


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
@handle_openai_exceptions
def create_creepy_story(payload: InputPayload = Body(None)):
    """
    Process the data and generate the video file
    Save the video file on the server with a unique name or identifier
    Return the unique identifier to the client
    """

    # Set the API key as a global variable
    openai.api_key = payload.openai_key

    # Check if directory exists and delete it if it does
    with suppress(FileNotFoundError):
        shutil.rmtree(IMAGE_DIR)
    Path(IMAGE_DIR).mkdir(parents=True)

    # Generate bullet points
    bullet_dict = generate_bullet_points_using_chatgpt(
        payload.input_text, payload.openai_key
    )

    # Generate creepy imgs
    for i, bullet_point in enumerate(bullet_dict):
        generate_imgs_using_dalle2(
            i, bullet_point["sentence"], payload.openai_key, IMAGE_DIR
        )

    # # Generate a UUID for the video file
    # video_id = str(uuid.uuid4())
    video_id = "final_video"

    # Generate output video
    video = Video((1024, 768), video_id, IMAGE_DIR)
    video.shape_changer()
    video.video_creator()

    return {"video_id": video_id}


@app.get("/create-creepy-story/videos/{video_id}.mp4")
@handle_openai_exceptions
def serve_video(video_id: str):
    """
    Locate the video file on the server using the video_id
    Read the video file in binary mode
    Set the content type to "video/mp4"
    Return the video bytes to the client
    """

    # Set the video file path based on whether the code is running in a Docker container or locally
    base_path = (
        Path("/app")
        if os.environ.get("KUBERNETES_CLUSTER") == "True"
        or os.environ.get("DOCKER_CONTAINER")
        else CURR_PATH
    )
    video_file_path = os.path.join(
        base_path, "video_generation", "videos", f"{video_id}.mp4"
    )

    # Open the video file in binary mode
    with open(video_file_path, "rb") as video_file:
        # Read the video file
        video_bytes = video_file.read()

    headers = {"Content-Type": "video/mp4"}

    return Response(video_bytes, headers=headers)
