# **Face Recognition Attendance System**

## **Project Setup**
This project uses **PostgreSQL** as the database for managing student records and attendance. The database is connected to `scripts/database.py`, and authentication credentials are securely managed using **environment variables** to prevent exposing sensitive information in version control.

> **Note:** If this is your first time using PostgreSQL, your default username is `postgres`.

## **Database Schema**
The system consists of two tables:
1. **students** – Stores registered student details along with their facial encodings.
2. **attendance** – Logs student attendance with timestamps, restricting each student to one check-in per day.

## **Setting Up the Database**
1. Ensure **PostgreSQL** is installed and running. You can access it via:
   - `psql` (CLI)
   - **pgAdmin** (GUI)  
2. Create the necessary tables using `scripts/database.py`.

## **Registering a Student**
Run the **registration script** via the command line:
```sh
python scripts/register_student.py
```
- The terminal will guide you through capturing a student's facial encoding.
- If a student with the same name is already registered, you will be given the option to either **update the existing entry** or **exit**.

## **Marking Attendance**
Run the **video capture script** to log attendance:
```sh
python scripts/video_capture.py
```
- The system captures facial recognition data and logs attendance in the database.
- A student can only check in **once per day** to prevent duplicate entries.

## **Dependencies**
Ensure all required dependencies are installed before running the scripts. Use:
```sh
pip install -r requirements.txt
```

## **Author**
**Dhyey Sanghvi**  
📧 [Email](mailto:sanghvidhyey@gmail.com)
