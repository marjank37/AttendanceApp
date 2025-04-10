from Entities.Student import Student

class Classes:
    def __init__(self):
        self.students_list = []
        self.show_students_list = []

    def search(self, term):
        term = term.upper().strip()
        self.show_students_list.clear()
        for student in self.students_list:
            if (term in student.first_name.upper()
                or term in student.last_name.upper()
                or term in str(student.student_card)):
                self.show_students_list.append(student)

    def get_absent_count(self, student):
        return student.attendance.count("Absent")

    def get_absent_students(self, max_absences=3):
        return [s for s in self.students_list if self.get_absent_count(s) > max_absences]
        # other way for writing the code without list comprehension
        # result = []
        #for s in self.student_list:
            #if self.get_absent_count(s) > max_absences:
                #result.append()
                #return result

    def save_to_txt(self, filepath):
        with open(filepath, "w") as f:
            for s in self.students_list:
                line = f"{s.first_name} {s.last_name}: {', '.join(s.attendance)}\n"
                f.write(line)
