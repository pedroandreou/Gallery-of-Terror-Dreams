import base64
import os

import requests
import streamlit as st
from PIL import Image


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
    # Make a request to the backend API
    headers = {"Content-Type": "application/json"}

    data = {"input_text": text, "openai_key": st.session_state["api_key"]}

    try:
        response = requests.post(
            "http://localhost:8000/create-creepy-story", headers=headers, json=data
        ).json()

        video_url = response["video_url"]

        response = requests.get(video_url)
        st.video(response.content)
    except Exception as e:
        st.error(f"The provided OpenAI API key is invalid or incorrect")


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
        value=st.session_state["text_input"],
        height=200,
        key="text_input",
        max_chars=1000,
    )

    col1, col2 = st.columns([3, 1])
    col1.write("")
    col2.write("")

    submit_disabled = len(text_input) < 30 or st.session_state["submit_disabled"]
    submit_button = col2.button("Submit", disabled=submit_disabled)

    # When api key and text were given
    if st.session_state["api_key"] and text_input:
        # Handle the submit button when pressed
        if submit_button:
            handle_submit(text_input)

    # Prompt the user for their API key
    st.sidebar.subheader("OpenAI API Key")
    api_key = st.sidebar.text_input(
        "Enter your OpenAI API key", type="password", value=st.session_state["api_key"]
    )
    if api_key:
        # Set the API key in session state
        st.session_state["api_key"] = api_key

        # Create a pop-up notification
        st.success("API key set successfully")

        # Enable the submit button
        st.session_state["submit_disabled"] = False

    # Store the values in session state if they have changed
    if text_input != st.session_state["text_input"]:
        st.session_state["text_input"] = text_input

    # Create the warning placeholder
    if "warning_placeholder" not in st.session_state:
        st.session_state["warning_placeholder"] = st.empty()

    # Update the warning message using the callback function
    chars_left = 30 - len(st.session_state["text_input"])
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
