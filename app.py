import streamlit as st
import cv2
from filters import *
from utils import *

# Page config
st.set_page_config(page_title="✨ Smart Image Editor", page_icon="🖼️", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    .stDownloadButton>button {
        background-color: #2196F3;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>✨ Smart Image Editor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload → Edit → Download your image easily</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🎨 Adjust Filters")

blur = st.sidebar.slider("Blur", 1, 51, 1)
sharpness = st.sidebar.slider("Sharpness", 0.0, 3.0, 0.0)
brightness = st.sidebar.slider("Brightness", -100, 100, 0)
contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)

gray = st.sidebar.checkbox("Grayscale")
edge = st.sidebar.checkbox("Edge Detection")

t1 = st.sidebar.slider("Threshold 1", 0, 255, 100)
t2 = st.sidebar.slider("Threshold 2", 0, 255, 200)

if st.sidebar.button("🔄 Reset"):
    st.rerun()

# Upload section
st.markdown("### 📤 Upload Your Image")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file is None:
    st.info("👆 Please upload an image to start editing")

# Processing
if uploaded_file is not None:
    image = load_image(uploaded_file)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    processed = image.copy()

    if blur > 1:
        processed = apply_blur(processed, blur)

    if sharpness > 0:
        processed = apply_sharpness(processed, sharpness)

    if brightness != 0:
        processed = adjust_brightness(processed, brightness)

    if contrast != 1.0:
        processed = adjust_contrast(processed, contrast)

    if gray:
        processed = to_grayscale(processed)

    if edge:
        processed = edge_detection(processed, t1, t2)

    # Display images
    st.markdown("### 🖼️ Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Original Image")
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_container_width=True)

    with col2:
        st.markdown("#### Edited Image")
        st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_container_width=True)

    # Download
    st.markdown("### 📥 Download Edited Image")

    img_bytes = convert_to_bytes(processed)

    st.download_button(
        label="⬇️ Download Image",
        data=img_bytes,
        file_name="edited.png",
        mime="image/png"
    )