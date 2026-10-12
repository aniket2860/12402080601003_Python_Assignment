# Assignment 2
# Question 3 - MySQL Student-Course Analytics Engine

import csv
import mysql.connector
from mysql.connector import Error


def connect_db(host, user, password, database):
    # Create database if it does not exist
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    cursor = connection.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{database}`"
    )
    cursor.close()
    connection.close()

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def setup_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            spi DECIMAL(4,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id VARCHAR(50) NOT NULL,
            course_id VARCHAR(50) NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id)
                REFERENCES Student(student_id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    cursor.close()


def import_students(connection, csv_path):
    cursor = connection.cursor()

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"student_id", "name", "spi"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "Student CSV must contain student_id,name,spi"
            )

        for row in reader:
            student_id = row["student_id"].strip()
            name = row["name"].strip()
            spi = float(row["spi"])

            if not student_id or not name or not 0 <= spi <= 10:
                raise ValueError("Invalid student record")

            cursor.execute("""
                INSERT INTO Student (student_id, name, spi)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    spi = VALUES(spi)
            """, (student_id, name, spi))

    connection.commit()
    cursor.close()


def import_registrations(connection, csv_path):
    cursor = connection.cursor()

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"student_id", "course_id"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "Registration CSV must contain student_id,course_id"
            )

        for row in reader:
            student_id = row["student_id"].strip()
            course_id = row["course_id"].strip()

            if not student_id or not course_id:
                raise ValueError("Invalid registration record")

            cursor.execute("""
                INSERT IGNORE INTO CourseRegistration
                    (student_id, course_id)
                VALUES (%s, %s)
            """, (student_id, course_id))

    connection.commit()
    cursor.close()


def show_analytics(connection, course_id, threshold):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT s.student_id, s.name, s.spi
        FROM Student s
        JOIN CourseRegistration r
            ON s.student_id = r.student_id
        WHERE r.course_id = %s AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id
    """, (course_id, threshold))

    results = cursor.fetchall()

    if results:
        for student_id, name, spi in results:
            print(f"{student_id} {name} {float(spi):.2f}")
    else:
        print("NO RESULTS")

    cursor.close()


def main():
    connection = None

    try:
        host = input("Host: ").strip()
        user = input("Username: ").strip()
        password = input("Password: ")
        database = input("Database: ").strip()

        if not database or not database.replace("_", "").isalnum():
            print("INVALID")
            return

        student_csv = input("Student CSV path: ").strip()
        registration_csv = input("Registration CSV path: ").strip()
        course_id = input("Course ID: ").strip()
        threshold = float(input("SPI threshold: ").strip())

        if not course_id or not 0 <= threshold <= 10:
            print("INVALID")
            return

        connection = connect_db(
            host, user, password, database
        )

        setup_tables(connection)
        import_students(connection, student_csv)
        import_registrations(connection, registration_csv)
        show_analytics(connection, course_id, threshold)

    except (ValueError, KeyError, OSError):
        print("INVALID")

    except Error as error:
        print("DATABASE_ERROR:", error)

    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
