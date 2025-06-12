from flask import Flask, render_template, request, redirect, jsonify
import face_recognition
import numpy as np
import cv2
import base64
import os

app = Flask(__name__)

# Load known face encodings
known_encodings = []
known_faces_dir = 'known_faces'

for filename in os.listdir(known_faces_dir):
    image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
    encoding = face_recognition.face_encodings(image)
    if encoding:
        known_encodings.append(encoding[0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data_url = request.json['image']
    encoded_data = data_url.split(',')[1]
    img_bytes = base64.b64decode(encoded_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, faces)

    for face_encoding in encodings:
        results = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
        if any(results):
            return jsonify({"authenticated": True})

    return jsonify({"authenticated": False})

@app.route('/dashboard')
def dashboard():
    return "Selamat datang! Anda berhasil login."

if __name__ == '__main__':
    app.run(debug=True)
