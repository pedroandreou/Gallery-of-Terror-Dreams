import re
from typing import List

import openai
from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
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


class OutputItem(BaseModel):
    number: int
    sentence: str


class OutputPayload(BaseModel):
    sentences: List[OutputItem]


app = FastAPI()


@app.post("/generate-bullet-points", response_class=JSONResponse, status_code=200)
def generate_bullet_points(payload: InputPayload = Body(None)):
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

    # Define the GPT-3 prompt
    prompt = f"Generate 10 bullet points that would narrate a horror, creepy, frightening, scaring, terrifying movie from the following text: {payload.input_text} "

    # Use OpenAI's GPT-3 API to generate the bullet points
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=10,
        stop=None,
        temperature=0.5,
    )
    bullet_dict = generate_output_dictionary(response.choices[0].text.lstrip())

    # Convert dict to BaseModel
    output_payload = OutputPayload(sentences=bullet_dict)

    return JSONResponse(content=jsonable_encoder(output_payload))


if __name__ == "__main__":
    import subprocess

    subprocess.Popen(["start", "chrome", "http://127.0.0.1:8000/docs"], shell=True)

    import uvicorn

    uvicorn.run("gpt3:app", host="0.0.0.0", port=8000, reload=True)
