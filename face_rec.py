import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import face_recognition
import numpy as np
import cv2
import os

class Watcher:
    DIRECTORY_TO_WATCH = "faces_recognition"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(f"Received created event - {event.src_path}")
            classify_face(event.src_path)

def classify_face(image_path):
    # Convertir la ruta a una ruta absoluta
    image_path = os.path.abspath(image_path)
    # Verificar si la imagen se carga correctamente
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image: {image_path}")
        return

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)
            cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    while True:
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names

def load_known_faces():
    faces_encoded = []
    known_face_names = []
    for image_name in os.listdir("faces"):
        image_path = os.path.join("faces", image_name)
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error loading image: {image_path}")
            continue
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            faces_encoded.append(face_encodings[0])
            known_face_names.append(os.path.splitext(image_name)[0])
    return faces_encoded, known_face_names

if __name__ == '__main__':
    faces_encoded, known_face_names = load_known_faces()
    w = Watcher()
    w.run()