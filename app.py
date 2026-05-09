import streamlit as st
from PIL import Image
from transformers import pipeline
import random
import re
import numpy as np

# Set up the Streamlit page.
st.set_page_config(
    page_title="Text to Audio Story",
    page_icon="🌟",
    layout="wide"
)

DOG_SVG = """
<svg width="100%" height="100%" viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet">
    <path d="M55 95 C35 80, 35 45, 65 42 C75 20, 115 20, 125 42 C155 45, 160 80, 140 95" 
          fill="#FFF7E6" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M63 45 C48 50, 43 68, 50 85" fill="none" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M125 45 C145 50, 150 70, 140 88" fill="none" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <circle cx="78" cy="78" r="6" fill="#333333"/>
    <circle cx="118" cy="78" r="6" fill="#333333"/>
    <path d="M93 95 Q100 102 107 95" fill="none" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M100 88 L100 100" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <circle cx="100" cy="88" r="6" fill="#333333"/>
    <path d="M72 120 C65 150, 135 150, 128 120" fill="#FFF7E6" stroke="#333333" stroke-width="5"/>
    <path d="M75 145 L70 170" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M125 145 L130 170" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M65 170 L78 170" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
    <path d="M122 170 L135 170" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
</svg>
"""

# Add child-friendly CSS styles.
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(
            90deg,
            #FFF1F6 0%,
            #FFF7FB 12%,
            #FFFDF2 28%,
            #FFFDF2 72%,
            #FFF7FB 88%,
            #FFF1F6 100%
        );
    }}

    .block-container {{
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }}

    h1 {{
        text-align: center;
        color: #2F3142;
        font-size: 48px;
        font-weight: 800;
    }}

    h2, h3 {{
        color: #4B7BEC;
    }}

    .stButton > button {{
        width: 100%;
        height: 68px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 25px;
        background-color: #FFCE54;
        color: #333333;
        border: 4px solid #F6B93B;
        box-shadow: 0 5px 0 #D99B24;
    }}

    .stButton > button:hover {{
        background-color: #FFD966;
        color: #000000;
        border: 4px solid #E58E26;
        transform: scale(1.01);
    }}

    .story-box {{
        background-color: #E8F8F5;
        padding: 24px;
        border-radius: 24px;
        border: 4px solid #55E6C1;
        font-size: 22px;
        line-height: 1.7;
        color: #2C3A47;
    }}

    .caption-box {{
        background-color: #FDEBD0;
        padding: 18px;
        border-radius: 18px;
        border: 3px solid #F5B041;
        font-size: 19px;
        color: #2C3A47;
    }}

    .tip-box {{
        background-color: #FCE4EC;
        padding: 20px;
        border-radius: 22px;
        border: 3px solid #F8A5C2;
        font-size: 19px;
        color: #2C3A47;
        line-height: 1.7;
        text-align: center;
    }}

    .step-box {{
        background-color: #E8F8F5;
        padding: 14px;
        border-radius: 16px;
        border: 2px solid #55E6C1;
        font-size: 18px;
        color: #2C3A47;
        text-align: center;
        margin-top: 18px;
        margin-bottom: 18px;
    }}

    .next-box {{
        background-color: #FFF7E6;
        padding: 18px;
        border-radius: 18px;
        border: 3px solid #F7D794;
        font-size: 20px;
        color: #2C3A47;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 18px;
    }}

    .dog-left, .dog-right {{
        position: fixed;
        top: 150px;
        width: 130px;
        height: 130px;
        max-width: 130px;
        max-height: 130px;
        opacity: 0.95;
        z-index: 1;
        overflow: hidden;
        pointer-events: none;
    }}

    .dog-left svg, .dog-right svg {{
        width: 130px !important;
        height: 130px !important;
        max-width: 130px !important;
        max-height: 130px !important;
        display: block;
    }}

    .dog-left {{
        left: 25px;
    }}

    .dog-right {{
        right: 25px;
    }}

    .paw-left, .paw-right {{
        position: fixed;
        bottom: 40px;
        font-size: 32px;
        line-height: 1.8;
        z-index: 1;
        pointer-events: none;
    }}

    .paw-left {{
        left: 48px;
    }}

    .paw-right {{
        right: 48px;
    }}

    .top-line, .footer-line {{
        text-align: center;
        font-size: 30px;
        margin-bottom: 8px;
    }}

    .footer-line {{
        font-size: 28px;
        margin-top: 25px;
    }}

    @media screen and (max-width: 1000px) {{
        .dog-left, .dog-right, .paw-left, .paw-right {{
            display: none;
        }}

        .block-container {{
            margin-top: 0px;
            border-radius: 18px;
        }}

        h1 {{
            font-size: 36px;
        }}
    }}
    </style>

    <div class="dog-left">{DOG_SVG}</div>
    <div class="dog-right">{DOG_SVG}</div>
    <div class="paw-left">🐾<br>🐾<br>🐾</div>
    <div class="paw-right">🐾<br>🐾<br>🐾</div>
    """,
    unsafe_allow_html=True
)

# Load the image captioning model.
@st.cache_resource
def load_captioning_model():
    return pipeline(
        "image-to-text",
        model="Salesforce/blip-image-captioning-base"
    )

# Load the text-to-audio model.
@st.cache_resource
def load_audio_generator():
    return pipeline(
        "text-to-audio",
        model="Matthijs/mms-tts-eng"
    )

# Open and validate the uploaded image.
def open_uploaded_image(uploaded_file):
    try:
        return Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("Oops! 😢 This file does not look like a valid image. Please upload a JPG or PNG picture.")
        return None

# Generate a caption from the uploaded image.
def generate_caption(image, captioning_model):
    result = captioning_model(image)

    if result and isinstance(result, list):
        caption = result[0].get("generated_text", "").strip()
        return caption or "a lovely scene"

    return "a lovely scene"

# Format the caption for display or story text.
def format_caption(caption, capitalize=False):
    caption = (caption or "a lovely scene").strip()
    first_letter = caption[0].upper() if capitalize else caption[0].lower()
    return first_letter + caption[1:]

# Create a story based on the image caption.
def generate_story_from_caption(caption):
    scene = format_caption(caption, capitalize=False)

    opening = random.choice([
        "One sunny morning",
        "On a bright and cheerful day",
        "Once upon a time",
        "One peaceful afternoon"
    ])

    action = random.choice([
        "something special began to happen",
        "a tiny surprise appeared nearby",
        "a gentle adventure quietly began",
        "a happy little moment started to grow"
    ])

    helper = random.choice([
        "a kind friend came along to help",
        "a cheerful helper joined the adventure",
        "a friendly voice said, 'Let's explore together'",
        "a new friend arrived with a big smile"
    ])

    lesson = random.choice([
        "kindness can make every day brighter",
        "small adventures can become wonderful memories",
        "curiosity can lead to happy discoveries",
        "sharing joy can make everyone smile"
    ])

    return (
        f"{opening}, {scene} became the start of a magical adventure. "
        f"Soon, {action}. "
        f"Then {helper}, and they explored the world with brave hearts and happy smiles. "
        f"By the end of the day, everyone learned that {lesson}. "
        "They returned home feeling proud, safe, and full of joy."
    )

# Split the story into sentences for clearer audio pauses.
def split_story_into_sentences(story):
    return [
        sentence.strip()
        for sentence in re.split(r'(?<=[.!?])\s+', story.strip())
        if sentence.strip()
    ]

# Create silence with the same shape as the audio.
def create_silence_like_audio(audio_array, sample_rate, seconds=0.85):
    silence_length = int(sample_rate * seconds)

    if audio_array.ndim == 1:
        return np.zeros(silence_length, dtype=audio_array.dtype)

    if audio_array.ndim == 2 and audio_array.shape[0] <= audio_array.shape[1]:
        return np.zeros((audio_array.shape[0], silence_length), dtype=audio_array.dtype)

    if audio_array.ndim == 2:
        return np.zeros((silence_length, audio_array.shape[1]), dtype=audio_array.dtype)

    return np.zeros(silence_length, dtype=np.float32)

# Convert the story into audio with clearer pauses.
def generate_audio(story, audio_generator):
    audio_parts = []
    sample_rate = None

    for sentence in split_story_into_sentences(story):
        speech_output = audio_generator(sentence)
        audio_array = np.asarray(speech_output["audio"])
        sample_rate = speech_output["sampling_rate"]

        audio_parts.append(audio_array)
        audio_parts.append(create_silence_like_audio(audio_array, sample_rate))

    first_audio = audio_parts[0]
    axis = 1 if first_audio.ndim == 2 and first_audio.shape[0] <= first_audio.shape[1] else 0

    return np.concatenate(audio_parts, axis=axis), sample_rate

# Initialize session state.
def initialize_state():
    defaults = {
        "caption": "",
        "story": "",
        "audio_array": None,
        "sample_rate": None,
        "has_result": False,
        "is_generating": False
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

# Clear generated results from session state.
def clear_results():
    st.session_state.update({
        "caption": "",
        "story": "",
        "audio_array": None,
        "sample_rate": None,
        "has_result": False,
        "is_generating": False
    })

# Save generated results in session state.
def save_results(caption, story, audio_array, sample_rate):
    st.session_state.update({
        "caption": caption,
        "story": story,
        "audio_array": audio_array,
        "sample_rate": sample_rate,
        "has_result": True,
        "is_generating": False
    })

# Generate caption, story, and audio.
def create_story_and_audio(image):
    st.session_state["is_generating"] = True

    with st.spinner("Loading magic tools... 🪄✨"):
        captioning_model = load_captioning_model()
        audio_generator = load_audio_generator()

    with st.spinner("Reading the image... 👀📷"):
        caption = generate_caption(image, captioning_model)

    with st.spinner("Making your story... 📖✨"):
        story = generate_story_from_caption(caption)

    with st.spinner("Making the audio... 🔊🎵"):
        audio_array, sample_rate = generate_audio(story, audio_generator)

    save_results(caption, story, audio_array, sample_rate)

# Display generated caption, story, and audio.
def display_results():
    st.markdown("### 🖼️ What I See in Your Picture")
    st.markdown(
        f"""
        <div class="caption-box">
        {format_caption(st.session_state["caption"], capitalize=True)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📖 Your Magical Story")
    st.markdown(
        f"""
        <div class="story-box">
        {st.session_state["story"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔊 Listen to Your Story")
    st.audio(
        st.session_state["audio_array"],
        sample_rate=st.session_state["sample_rate"]
    )

# Run the main Streamlit app.
def main():
    initialize_state()

    st.markdown('<div class="top-line">📷 📖 🔊</div>', unsafe_allow_html=True)
    st.title("Turn Your Picture into an Audio Story")

    st.markdown(
        """
        <div class="tip-box">
        👋 Welcome to the storytelling app!<br>
        Upload a picture, and the app will create a short story based on what it sees. 📷✨<br>
        You can also listen to the story with audio. 📖🔊
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="step-box">
        1️⃣ Upload a picture → 2️⃣ Make a story → 3️⃣ Listen and enjoy
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a picture for your story:",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        clear_results()
        st.info("Please upload a picture first. Your story will appear here after the image is uploaded. ✨")
        return

    image = open_uploaded_image(uploaded_file)

    if image is None:
        return

    st.image(image, caption="Uploaded picture 🖼️", use_container_width=True)

    if st.button("✨ Make My Story! ✨"):
        try:
            create_story_and_audio(image)
            st.success("Your story and audio are ready! 🌟")
        except Exception as error:
            st.session_state["is_generating"] = False
            st.error("Something went wrong while making the story or audio. 😢")
            st.warning("Please try another image or click the button again.")

            with st.expander("Show error details for debugging"):
                st.write(error)

    if st.session_state["has_result"]:
        display_results()

        if not st.session_state["is_generating"]:
            st.markdown(
                '<div class="next-box">What would you like to do next?</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2, gap="large")

            with col1:
                if st.button("🔄 Tell Me Another Story!"):
                    try:
                        create_story_and_audio(image)
                        st.success("A new story is ready! 🌟")
                        st.rerun()
                    except Exception as error:
                        st.session_state["is_generating"] = False
                        st.error("Something went wrong while making another story. 😢")

                        with st.expander("Show error details for debugging"):
                            st.write(error)

            with col2:
                if st.button("🖼️ Try a New Image!"):
                    clear_results()
                    st.info("Please click the small X beside the uploaded file, then upload a new image.")

            st.markdown(
                '<div class="footer-line">📷 ✨ 📖 🔊 ✨ 📷</div>',
                unsafe_allow_html=True
            )

# Start the app.
if __name__ == "__main__":
    main()
