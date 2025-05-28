import base64
import cv2
import numpy as np

def load_file(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error loading file: {e}")

def save_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    