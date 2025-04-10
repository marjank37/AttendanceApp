from tkinter import Tk, Label, Button
from Entities.Student import Student
from Entities.Class import Classes
import pandas as pd
import csv

# === Load students from CSV into class ===
my_class = Classes()
df = pd.read_csv("D:/python/Attendance_Project/student_list.csv")

for i, row in df.iterrows():
    student = Student(
        id=i + 1,
        first_name=row["first_name"],
        last_name=row["last_name"],
        student_card=row["student_card"]
    )
    my_class.students_list.append(student)

# === GUI setup ===
root = Tk()
root.title("Attendance Tracker")

# === Table Headers ===
Label(root, text="#", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
Label(root, text="First Name", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)
Label(root, text="Last Name", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)

for i in range(10):
    Label(root, text=f"Session {i+1}", font=("Arial", 10, "bold")).grid(row=1, column=i+3, padx=5, pady=5)

# === Dictionary to hold label references ===
student_labels = {}  # key = student.id, value = (id_label, first_name_label, last_name_label)

# === Toggle Button Function ===
def toggle_status(btn, student, session_index):
    current = btn["text"]
    if current == "Empty":
        btn.config(text="Present", bg="green", fg="white")
        student.attendance[session_index] = "Present"
    elif current == "Present":
        btn.config(text="Absent", bg="red", fg="white")
        student.attendance[session_index] = "Absent"
    else:
        btn.config(text="Empty", bg="gray", fg="white")
        student.attendance[session_index] = "Empty"

    # Update color if absent > 3
    absence_count = student.attendance.count("Absent")
    id_lbl, fname_lbl, lname_lbl = student_labels[student.id]
    color = "red" if absence_count > 3 else "black"
    id_lbl.config(fg=color)
    fname_lbl.config(fg=color)
    lname_lbl.config(fg=color)

# === Draw Table ===
for row_idx, student in enumerate(my_class.students_list):
    id_label = Label(root, text=student.id)
    fname_label = Label(root, text=student.first_name)
    lname_label = Label(root, text=student.last_name)

    id_label.grid(row=row_idx + 2, column=0, padx=5, pady=2)
    fname_label.grid(row=row_idx + 2, column=1, padx=5, pady=2)
    lname_label.grid(row=row_idx + 2, column=2, padx=5, pady=2)

    student_labels[student.id] = (id_label, fname_label, lname_label)

    for sess_idx in range(10):
        btn = Button(root, text="Empty", bg="gray", width=8)
        btn.grid(row=row_idx+2, column=sess_idx+3, padx=2, pady=2)
        btn.config(command=lambda b=btn, s=student, idx=sess_idx: toggle_status(b, s, idx))

# === Export to TXT and CSV ===
def export_data():
    # Export to TXT (using method in your Class)
    my_class.save_to_txt("attendance_output.txt")

    # Export to CSV
    with open("attendance_output.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        # header
        writer.writerow(["First Name", "Last Name", "Student Card"] + [f"Session {i+1}" for i in range(10)])
        # data
        for student in my_class.students_list:
            writer.writerow([
                student.first_name,
                student.last_name,
                student.student_card,
                *student.attendance
            ])

    print("Data saved to attendance_output.txt and attendance_output.csv")

# === Export Button ===
Button(root, text="Export", command=export_data, bg="blue", fg="white", width=15)\
    .grid(row=len(my_class.students_list)+3, column=0, columnspan=3, pady=10)

# === Run GUI ===
root.mainloop()
