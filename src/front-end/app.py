import base64
import os

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

    data = {"input_text": text, "openai_key": st.session_state["api_key"]}

    try:
        response = requests.post(
            "http://back-end:8000/create-creepy-story", headers=headers, json=data
        ).json()

        video_url = response["video_url"]

        response = requests.get(video_url)
        st.video(response.content)
    except requests.exceptions.RequestException as e:
        st.write(f"Error: {e}")


def main():
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
    for _ in range(5):
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
    st.markdown(text_input_style, unsafe_allow_html=True)
    text_input = st.text_area("Enter text here", value="", height=200, key="text_input")

    col1, col2 = st.columns([3, 1])
    col1.write("")
    col2.write("")
    submit_button = col2.button("Submit")

    # When button is pressed, handle text submission
    if submit_button:
        handle_submit(text_input)

    # Initialize session state
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = None

    # Prompt the user for their API key
    st.sidebar.subheader("OpenAI API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if api_key:
        # Set the API key in session state
        st.session_state["api_key"] = api_key

        # Create a pop-up notification
        st.success("API key set successfully")


if __name__ == "__main__":
    main()
