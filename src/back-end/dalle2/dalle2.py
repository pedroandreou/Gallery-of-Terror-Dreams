from base64 import b64decode
from pathlib import Path

import openai


def generate_imgs_using_dalle2(count: int, text: str, api_key: str, image_dir: Path):
    openai.api_key = api_key

    prompt = f"Take a spooky photo using camera settings like the SONY A60, with an f/1.5 aperture, that clearly displays the following scary story, inspired by the creepy mood of The Exorcist: {text}"

    response = openai.Image.create(
        prompt=prompt,
        n=2,  # Generate 2 images
        size="256x256",
        response_format="b64_json",
    )

    # Construct the file path for the image file
    file_path = image_dir / f"best_{count}.png"

    for i, image_dict in enumerate(response["data"]):
        # Save only the second photo's JSON as a PNG
        # since the second generation is usually better
        # than the first one
        if i == 1:
            image_data = b64decode(image_dict["b64_json"])

            with open(file_path, mode="wb") as png:
                png.write(image_data)
