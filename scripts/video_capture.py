import cv2
import numpy as np
from face_detector import detect_and_encode_faces
from database import log_attendance, get_student_encodings, has_attendance_been_logged_today

def recognize_and_log_faces(frame):
    face_data = detect_and_encode_faces(frame)
    known_faces = get_student_encodings()

    for encoding, (top, right, bottom, left) in face_data:
        x, y, w, h = left, top, right - left, bottom - top
        for student_id, known_encoding in known_faces.items():
            distance = np.linalg.norm(encoding - known_encoding)
            if distance < 0.6 and not has_attendance_been_logged_today(student_id):
                log_attendance(student_id)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Attendance Logged", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                return  # Log only once per frame to avoid multiple entries

def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera is not accessible")
        return

    print("Press 'a' to capture attendance or 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Video', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('a'):
            recognize_and_log_faces(frame)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
