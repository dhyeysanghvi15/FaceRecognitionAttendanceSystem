import psycopg2
import os
import pickle
from datetime import datetime

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST')
    )

def add_student(name, encoding):
    with connect_db() as conn:
        with conn.cursor() as cur:
            encoded_data = pickle.dumps(encoding)
            cur.execute("INSERT INTO students (name, encoding) VALUES (%s, %s) RETURNING id", (name, encoded_data))
            student_id = cur.fetchone()[0]
            conn.commit()
            return student_id

def update_student_encoding(student_id, encoding):
    with connect_db() as conn:
        with conn.cursor() as cur:
            encoded_data = pickle.dumps(encoding)
            cur.execute("UPDATE students SET encoding = %s WHERE id = %s", (encoded_data, student_id))
            conn.commit()

def get_student_by_name(name):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM students WHERE name = %s", (name,))
            result = cur.fetchone()
            return result[0] if result else None

def get_student_encodings():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, encoding FROM students")
            students = {row[0]: pickle.loads(row[1]) for row in cur.fetchall() if row[1] is not None}
            return students

def log_attendance(student_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO attendance (student_id, date_time) VALUES (%s, %s)", (student_id, datetime.now()))
            conn.commit()

def has_attendance_been_logged_today(student_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = %s AND DATE(date_time) = CURRENT_DATE
                """, (student_id,))
            return cur.fetchone()[0] > 0
