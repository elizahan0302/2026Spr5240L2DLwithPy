import streamlit as st
from PIL import Image
from transformers import pipeline

# Set up the Streamlit page.
st.set_page_config(
    page_title="Little Garden Story Maker",
    page_icon="🌸",
    layout="wide"
)

# Add child-friendly CSS styles.
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            90deg,
            #B8F2C2 0%,
            #EFFFF4 10%,
            #FFFDF2 25%,
            #FFFDF2 75%,
            #EFFFF4 90%,
            #B8F2C2 100%
        );
    }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        background-color: rgba(255, 255, 255, 0.82);
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

    .garden-title {
        text-align: center;
        font-size: 32px;
        margin-bottom: 10px;
    }

    .grass-left {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 140px;
        height: 100%;
        background: linear-gradient(to top, #7ED957, #B8F2C2);
        opacity: 0.85;
        z-index: -1;
        border-right: 6px dashed #5DBB63;
    }

    .grass-right {
        position: fixed;
        right: 0;
        bottom: 0;
        width: 140px;
        height: 100%;
        background: linear-gradient(to top, #7ED957, #B8F2C2);
        opacity: 0.85;
        z-index: -1;
        border-left: 6px dashed #5DBB63;
    }

    .flower-left {
        position: fixed;
        left: 18px;
        bottom: 30px;
        font-size: 34px;
        line-height: 1.8;
        z-index: 1;
    }

    .flower-right {
        position: fixed;
        right: 18px;
        bottom: 30px;
        font-size: 34px;
        line-height: 1.8;
        z-index: 1;
    }

    .top-flower-line {
        text-align: center;
        font-size: 28px;
        margin-bottom: 8px;
    }

    .footer-garden {
        text-align: center;
        font-size: 28px;
        margin-top: 25px;
    }

    @media screen and (max-width: 900px) {
        .grass-left, .grass-right, .flower-left, .flower-right {
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

    <div class="grass-left"></div>
    <div class="grass-right"></div>

    <div class="flower-left">
        🌸<br>🌷<br>🌼<br>🌸<br>🌱
    </div>

    <div class="flower-right">
        🌱<br>🌸<br>🌼<br>🌷<br>🌸
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

# Load the story generation model.
@st.cache_resource
def load_story_generator():
    return pipeline(
        "text-generation",
        model="pranavpsv/genre-story-generator-v2"
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
        return result[0].get("generated_text", "")

    return "a beautiful and magical picture"

# Generate a complete child-friendly story from the caption.
def generate_story(caption, story_generator):
    prompt = (
        "Write a complete cheerful children's story for kids aged 3 to 10. "
        "The story must be between 50 and 90 words. "
        "The story must have a clear beginning, middle, and happy ending. "
        "Use simple, kind, and positive language. "
        f"The story is based on this picture: {caption}. "
        "Story:"
    )

    result = story_generator(
        prompt,
        max_new_tokens=140,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1
    )

    generated_text = result[0]["generated_text"]
    story = generated_text.replace(prompt, "").strip()
    story = clean_story(story)

    if len(story.split()) < 50 or not story.endswith((".", "!", "?")):
        story = create_backup_story(caption)

    return story

# Clean the generated story and stop it at the last complete sentence.
def clean_story(story):
    story = story.replace("\n", " ").strip()

    ending_positions = [
        story.rfind("."),
        story.rfind("!"),
        story.rfind("?")
    ]

    last_ending = max(ending_positions)

    if last_ending != -1:
        story = story[:last_ending + 1]

    words = story.split()

    if len(words) > 100:
        shortened_story = " ".join(words[:100])

        ending_positions = [
            shortened_story.rfind("."),
            shortened_story.rfind("!"),
            shortened_story.rfind("?")
        ]

        last_ending = max(ending_positions)

        if last_ending != -1:
            story = shortened_story[:last_ending + 1]
        else:
            story = create_backup_story("a wonderful picture")

    return story

# Create a backup story if the model output is too short.
def create_backup_story(caption):
    return (
        f"Once upon a time, there was {caption}. "
        "It was a bright and happy day in a little garden. "
        "A curious friend looked around and found something wonderful to explore. "
        "With a big smile and a brave heart, the friend went on a small adventure. "
        "Along the way, everyone learned to be kind, curious, and helpful. "
        "At sunset, they all felt proud, safe, and happy."
    )

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
        <div class="top-flower-line">
        🌸 🌿 🌷 🌼 🌿 🌸
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("🌸 Little Garden Story Maker")

    st.markdown(
        """
        <div class="tip-box">
        👋 Hello, little storyteller!<br>
        Upload a picture, and I will grow a magical story for you in our story garden. 📷🌱<br>
        Then you can listen to your story too! 📖🔊
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    uploaded_file = st.file_uploader(
        "📷 Choose a picture to begin your garden story adventure!",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Please upload a picture first. A little story flower is waiting to bloom! 🌸")
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

    if st.button("✨ Grow My Story! ✨"):
        try:
            with st.spinner("Loading the AI garden tools... 🧠🌱"):
                captioning_model = load_captioning_model()
                story_generator = load_story_generator()
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

            with st.spinner("Growing a magical story for you... 📖🌸"):
                story = generate_story(caption, story_generator)

            st.markdown("### 📖 Your Garden Story")
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

            st.success("Your story has bloomed! Great job, little storyteller! 🌟🌸")

            st.markdown(
                """
                <div class="footer-garden">
                🌱 🌸 🌼 🌷 🌿 🌷 🌼 🌸 🌱
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as error:
            st.error("Oh no! Something went wrong while growing the story. 😢")
            st.warning("Please try another image or click the button again.")

            with st.expander("Show error details for debugging"):
                st.write(error)

# Start the app.
if __name__ == "__main__":
    main()
