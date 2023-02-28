import base64
import os
import subprocess

import requests
import streamlit as st


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def handle_submit(text):
    """
    Pass the submitted text to back-end
    and show the generated output
    """
    # Make a request to the backend API
    headers = {"Content-Type": "application/json"}

    data = {"input_text": text}

    try:
        response = requests.post(
            "http://localhost:8000/create-creepy-story", headers=headers, json=data
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.write(f"Error: {e}")
        st.write(f"Response content: {e.response.content}")

    # Get the absolute path of the current directory
    current_path = os.path.abspath(os.path.dirname(__file__))

    # Get the absolute path of the parent directory
    parent_path = os.path.abspath(os.path.join(current_path, ".."))

    video_file = open(f"{parent_path}/back-end/output.mp4", "rb")
    video_bytes = video_file.read()

    st.video(video_bytes)


# Add img to the bg
current_dir = os.path.abspath(os.path.dirname(__file__))
background_url = f"{current_dir}/imgs/bg.jpg".replace("\\", "/")
add_bg_from_local(background_url)


# Center the container horizontally
st.markdown(
    "<h1 style='text-align: center; color: red; font-size: 36px; font-weight: bold;'>Gallery of Terror dreams</h1>",
    unsafe_allow_html=True,
)

# Leave empty space
for i in range(5):
    st.write("")


# Define custom CSS for the text area
text_input_style = """
    <style>
        div[data-baseweb="textarea"] textarea {
            background-color: black;
            color: white;
        }
        .stButton button {
            background-color: black;
            color: white;
            margin-left: 10px;
        }
    </style>
"""

# Create input box and submit button
container = st.container()
st.markdown(text_input_style, unsafe_allow_html=True)
text_input = st.text_area("Enter text here", value="", height=200, key="text_input")

col1, col2 = st.columns([3, 1])
col1.write("")
col2.write("")
submit_button = col2.button("Submit")

# When button is pressed, handle text submission
if submit_button:
    handle_submit(text_input)


# Define custom CSS for the layout
layout_style = """
    <style>
        .main .block-container {
            width: 50%;
            margin: auto;
        }
    </style>
"""

st.markdown(layout_style, unsafe_allow_html=True)


if __name__ == "__main__":
    cmd = [
        "streamlit",
        "run",
        "app.py",
        "--server.port=8501",  # Change the port number to 8501
        "--browser.gatherUsageStats=false",
    ]
    subprocess.run(cmd)
