import base64
import os
import re
import string
from pathlib import Path

import nltk
import requests
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image

try:
    nltk.data.find("tokenizers/punkt")
except (LookupError, OSError):
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except (LookupError, OSError):
    nltk.download("stopwords")


current_path = Path(__file__).resolve().parent

# Change the webpage name and icon
web_icon_path = current_path / "images/texas_icon.jpg"
web_icon = Image.open(web_icon_path)
st.set_page_config(
    page_title="Gallery of Terro Dreams",
    page_icon=web_icon,
    initial_sidebar_state="expanded",
)

# Add audio player
audio_file = open(f"{current_path}/audio/exorcist_theme.mp3", "rb")
audio_bytes = audio_file.read()
st.sidebar.audio(audio_bytes, format="audio/mp3", start_time=0)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        img_bytes = f.read()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{base64.b64encode(img_bytes).decode()}');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Add img to the bg
main_bg_path = current_path / "images/main_bg.jpg"
add_bg_from_local(main_bg_path)


def update_warning(chars_left):
    if chars_left > 0:
        st.warning(f"Please enter at least {chars_left} more characters.")
    else:
        st.warning("")


def handle_submit(text):
    """
    Pass the submitted text to back-end
    and show the generated output
    """

    def preprocess_text(text):
        # Remove leading and trailing white space from the text
        text = text.strip()

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Split input string into tokens
        tokens = text.split()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stop words
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if not token in stop_words]

        # Define a regular expression pattern to match special characters
        pattern = r"[^A-Za-z]+"

        # Remove special characters from each token
        clean_tokens = [re.sub(pattern, "", token) for token in tokens]

        preprocessed_text = " ".join(clean_tokens)

        return preprocessed_text

    # Custom CSS style for the spinner
    st.markdown(
        """
        <style>
            .custom-spinner-label {
                font-size: 20px;
                color: red;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="custom-spinner-label">Processing the request...</div>',
        unsafe_allow_html=True,
    )
    try:
        with st.spinner():
            # Generate the video
            base_url = (
                "http://back-end:8000"
                if os.environ.get("DOCKER_CONTAINER")
                else "http://localhost:8000"
            )
            api_url = f"{base_url}/create-creepy-story"
            headers = {"Content-Type": "application/json"}

            data = {
                "input_text": preprocess_text(text),
                "openai_key": st.session_state["api_key"],
            }
            response_data = requests.post(api_url, headers=headers, json=data).json()

            if "error" in response_data:
                error_message = response_data["error"]

                return error_message
            else:
                video_id = response_data["video_id"]

                # Get the generated video
                api_url = f"{base_url}/create-creepy-story/videos/{video_id}.mp4"
                response = requests.get(api_url)

                content_type = response.headers.get("Content-Type")
                if content_type == "application/json":
                    error_message = response.json()["error"]

                    return error_message
                elif content_type == "video/mp4":
                    # Show the video on the ui
                    return response.content

    except requests.exceptions.RequestException as e:
        st.error(f"An unexpected error occured: {e}")


# Initialize session state variables
if "text_input" not in st.session_state:
    st.session_state["text_input"] = ""
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None

# Center the title horizontally
st.markdown(
    "<h1 style='text-align: center; color: red; font-size: 36px; font-weight: bold;'>Gallery of Terror dreams</h1>",
    unsafe_allow_html=True,
)

for _ in range(5):
    st.write("")

# Define custom CSS
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
        .stAlert {
            background-color: black !important;
            color: white !important;
        }
    </style>
"""

# Create input box
st.markdown(text_input_style, unsafe_allow_html=True)
text_input = st.text_area(
    "Enter text here",
    value=st.session_state.get("text_input", ""),
    height=200,
    key="text_input",
    max_chars=1000,
)

col1, col2 = st.columns([3, 1])
col1.write("")
col2.write("")

# Prompt the user for their API key
st.sidebar.subheader("OpenAI API Key")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    type="password",
    value=st.session_state.get("api_key", "")
    if st.session_state.get("api_key") is not None
    else "",
)


# Enable the submit button when both the API key and text input are provided
# Disable the submit button when either the API key or text input is missing
# Special case: Temporarily disable the submit button when it is pressed and enabled
# This prevents the user from sending multiple requests to OpenAI simultaneously
if "submit_executed" not in st.session_state:
    st.session_state["submit_executed"] = False

if "submit_pressed" not in st.session_state:
    st.session_state["submit_pressed"] = False

if "video_output" not in st.session_state:
    st.session_state["video_output"] = None

if api_key and text_input and not st.session_state["submit_pressed"]:
    st.session_state["submit_disabled"] = False
else:
    st.session_state["submit_disabled"] = True

submit_button = col2.button(
    "Submit", disabled=st.session_state["submit_disabled"], key="submit_button"
)

if api_key:
    # Set the API key in session state
    st.session_state["api_key"] = api_key

    # Create a pop-up notification
    st.success("API key set successfully")

# When api key and text were given
if api_key and text_input:
    # Handle the submit button when pressed
    if submit_button:
        # Disable the submit button
        st.session_state["submit_pressed"] = True
        st.session_state["submit_disabled"] = True
        st.experimental_rerun()  # Rerun the script to update the button state

# Call the handle_submit function after the button state has been updated and the button is pressed
if st.session_state["submit_pressed"]:
    st.session_state["submit_pressed"] = False
    st.session_state["video_output"] = handle_submit(text_input)
    st.session_state["submit_executed"] = True
    st.experimental_rerun()  # Rerun the script to enable the button after the function execution

# Display the video output if available
if st.session_state["video_output"]:
    if isinstance(st.session_state["video_output"], str):
        st.error("An error occurred: " + str(st.session_state["video_output"]))
    else:
        st.video(st.session_state["video_output"])
        st.success("Request completed")


# Create the warning placeholder
if "warning_placeholder" not in st.session_state:
    st.session_state["warning_placeholder"] = st.empty()

# Update the warning message using the callback function
chars_left = 30 - len(st.session_state.get("text_input", ""))
update_warning(chars_left)

# Display the hyperlink within the sidebar
st.sidebar.write(
    "If you do not remember your API key, get it from [here](https://platform.openai.com/account/api-keys)"
)

st.sidebar.warning(
    "After making changes to the GUI, be sure to click on the background to ensure that Streamlit updates the interface"
)
