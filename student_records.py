
students = [
    {"name": "Dass", "age": 20, "department": "CSE",
     "marks": [78, 85, 72], "attendance": 91},
    {"name": "Chandra", "age": 19, "department": "CSE",
     "marks": [65, 71, 68], "attendance": 84},
    {"name": "Parvathi", "age": 20, "department": "ECE",
     "marks": [45, 52, 48], "attendance": 72}
]

def average(student):
    return sum(student["marks"]) / len(student["marks"])

def display_students():
    for s in students:
        avg = average(s)
        result = "PASS" if avg >= 40 else "FAIL"
        print(f'{s["name"]} | {s["department"]} | '
              f'Average: {avg:.1f} | {result} | '
              f'Attendance: {s["attendance"]}%')

def class_summary():
    total = sum(sum(s["marks"]) for s in students)
    count = sum(len(s["marks"]) for s in students)
    top = max(students, key=average)

    print("\n--- CLASS SUMMARY ---")
    print("Total Students:", len(students))
    print("Average Class Mark:", round(total / count, 1))
    print("Top Performer:", top["name"],
          "- Average:", round(average(top), 1))

    print("\nAttendance Below 75%:")
    for s in students:
        if s["attendance"] < 75:
            print(s["name"], "-", str(s["attendance"]) + "%")

    print("\nStudents with Average Marks >= 60:")
    for s in students:
        if average(s) >= 60:
            print(s["name"])

print("--- STUDENT RECORDS ---")
display_students()
class_summary()
