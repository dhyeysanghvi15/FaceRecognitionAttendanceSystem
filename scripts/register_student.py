import cv2
import face_recognition
import time
from database import add_student, get_student_by_name, update_student_encoding

def capture_face_encoding():
    cap = cv2.VideoCapture(0)
    print("Adjust your position in front of the camera. Press 'c' to start the countdown.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow('Video', frame)

        # Wait for the user to press 'c' to start the countdown
        if cv2.waitKey(1) & 0xFF == ord('c'):
            print("Capturing in...")
            for i in range(3, 0, -1):
                print(i)
                time.sleep(1)

            # Convert the image to RGB and find face encodings
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if face_encodings:
                print("Face captured successfully.")
                cap.release()
                cv2.destroyAllWindows()
                return face_encodings[0]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Registration cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def register_student():
    student_name = input("Enter the name of the student: ")
    existing_student_id = get_student_by_name(student_name)

    if existing_student_id:
        print(f"Student '{student_name}' is already registered.")
        choice = input("Press 'm' to modify the registration, or 'q' to quit: ")
        if choice.lower() == 'q':
            print("Registration cancelled.")
            return
        elif choice.lower() == 'm':
            print(f"Modifying the registration for '{student_name}'.")

    print("Please look directly into the camera to capture face encoding.")
    face_encoding = capture_face_encoding()

    if face_encoding is not None:
        if existing_student_id:
            update_student_encoding(existing_student_id, face_encoding)
            print(f"Student '{student_name}' encoding updated successfully.")
        else:
            student_id = add_student(student_name, face_encoding)
            print(f"Student '{student_name}' registered successfully with ID {student_id}.")
    else:
        print("Failed to capture face encoding. Please try again.")

if __name__ == "__main__":
    register_student()
