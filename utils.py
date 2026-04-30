from PIL import Image
import numpy as np
import cv2

def load_image(uploaded_file):
    image = Image.open(uploaded_file)
    return np.array(image)

def convert_to_bytes(image):
    _, buffer = cv2.imencode('.png', image)
    return buffer.tobytes()