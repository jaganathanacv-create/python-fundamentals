
import json
import os


DATA_FILE = "students.json"


class Student:
    def __init__(self, student_id, name, department, marks, attendance,
                 status="Active"):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.marks = marks
        self.attendance = attendance
        self.status = status

    @property
    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0

    @property
    def performance(self):
        if self.average >= 75:
            return "Excellent"
        elif self.average >= 60:
            return "Good"
        elif self.average >= 40:
            return "Average"
        return "Needs Improvement"

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "department": self.department,
            "marks": self.marks,
            "attendance": self.attendance,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"], data["name"], data["department"],
            data["marks"], data["attendance"],
            data.get("status", "Active")
        )

    def display(self):
        print(f"\nID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Average: {self.average:.1f}%")
        print(f"Attendance: {self.attendance}%")
        print(f"Performance: {self.performance}")
        print(f"Status: {self.status}")


class FileManager:
    @staticmethod
    def load():
        if not os.path.exists(DATA_FILE):
            return []

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("Invalid file format. Starting with empty records.")
                return []

            students = []
            for record in data:
                try:
                    student = Student.from_dict(record)
                    if (
                        student.marks
                        and all(
                            isinstance(m, (int, float)) and 0 <= m <= 100
                            for m in student.marks
                        )
                        and 0 <= student.attendance <= 100
                    ):
                        students.append(student)
                except (KeyError, TypeError, ValueError):
                    print("Skipping an invalid student record.")

            return students

        except (json.JSONDecodeError, OSError):
            print("Unable to read data file. Starting with empty records.")
            return []

    @staticmethod
    def save(students):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in students],
                    file,
                    indent=4
                )
            return True
        except OSError:
            print("Error: Could not save student records.")
            return False


class ReportGenerator:
    @staticmethod
    def generate(students):
        if not students:
            print("No student records available.")
            return

        ranked = sorted(
            students, key=lambda student: student.average, reverse=True
        )

        print("\n========== STUDENT REPORT ==========")
        for student in ranked:
            print(
                f"{student.student_id} | {student.name} | "
                f"{student.department} | Average: {student.average:.1f}% | "
                f"Performance: {student.performance}"
            )

        class_average = sum(s.average for s in students) / len(students)
        print("\nTotal Students:", len(students))
        print(f"Class Average: {class_average:.1f}%")
        print("Top Performer:", ranked[0].name)
        print("Active Students:",
              sum(s.status == "Active" for s in students))


class StudentManager:
    def __init__(self):
        self.students = FileManager.load()

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def add_student(self):
        student_id = input("Student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return

        if self.find_student(student_id):
            print("Duplicate student ID. Student not added.")
            return

        name = input("Student name: ").strip()
        department = input("Department: ").strip()

        if not name or not department:
            print("Name and department cannot be empty.")
            return

        marks = []
        for i in range(1, 4):
            while True:
                try:
                    mark = float(input(f"Subject {i} marks (0-100): "))
                    if 0 <= mark <= 100:
                        marks.append(mark)
                        break
                    print("Marks must be between 0 and 100.")
                except ValueError:
                    print("Enter a valid number.")

        while True:
            try:
                attendance = float(input("Attendance (0-100): "))
                if 0 <= attendance <= 100:
                    break
                print("Attendance must be between 0 and 100.")
            except ValueError:
                print("Enter a valid number.")

        student = Student(
            student_id, name, department, marks, attendance
        )
        self.students.append(student)

        if FileManager.save(self.students):
            print("Student added successfully.")
        else:
            self.students.remove(student)

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        for student in self.students:
            student.display()

    def search_student(self):
        student_id = input("Enter student ID: ").strip()
        student = self.find_student(student_id)

        if student:
            student.display()
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter student ID to update: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        print("1. Update name")
        print("2. Update department")
        print("3. Update marks")
        print("4. Update attendance")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            value = input("New name: ").strip()
            if value:
                student.name = value
            else:
                print("Name cannot be empty.")
                return

        elif choice == "2":
            value = input("New department: ").strip()
            if value:
                student.department = value
            else:
                print("Department cannot be empty.")
                return

        elif choice == "3":
            marks = []
            for i in range(1, 4):
                while True:
                    try:
                        mark = float(input(f"Subject {i} marks (0-100): "))
                        if 0 <= mark <= 100:
                            marks.append(mark)
                            break
                        print("Marks must be between 0 and 100.")
                    except ValueError:
                        print("Enter a valid number.")
            student.marks = marks

        elif choice == "4":
            while True:
                try:
                    attendance = float(input("New attendance (0-100): "))
                    if 0 <= attendance <= 100:
                        student.attendance = attendance
                        break
                    print("Attendance must be between 0 and 100.")
                except ValueError:
                    print("Enter a valid number.")
        else:
            print("Invalid option.")
            return

        if FileManager.save(self.students):
            print("Student updated successfully.")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()
        student = self.find_student(student_id)

        if not student:
            print("Student not found.")
            return

        confirm = input(
            f"Delete {student.name}? Type yes to confirm: "
        ).strip().lower()

        if confirm == "yes":
            self.students.remove(student)
            if FileManager.save(self.students):
                print("Student deleted successfully.")
            else:
                self.students.append(student)
        else:
            print("Deletion cancelled.")

    def run(self):
        while True:
            print("\n===== OOP STUDENT MANAGEMENT =====")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Performance Report")
            print("7. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                ReportGenerator.generate(self.students)
            elif choice == "7":
                FileManager.save(self.students)
                print("Records saved. Goodbye!")
                break
            else:
                print("Invalid option. Choose 1-7.")


if __name__ == "__main__":
    manager = StudentManager()
    manager.run()
