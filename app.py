import streamlit as st
from PIL import Image
from transformers import pipeline
import random

# Set up the Streamlit page.
st.set_page_config(
    page_title="Text to Audio Story",
    page_icon="📚",
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
        color: #2F3142;
        font-size: 48px;
        font-weight: 800;
    }

    h2, h3 {
        color: #4B7BEC;
    }

    .stButton > button {
        width: 100%;
        height: 68px;
        font-size: 24px;
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

    .step-box {
        background-color: #E8F8F5;
        padding: 14px;
        border-radius: 16px;
        border: 2px solid #55E6C1;
        font-size: 18px;
        color: #2C3A47;
        text-align: center;
        margin-top: 18px;
        margin-bottom: 18px;
    }

    .next-box {
        background-color: #FFF7E6;
        padding: 18px;
        border-radius: 18px;
        border: 3px solid #F7D794;
        font-size: 18px;
        color: #2C3A47;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .dog-left {
        position: fixed;
        left: 25px;
        top: 150px;
        width: 130px;
        opacity: 0.95;
        z-index: 1;
    }

    .dog-right {
        position: fixed;
        right: 25px;
        top: 150px;
        width: 130px;
        opacity: 0.95;
        z-index: 1;
    }

    .paw-left {
        position: fixed;
        left: 48px;
        bottom: 40px;
        font-size: 32px;
        line-height: 1.8;
        z-index: 1;
    }

    .paw-right {
        position: fixed;
        right: 48px;
        bottom: 40px;
        font-size: 32px;
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
        "One peaceful afternoon"
    ]

    feelings = [
        "felt curious and excited",
        "was ready for a small adventure",
        "wanted to explore the world nearby",
        "felt happy, brave, and kind"
    ]

    actions = [
        "looked around carefully and found something special",
        "took a small step forward and smiled",
        "noticed a tiny surprise nearby",
        "shared the happy moment with a new friend"
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
        f"{opening}, the picture showed {caption}. "
        f"It {feeling}. "
        f"It {action}. "
        "Along the way, a gentle friend came to help, and together they turned the moment into a magical adventure. "
        f"By the end of the day, everyone learned that {lesson}. "
        "They went home smiling, feeling proud, safe, and happy."
    )

    return story

# Add short pauses after sentence endings.
def add_pauses_to_text(story):
    paused_story = story.replace(". ", ". ... ")
    paused_story = paused_story.replace("! ", "! ... ")
    paused_story = paused_story.replace("? ", "? ... ")
    return paused_story

# Convert the story into audio.
def generate_audio(story, audio_generator):
    story_with_pauses = add_pauses_to_text(story)
    speech_output = audio_generator(story_with_pauses)

    audio_array = speech_output["audio"]
    sample_rate = speech_output["sampling_rate"]

    return audio_array, sample_rate

# Save generated results in session state.
def save_results(caption, story, audio_array, sample_rate):
    st.session_state["caption"] = caption
    st.session_state["story"] = story
    st.session_state["audio_array"] = audio_array
    st.session_state["sample_rate"] = sample_rate
    st.session_state["has_result"] = True

# Clear generated results from session state.
def clear_results():
    st.session_state["caption"] = ""
    st.session_state["story"] = ""
    st.session_state["audio_array"] = None
    st.session_state["sample_rate"] = None
    st.session_state["has_result"] = False

# Generate caption, story, and audio.
def create_story_and_audio(image):
    with st.spinner("Loading AI models... 🧠✨"):
        captioning_model = load_captioning_model()
        audio_generator = load_audio_generator()

    with st.spinner("Reading the picture... 👀📷"):
        caption = generate_caption(image, captioning_model)

    with st.spinner("Generating a short story... 📖✨"):
        story = generate_story_from_caption(caption)

    with st.spinner("Generating audio data... 🔊🎵"):
        audio_array, sample_rate = generate_audio(story, audio_generator)

    save_results(caption, story, audio_array, sample_rate)

# Display generated caption, story, and audio.
def display_results():
    st.markdown("### 🖼️ What I See in Your Picture")
    st.markdown(
        f"""
        <div class="caption-box">
        {st.session_state["caption"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### 📖 Your Magical Story")
    st.markdown(
        f"""
        <div class="story-box">
        {st.session_state["story"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### 🔊 Listen to Your Story")
    st.audio(
        st.session_state["audio_array"],
        sample_rate=st.session_state["sample_rate"]
    )

# Run the main Streamlit app.
def main():
    if "has_result" not in st.session_state:
        clear_results()

    st.markdown(
        """
        <div class="top-line">
        📷 📖 🔊
        </div>
        """,
        unsafe_allow_html=True
    )

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
        1️⃣ Upload a picture → 2️⃣ Create a story → 3️⃣ Listen to audio
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

    st.image(
        image,
        caption="Uploaded picture 🖼️",
        use_container_width=True
    )

    st.write("")

    if st.button("✨ Generate Story and Audio ✨"):
        try:
            create_story_and_audio(image)
            st.success("Story and audio generated successfully! 🌟")
        except Exception as error:
            st.error("Something went wrong while creating the story or audio. 😢")
            st.warning("Please try another image or click the button again.")

            with st.expander("Show error details for debugging"):
                st.write(error)

    if st.session_state["has_result"]:
        display_results()

        st.markdown(
            """
            <div class="next-box">
            What would you like to do next?
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Make Another Story"):
                try:
                    create_story_and_audio(image)
                    st.success("A new story has been created! 🌟")
                    st.rerun()
                except Exception as error:
                    st.error("Something went wrong while making another story. 😢")

                    with st.expander("Show error details for debugging"):
                        st.write(error)

        with col2:
            if st.button("🖼️ Choose a New Picture"):
                clear_results()
                st.info("Please click the small X beside the uploaded file, then upload a new picture.")

        st.markdown(
            """
            <div class="footer-line">
            📷 ✨ 📖 🔊 ✨ 📷
            </div>
            """,
            unsafe_allow_html=True
        )

# Start the app.
if __name__ == "__main__":
    main()
