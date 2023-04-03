from typing import List

import openai


def generate_bullet_points_using_gpt3(text: str, openai_key: str):
    def generate_output_dictionary(text: str) -> List[str]:
        # Remove leading whitespaces
        lines = [line.lstrip() for line in text.splitlines()]

        # Get the text after the first whitespace
        # e.g. "1. Hi there" => "Hi there"
        text_list = [line.split(" ", 1)[1] for line in lines]

        bullet_dict = [
            {"number": i + 1, "sentence": sentence}
            for i, sentence in enumerate(text_list)
        ]

        return bullet_dict

    prompt = f"Generate five sentences to narrate a horror story of: {text}\n1."

    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.6,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.72,
        presence_penalty=0.72,
    )

    output = "1. " + response.choices[0].message.content.lstrip()

    bullet_points = generate_output_dictionary(output)

    return bullet_points
