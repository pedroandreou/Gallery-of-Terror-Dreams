import subprocess

import streamlit as st


def handle_submit(text):
    """
    Handle text submission
    """
    st.write(f"Text submitted: {text}")


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
        "--server.port=8000",
        "--browser.gatherUsageStats=false",
        "--server.enableCORS=false",
    ]
    subprocess.run(cmd)
