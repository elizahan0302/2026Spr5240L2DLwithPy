import streamlit as st
from PIL import Image
from transformers import pipeline
import random

# Set up the Streamlit page.
st.set_page_config(
    page_title="Puppy Picture Story",
    page_icon="🐶",
    layout="wide"
)

# Add child-friendly CSS styles.
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            90deg,
            #FFF1F6 0%,
            #FFF7FB 12%,
            #FFFDF2 28%,
            #FFFDF2 72%,
            #FFF7FB 88%,
            #FFF1F6 100%
        );
    }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }

    h1 {
        text-align: center;
        color: #FF6F91;
        font-size: 48px;
        font-weight: 800;
    }

    h2, h3 {
        color: #4B7BEC;
    }

    .stButton > button {
        width: 100%;
        height: 68px;
        font-size: 26px;
        font-weight: bold;
        border-radius: 25px;
        background-color: #FFCE54;
        color: #333333;
        border: 4px solid #F6B93B;
        box-shadow: 0 5px 0 #D99B24;
    }

    .stButton > button:hover {
        background-color: #FFD966;
        color: #000000;
        border: 4px solid #E58E26;
        transform: scale(1.01);
    }

    .story-box {
        background-color: #E8F8F5;
        padding: 24px;
        border-radius: 24px;
        border: 4px solid #55E6C1;
        font-size: 22px;
        line-height: 1.7;
        color: #2C3A47;
    }

    .caption-box {
        background-color: #FDEBD0;
        padding: 18px;
        border-radius: 18px;
        border: 3px solid #F5B041;
        font-size: 19px;
        color: #2C3A47;
    }

    .tip-box {
        background-color: #FCE4EC;
        padding: 20px;
        border-radius: 22px;
        border: 3px solid #F8A5C2;
        font-size: 19px;
        color: #2C3A47;
        line-height: 1.7;
        text-align: center;
    }

    .dog-left {
        position: fixed;
        left: 15px;
        top: 120px;
        width: 150px;
        opacity: 0.95;
        z-index: 1;
    }

    .dog-right {
        position: fixed;
        right: 15px;
        top: 120px;
        width: 150px;
        opacity: 0.95;
        z-index: 1;
    }

    .paw-left {
        position: fixed;
        left: 45px;
        bottom: 40px;
        font-size: 34px;
        line-height: 1.8;
        z-index: 1;
    }

    .paw-right {
        position: fixed;
        right: 45px;
        bottom: 40px;
        font-size: 34px;
        line-height: 1.8;
        z-index: 1;
    }

    .top-line {
        text-align: center;
        font-size: 30px;
        margin-bottom: 8px;
    }

    .footer-line {
        text-align: center;
        font-size: 28px;
        margin-top: 25px;
    }

    @media screen and (max-width: 1000px) {
        .dog-left, .dog-right, .paw-left, .paw-right {
            display: none;
        }

        .block-container {
            margin-top: 0px;
            border-radius: 18px;
        }

        h1 {
            font-size: 36px;
        }
    }
    </style>

    <div class="dog-left">
        <svg viewBox="0 0 200 200">
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
            <path d="M133 128 Q165 118 158 95" fill="none" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
            <text x="50" y="195" font-size="22">woof!</text>
        </svg>
    </div>

    <div class="dog-right">
        <svg viewBox="0 0 200 200">
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
            <path d="M67 128 Q35 118 42 95" fill="none" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
            <text x="48" y="195" font-size="22">hello!</text>
        </svg>
    </div>

    <div class="paw-left">
        🐾<br>🐾<br>🐾
    </div>

    <div class="paw-right">
        🐾<br>🐾<br>🐾
    </div>
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

# Open and check the uploaded image.
def open_uploaded_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        return image.convert("RGB")
    except Exception:
        st.error("Oops! 😢 This file does not look like a valid image. Please upload a JPG or PNG picture.")
        return None

# Generate a caption from the uploaded image.
def generate_caption(image, captioning_model):
    result = captioning_model(image)

    if result and isinstance(result, list):
        caption = result[0].get("generated_text", "").strip()
        if caption:
            return caption

    return "a lovely picture"

# Create a story that stays related to the image caption.
def generate_story_from_caption(caption):
    openings = [
        "One sunny morning",
        "On a bright and cheerful day",
        "Once upon a time",
        "One happy afternoon"
    ]

    feelings = [
        "felt curious and excited",
        "was ready for a little adventure",
        "wanted to explore the world",
        "felt happy and brave"
    ]

    actions = [
        "looked around carefully and found something special",
        "took a small step forward and smiled",
        "noticed a tiny surprise nearby",
        "decided to share the happy moment with a friend"
    ]

    lessons = [
        "being kind makes every day brighter",
        "small adventures can become wonderful memories",
        "curiosity can lead to happy discoveries",
        "sharing joy makes everyone smile"
    ]

    opening = random.choice(openings)
    feeling = random.choice(feelings)
    action = random.choice(actions)
    lesson = random.choice(lessons)

    story = (
        f"{opening}, there was {caption}. "
        f"It {feeling}. "
        f"It {action}. "
        "Along the way, a gentle friend came to help, and together they turned the moment into a magical adventure. "
        f"By the end of the day, everyone learned that {lesson}. "
        "They went home smiling, feeling proud, safe, and happy."
    )

    return story

# Convert the story into audio.
def generate_audio(story, audio_generator):
    speech_output = audio_generator(story)
    audio_array = speech_output["audio"]
    sample_rate = speech_output["sampling_rate"]
    return audio_array, sample_rate

# Run the main Streamlit app.
def main():
    st.markdown(
        """
        <div class="top-line">
        🐶 🐾 📖 ✨ 🐾 🐶
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("🐶 Puppy Picture Story")

    st.markdown(
        """
        <div class="tip-box">
        👋 Hello, little storyteller!<br>
        Upload a picture, and the puppy helper will make a story about your picture. 📷🐶<br>
        Then you can listen to your story too! 📖🔊
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    uploaded_file = st.file_uploader(
        "📷 Choose a picture to begin your puppy story adventure!",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Please upload a picture first. A puppy story is waiting for you! 🐶")
        return

    image = open_uploaded_image(uploaded_file)

    if image is None:
        return

    st.image(
        image,
        caption="Your uploaded picture 🖼️",
        use_container_width=True
    )

    st.write("")

    if st.button("✨ Make My Puppy Story! ✨"):
        try:
            with st.spinner("Loading the puppy helper tools... 🧠🐶"):
                captioning_model = load_captioning_model()
                audio_generator = load_audio_generator()

            with st.spinner("Looking carefully at your picture... 👀📷"):
                caption = generate_caption(image, captioning_model)

            st.markdown("### 🖼️ What I see in the picture")
            st.markdown(
                f"""
                <div class="caption-box">
                {caption}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            with st.spinner("Writing a story about your picture... 📖✨"):
                story = generate_story_from_caption(caption)

            st.markdown("### 📖 Your Puppy Story")
            st.markdown(
                f"""
                <div class="story-box">
                {story}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            with st.spinner("Turning your story into audio... 🔊🎵"):
                audio_array, sample_rate = generate_audio(story, audio_generator)

            st.markdown("### 🔊 Listen to Your Story")
            st.audio(audio_array, sample_rate=sample_rate)

            st.success("Your puppy story is ready! Great job, little storyteller! 🌟🐶")

            st.markdown(
                """
                <div class="footer-line">
                🐾 🐶 🐾 📖 🐾 🐶 🐾
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as error:
            st.error("Oh no! Something went wrong while making the story. 😢")
            st.warning("Please try another image or click the button again.")

            with st.expander("Show error details for debugging"):
                st.write(error)

# Start the app.
if __name__ == "__main__":
    main()
