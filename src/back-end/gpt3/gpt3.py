import re
from typing import List

import openai


def generate_bullet_points_using_gpt3(text: str, openai_key: str):
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

    openai.api_key = openai_key
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
