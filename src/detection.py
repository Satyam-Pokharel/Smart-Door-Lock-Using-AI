import face_recognition
import pickle
if __name__!="__main__":
    from .camera import WebCamVideoStream
from itertools import chain
import cv2
import numpy as np
import time
import os
import telegram  # Import python-telegram-bot library
from dotenv import load_dotenv  # Import python-dotenv to load .env file

# Load environment variables from .env file
load_dotenv()

# Access Telegram bot token and admin chat ID from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def compare_encoding(image, authorized_encodings):
    try:
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        result = []
        for encoding in authorized_encodings:
            result.append(face_recognition.compare_faces(encoding, face_encodings))
        return np.argmax(np.bincount(list(chain(*result))))
    except:
        return False

def send_image_to_telegram(image_path):
    """Send the unauthorized user image to the admin via Telegram (synchronously)."""
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo, caption="Unauthorized user detected!")
        print(f"Image sent to Telegram admin (chat ID: {ADMIN_CHAT_ID})")
    except Exception as e:
        print(f"Error sending image to Telegram: {e}")

def saveFaceToFolder(image):
    try:
        filename = os.path.join(os.path.dirname(__file__), "..", "Unauthorized", f"{int(time.time())}.png")
        cv2.imwrite(filename, image)  # Saving as-is (RGB), will cause blue tint
        print(f"Saved unauthorized user photo to {filename}")

        # Send the saved image to Telegram admin (synchronously)
        send_image_to_telegram(filename)
    except Exception as e:
        print(f"Error saving unauthorized user photo: {e}")

def create_encoding(image_bytes, path):
    authorized_encodings = []
    for image in image_bytes:
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        authorized_encodings.extend(face_encodings)
    save_encoding(authorized_encodings)

def load_authorized_encoding(encoding_file_path):
    try:
        with open(encoding_file_path, 'rb') as file:
            authorized_face_encodings = pickle.load(file)
        return authorized_face_encodings
    except FileNotFoundError:
        print("File not found. No authorized face encodings loaded.")
        return []

def save_encoding(authorized_encodings):
    with open("C:\\Users\\satya\\Desktop\\IOT\\encoding\\user.txt", 'wb') as file:
        pickle.dump(authorized_encodings, file)

def take_register_user():
    stream = WebCamVideoStream()
    image_frames = []
    for i in range(200):
        print(i)
        rgb_frame = cv2.cvtColor(stream.read_frame(), cv2.COLOR_BGR2RGB)
        image_frames.append(rgb_frame)
    create_encoding(image_frames, "users.pk1")

def compare_face():
    try:
        stream = WebCamVideoStream()
        rgb_frame = cv2.cvtColor(stream.read_frame(), cv2.COLOR_BGR2RGB)
        authorized_encoding = load_authorized_encoding("C:\\Users\\satya\\Desktop\\IOT\\encoding\\user.txt")
        result = compare_encoding(rgb_frame, authorized_encoding)
        if result == 0:
            saveFaceToFolder(rgb_frame)
        return result
    except Exception as e:
        print(f"Error in compare_face: {e}")
        return False

if __name__ == "__main__":
    from camera import WebCamVideoStream
    take_register_user()