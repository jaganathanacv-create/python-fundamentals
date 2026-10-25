
import json
import os

DATA_FILE = "students.json"


def load_students():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print("Invalid data format. Starting with empty records.")
                return []
            return data
    except (json.JSONDecodeError, OSError):
        print("File is empty or unreadable. Starting with empty records.")
        return []


def save_students(students):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        print("Error saving student records.")
        return False


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_number(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Invalid input. Enter a number.")


def get_marks():
    marks = []
    for subject in range(1, 4):
        mark = get_number(
            f"Enter marks for subject {subject} (0-100): ", 0, 100
        )
        marks.append(mark)
    return marks


def find_student(students, student_id):
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student
    return None


def add_student(students):
    student_id = get_text("Student ID: ")

    if find_student(students, student_id):
        print("Duplicate student ID! Student not added.")
        return

    student = {
        "id": student_id,
        "name": get_text("Student name: "),
        "department": get_text("Department: "),
        "marks": get_marks(),
        "attendance": get_number("Attendance (0-100%): ", 0, 100)
    }

    students.append(student)

    if save_students(students):
        print("Student added successfully.")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n--- ALL STUDENTS ---")
    for student in students:
        average = sum(student["marks"]) / len(student["marks"])
        result = "PASS" if average >= 40 else "FAIL"

        print(f"\nID: {student['id']}")
        print(f"Name: {student['name']}")
        print(f"Department: {student['department']}")
        print(f"Marks: {student['marks']}")
        print(f"Average: {average:.2f}")
        print(f"Attendance: {student['attendance']}%")
        print(f"Result: {result}")


def search_student(students):
    student_id = get_text("Enter student ID to search: ")
    student = find_student(students, student_id)

    if student:
        view_student_details(student)
    else:
        print("Student not found.")


def view_student_details(student):
    average = sum(student["marks"]) / len(student["marks"])
    print("\n--- STUDENT FOUND ---")
    print("ID:", student["id"])
    print("Name:", student["name"])
    print("Department:", student["department"])
    print("Marks:", student["marks"])
    print(f"Average: {average:.2f}%")
    print("Attendance:", str(student["attendance"]) + "%")
    print("Result:", "PASS" if average >= 40 else "FAIL")


def update_student(students):
    student_id = get_text("Enter student ID to update: ")
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    print("1. Update name")
    print("2. Update department")
    print("3. Update marks")
    print("4. Update attendance")

    choice = input("Choose field: ").strip()

    if choice == "1":
        student["name"] = get_text("New name: ")
    elif choice == "2":
        student["department"] = get_text("New department: ")
    elif choice == "3":
        student["marks"] = get_marks()
    elif choice == "4":
        student["attendance"] = get_number(
            "New attendance (0-100%): ", 0, 100
        )
    else:
        print("Invalid option.")
        return

    if save_students(students):
        print("Student updated successfully.")


def delete_student(students):
    student_id = get_text("Enter student ID to delete: ")
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    confirm = input(
        f"Delete {student['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        students.remove(student)
        if save_students(students):
            print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def performance_report(students):
    if not students:
        print("No records available for the report.")
        return

    ranked = sorted(
        students,
        key=lambda s: sum(s["marks"]) / len(s["marks"]),
        reverse=True
    )

    total = 0
    passed = 0

    print("\n--- PERFORMANCE REPORT ---")

    for student in ranked:
        average = sum(student["marks"]) / len(student["marks"])
        total += average

        if average >= 40:
            passed += 1

        result = "PASS" if average >= 40 else "FAIL"
        print(
            f"{student['name']} ({student['id']}) - "
            f"Average: {average:.2f} - {result}"
        )

    print("\nTotal students:", len(students))
    print(f"Class average: {total / len(students):.2f}")
    print("Passed:", passed)
    print("Failed:", len(students) - passed)
    print("Top performer:", ranked[0]["name"])


def main():
    students = load_students()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Performance Report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            performance_report(students)
        elif choice == "7":
            save_students(students)
            print("Records saved. Goodbye!")
            break
        else:
            print("Invalid option. Choose 1-7.")


if __name__ == "__main__":
    main()
