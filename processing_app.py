# -*- coding: utf-8 -*-
"""Processing_APP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z5UJgqDv0sWYwLZfbhQ-uoMZqxvVCLg0
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt

def load_image(uploaded_file):
    if uploaded_file is not None:
        image_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, 1)
        return image
    return None

def display_image(image, title="Image"):
    if image is None:
        st.write("No image to display.")
        return

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.imshow(image_rgb)
    ax.set_title(title)
    ax.axis('off')
    st.pyplot(fig)

def apply_filter(image, filter_type, sigma=1):
    if image is None:
        st.write("No image uploaded.")
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if filter_type == 'Mean':
        return cv2.blur(image, (5, 5))
    elif filter_type == 'Gaussian':
        kernel_size = int(2 * round(3 * abs(sigma)) + 1)
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    elif filter_type == 'Canny':
        blurred = cv2.GaussianBlur(gray, (5, 5), sigma)
        return cv2.Canny(blurred, 100, 200)
    else:
        return image

st.title("Image Processing App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = load_image(uploaded_file)
    st.subheader("Original Image")
    display_image(original_image)

    filter_type = st.selectbox('Select Filter:', ['Mean', 'Gaussian', 'Canny'])
    sigma = st.slider('Sigma:', 0.1, 10.0, 1.0, 0.1)

    if st.button("Apply Filter"):
        processed_image = apply_filter(original_image, filter_type, sigma)
        st.subheader(f"{filter_type} Filtered Image")
        display_image(processed_image)

        if processed_image is not None:
            # Convert the processed image to bytes
            is_success, buffer = cv2.imencode(".png", processed_image)
            if is_success:
                btn = st.download_button(
                    label="Download Filtered Image",
                    data=buffer.tobytes(),
                    file_name="filtered_image.png",
                    mime="image/png"
                )