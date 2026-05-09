import streamlit as st
from PIL import Image
from transformers import pipeline

# Set up the Streamlit page.
st.set_page_config(
    page_title="AI Storytelling App for Kids",
    page_icon="🌈",
    layout="centered"
)

# Add child-friendly CSS styles.
st.markdown(
    """
    <style>
    .main {
        background-color: #FFF8DC;
    }

    h1 {
        text-align: center;
        color: #FF6F61;
        font-size: 44px;
    }

    h2, h3 {
        color: #4B7BEC;
    }

    .stButton > button {
        width: 100%;
        height: 65px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 20px;
        background-color: #FFCE54;
        color: #333333;
        border: 3px solid #F6B93B;
    }

    .stButton > button:hover {
        background-color: #FFD966;
        color: #000000;
        border: 3px solid #E58E26;
    }

    .story-box {
        background-color: #E8F8F5;
        padding: 20px;
        border-radius: 20px;
        border: 3px solid #55E6C1;
        font-size: 20px;
        line-height: 1.6;
        color: #2C3A47;
    }

    .caption-box {
        background-color: #FDEBD0;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #F5B041;
        font-size: 18px;
        color: #2C3A47;
    }

    .tip-box {
        background-color: #F4ECF7;
        padding: 18px;
        border-radius: 18px;
        border: 2px solid #BB8FCE;
        font-size: 18px;
        color: #2C3A47;
        line-height: 1.6;
    }
    </style>
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

# Generate a child-friendly story from the caption.
def generate_story(caption, story_generator):
    prompt = (
        "Write a cheerful and simple children's story for kids aged 3 to 10. "
        "The story should be 50 to 100 words. "
        "Use positive, kind, and magical language. "
        f"The story is based on this picture: {caption}. "
        "Story:"
    )

    result = story_generator(
        prompt,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        num_return_sequences=1
    )

    generated_text = result[0]["generated_text"]
    story = generated_text.replace(prompt, "").strip()

    if len(story.split()) < 30:
        story = create_backup_story(caption)

    words = story.split()
    if len(words) > 100:
        story = " ".join(words[:100]) + "."

    return story

# Create a backup story if the model output is too short.
def create_backup_story(caption):
    return (
        f"Once upon a time, there was {caption}. "
        "It was a bright and happy day. A little friend looked around and found "
        "something wonderful to explore. With a big smile and a brave heart, "
        "the friend went on a small adventure. Along the way, everyone learned "
        "to be kind, curious, and helpful. At the end of the day, they all felt "
        "proud and happy."
    )

# Convert the story into audio.
def generate_audio(story, audio_generator):
    speech_output = audio_generator(story)
    audio_array = speech_output["audio"]
    sample_rate = speech_output["sampling_rate"]
    return audio_array, sample_rate

# Run the main Streamlit app.
def main():
    st.title("🌈 AI Storytelling App for Kids")

    st.markdown(
        """
        <div class="tip-box">
        👋 Hello, little storyteller!<br>
        Upload a picture, and I will create a magical story for you. 📷✨<br>
        Then you can listen to your story too! 📖🔊
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "📷 Choose a picture to begin your story adventure!",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Please upload a picture first. A fun story is waiting for you! ✨")
        return

    image = open_uploaded_image(uploaded_file)

    if image is None:
        return

    st.image(
        image,
        caption="Your uploaded picture 🖼️",
        use_container_width=True
    )

    if st.button("✨ Make My Story! ✨"):
        try:
            with st.spinner("Loading the AI models... 🧠✨"):
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

            with st.spinner("Writing a magical story for you... 📖✨"):
                story = generate_story(caption, story_generator)

            st.markdown("### 📖 Your Magical Story")
            st.markdown(
                f"""
                <div class="story-box">
                {story}
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.spinner("Turning your story into audio... 🔊🎵"):
                audio_array, sample_rate = generate_audio(story, audio_generator)

            st.markdown("### 🔊 Listen to Your Story")
            st.audio(audio_array, sample_rate=sample_rate)

            st.success("Your story is ready! Great job, little storyteller! 🌟")

        except Exception as error:
            st.error("Oh no! Something went wrong while making the story. 😢")
            st.warning("Please try another image or click the button again.")

            with st.expander("Show error details for debugging"):
                st.write(error)

# Start the app.
if __name__ == "__main__":
    main()
