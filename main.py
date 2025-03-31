import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from stability_sdk import client as stable_diffusion
import io
from PIL import Image

# Stability AI API key
STABILITY_API_KEY = "sk-kIPETilq2piuydomUkS7lphv6rMa2K6K7NvaJ7QMxMvCtmjW"

# Initialize Stable Diffusion client
stable_client = stable_diffusion.StabilityInference(
    key=STABILITY_API_KEY,
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0"
)

# Custom Styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: #ffffff;
        }
        .title-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .title {
            font-size: 42px;
            font-weight: 800;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .subtitle {
            font-size: 22px;
            font-weight: 500;
            font-family: 'Lora', serif;
            color: #e0e0e0;
        }
        .stButton > button {
            background-color: #e63946;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            transition: 0.3s ease-in-out;
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
        }
        .stButton > button:hover {
            background-color: #c92a2a;
        }
        .output-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            margin-top: 20px;
            font-size: 18px;
            color: #0a1931;
            border-left: 5px solid #ffffff;
            font-family: 'Lora', serif;
        }
    </style>
""", unsafe_allow_html=True)

# Options for Length & Language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# App Title
st.markdown(
    '<div class="title-container"><div class="title">🚀 BrandBoost</div><div class="subtitle">AI-Powered LinkedIn Post Generator</div></div>',
    unsafe_allow_html=True)

# Layout for Inputs
fs = FewShotPosts()
tags = fs.get_tags()

col1, col2, col3 = st.columns(3)

with col1:
    selected_tag = st.selectbox("🔖 Topic", options=tags)

with col2:
    selected_length = st.selectbox("📏 Length", options=length_options)

with col3:
    selected_language = st.selectbox("🗣️ Language", options=language_options)

# Description Field (User Input)
description = st.text_area("📝 Description (Optional)", placeholder="Provide specific details to personalize your post...")

# Function to generate an image from text
# Function to generate an image from text without any text elements
def generate_image(prompt):
    # Modify the prompt to explicitly discourage text
    sanitized_prompt = (
        f"{prompt}, ultra HD, photorealistic, no text, no letters, "
        "no symbols, no words, no captions, no numbers, no logos, no watermarks, "
        "pure visual representation, cinematic lighting, 8K"
    )

    response = stable_client.generate(sanitized_prompt)  # No negative_prompt argument

    for resp in response:
        for artifact in resp.artifacts:
            if artifact.type == 1:  # 1 represents image
                return Image.open(io.BytesIO(artifact.binary))

    return None

# Generate Button with Spinner
if st.button("✨ Generate Post & Image"):
    with st.spinner("Generating your LinkedIn post..."):
        post = generate_post(selected_length, selected_language, selected_tag, description)  # Pass Description

    # Display Post
    st.markdown(f"## Here is a LinkedIn post on {selected_tag}:")
    st.markdown(f'<div class="output-box">{post}</div>', unsafe_allow_html=True)

    # Generate Image Based on Post
    with st.spinner("Generating an image for your post..."):
        generated_image = generate_image(post)

    if generated_image:
        st.image(generated_image, caption="Generated Image for Your Post", width=700)
    else:
        st.error("Failed to generate an image. Please try again.")

    # Copy Button
    st.button("📋 Copy to Clipboard", key="copy_button")
