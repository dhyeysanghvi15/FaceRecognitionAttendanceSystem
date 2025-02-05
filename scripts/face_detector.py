import cv2
import face_recognition

def detect_and_encode_faces(frame):
    # Convert frame to RGB from BGR, which OpenCV uses
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Combine face encodings with their respective locations
    return zip(face_encodings, face_locations)
