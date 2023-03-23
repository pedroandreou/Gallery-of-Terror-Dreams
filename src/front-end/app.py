import base64
import os
import string
from urllib.parse import urljoin

import nltk
import requests
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image

nltk.download("stopwords")
nltk.download("punkt")


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

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Convert to lowercase
        text = text.lower()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stop words
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if not token in stop_words]

        # Remove special characters
        tokens = [token.encode("ascii", "ignore").decode("utf-8") for token in tokens]

        # Join the tokens back into a string
        preprocessed_text = " ".join(tokens)

        return preprocessed_text

    # Make a request to the backend API
    headers = {"Content-Type": "application/json"}

    api_url = (
        urljoin("http://back-end:8000/", "create-creepy-story")
        if os.environ.get("DOCKER_CONTAINER")
        else "http://localhost:8000/create-creepy-story"
    )
    data = {
        "input_text": preprocess_text(text),
        "openai_key": st.session_state["api_key"],
    }

    try:
        video_url = requests.post(api_url, headers=headers, json=data).json()[
            "video_url"
        ]

        response = requests.get(video_url)
        st.video(response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")


def main():
    current_path = os.path.dirname(__file__)

    # Change the webpage name and icon
    web_icon = Image.open(os.path.join(current_path, "images/texas_icon.jpg"))
    st.set_page_config(page_title="Gallery of Terro Dreams", page_icon=web_icon)

    # Add img to the bg
    main_bg_path = os.path.join(current_path, "images/main_bg.jpg")
    add_bg_from_local(main_bg_path)

    # Initialize session state variables
    if "text_input" not in st.session_state:
        st.session_state["text_input"] = ""
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = None
    if "submit_disabled" not in st.session_state:
        st.session_state["submit_disabled"] = True

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

    # Create input box and submit button
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

    submit_disabled = not (api_key and text_input)
    submit_button = col2.button("Submit", disabled=submit_disabled)

    if api_key:
        # Set the API key in session state
        st.session_state["api_key"] = api_key

        # Create a pop-up notification
        st.success("API key set successfully")

        # Enable/disable submit button based on input text
        submit_disabled = not text_input
        st.session_state["submit_disabled"] = submit_disabled

    # When api key and text were given
    if api_key and text_input:
        # Handle the submit button when pressed
        if submit_button:
            handle_submit(text_input)

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


if __name__ == "__main__":
    main()
