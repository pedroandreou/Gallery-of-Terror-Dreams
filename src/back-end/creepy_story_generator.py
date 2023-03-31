import os
import shutil
from contextlib import suppress
from pathlib import Path

from gpt3.gpt3 import generate_bullet_points_using_gpt3
from dalle2.dalle2 import generate_imgs_using_dalle2
from video_generation.images_to_video import Video
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
IMAGE_DIR = current_path / "dalle2" / "png_images"


@app.post("/create-creepy-story", response_class=JSONResponse, status_code=200)
def create_creepy_story(payload: InputPayload = Body(None)):
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
        bullet_dict = generate_bullet_points_using_gpt3(payload.input_text, payload.openai_key)

        # Generate creepy imgs
        for i, bullet_point in enumerate(bullet_dict):
            generate_imgs_using_dalle2(i, bullet_point["sentence"], payload.openai_key, IMAGE_DIR)

        # # Generate a UUID for the video file
        # video_id = str(uuid.uuid4())

        # Generate output video
        video = Video((1024, 768))
        video.shape_changer()
        video.video_creator()
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


@app.get("/create-creepy-story/videos/{video_id}.mp4")
def serve_video(video_id: str):
    """
    Locate the video file on the server using the video_id
    Read the video file in binary mode
    Set the content type to "video/mp4"
    Return the video bytes to the client
    """

    try:
        # Set the video file path based on whether the code is running in a Docker container or locally
        base_path = (
            Path("/code/src/back-end")
            if os.environ.get("DOCKER_CONTAINER")
            else os.path.dirname(__file__)
        )
        video_file_path = os.path.join(base_path, "video_generation", "videos", f"{video_id}.mp4")

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
