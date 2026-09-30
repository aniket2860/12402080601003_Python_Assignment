# Assignment 1
# Question 1 - Campus Merit Analyzer using Compound Data Structures

def main():

    first_line = input().split()

    if len(first_line) != 3:
        print("INVALID")
        return

    n, k, m = map(int, first_line)

    if n < 1 or k < 1 or m < 1:
        print("INVALID")
        return

    students = []

    for _ in range(n):

        parts = input().split()

        if len(parts) != 4 + m:
            print("INVALID")
            return

        enrollment = parts[0]
        name = parts[1]
        semester = int(parts[2])
        cpi = float(parts[3])

        marks = list(map(int, parts[4:]))

        if semester < 1 or semester > 8:
            print("INVALID")
            return

        if any(mark < 0 or mark > 100 for mark in marks):
            print("INVALID")
            return

        average = sum(marks) / m

        students.append({
            "enrollment": enrollment,
            "name": name,
            "semester": semester,
            "cpi": cpi,
            "marks": marks,
            "average": average
        })

    # Group students by semester
    semester_students = {}

    for student in students:
        semester = student["semester"]

        if semester not in semester_students:
            semester_students[semester] = []

        semester_students[semester].append(student)

    # Print top K students for each semester
    for semester in sorted(semester_students):

        students_in_semester = semester_students[semester]

        students_in_semester.sort(
            key=lambda student: (
                -student["cpi"],
                -student["average"],
                student["enrollment"]
            )
        )

        top_students = students_in_semester[:k]

        print(
            f"Semester {semester}:",
            *[student["enrollment"] for student in top_students]
        )

    # Find subject-wise highest marks
    for subject_index in range(m):

        highest_mark = max(
            student["marks"][subject_index]
            for student in students
        )

        toppers = [
            student["enrollment"]
            for student in students
            if student["marks"][subject_index] == highest_mark
        ]

        toppers.sort()

        print(
            f"S{subject_index + 1}:",
            *toppers
        )


if __name__ == "__main__":
    main()