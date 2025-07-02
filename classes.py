import uuid
from typing import List, Union
from persistent import Persistent
from persistent.list import PersistentList

class Course(Persistent):
    all_courses = {}

    def __init__(self, name: str, course_id: str = None):
        self.name = name
        self.course_id = course_id or str(uuid.uuid4())[:8]
        self.students = PersistentList()
        self.professors = PersistentList()
        Course.all_courses[self.name] = self

    def add_student(self, student: 'Student'):
        if student not in self.students:
            self.students.append(student)
        if self not in student.courses:
            student.courses.append(self)

    def add_professor(self, professor: 'Professor'):
        if professor not in self.professors:
            self.professors.append(professor)
        if self not in professor.courses:
            professor.courses.append(self)

    def get_students(self) -> List['Student']:
        return list(self.students)

    def get_professors(self) -> List['Professor']:
        return list(self.professors)

    def __str__(self):
        return f"Course({self.name}, {self.course_id})"
    __repr__ = __str__


class Professor(Persistent):
    def __init__(self, name: str, professor_id: str, courses: List[Union[Course, str]] = None):
        self.name = name
        self.professor_id = professor_id
        self.courses = PersistentList()
        for c in (courses or []):
            if isinstance(c, Course):
                course = c
            elif isinstance(c, str):
                course = Course.all_courses.get(c) or Course(c)
            else:
                raise TypeError("Each course must be a Course or a course-name string")
            self.add_course(course)

    def add_course(self, course: Course):
        if course not in self.courses:
            self.courses.append(course)
        if self not in course.professors:
            course.professors.append(self)

    def get_courses(self) -> List[Course]:
        return list(self.courses)

    def __str__(self):
        return f"Professor({self.name}, {self.professor_id})"
    __repr__ = __str__


class Student(Persistent):
    all_students = set()
    all_erasmus_students = set()

    def __init__(self,
                 name: str,
                 student_id: str,
                 year: int = 1,
                 courses: List[Union[Course, str]] = None,
                 erasmus: bool = False,
                 faculty: 'Faculty' = None):
        self.name = name
        self.student_id = student_id
        self.year = year
        self.erasmus = erasmus
        self.courses = PersistentList()

        if erasmus:
            Student.all_erasmus_students.add(self)
        else:
            Student.all_students.add(self)

        if faculty:
            if not isinstance(faculty, Faculty):
                raise TypeError("faculty must be a Faculty instance")
            self.faculty = faculty
            faculty.add_student(self)

        for c in (courses or []):
            if isinstance(c, Course):
                course = c
            elif isinstance(c, str):
                course = Course.all_courses.get(c) or Course(c)
            else:
                raise TypeError("Each course must be a Course or a course-name string")
            self.add_course(course)

    def add_course(self, course: Course):
        if course not in self.courses:
            self.courses.append(course)
        if self not in course.students:
            course.students.append(self)

    def get_courses(self) -> List[Course]:
        return list(self.courses)

    def __str__(self):
        return f"Student({self.name}, {self.student_id})"
    __repr__ = __str__


class Faculty(Persistent):
    all_faculties = set()

    def __init__(self, name: str, faculty_id: str, campus: 'Campus' = None):
        self.name = name
        self.faculty_id = faculty_id
        self.students = PersistentList()
        if not isinstance(campus, Campus):
            raise TypeError("campus must be a Campus instance")
        self.campus = campus
        campus.add_faculty(self)
        Faculty.all_faculties.add(self)

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)

    def get_students(self) -> List[Student]:
        return list(self.students)

    def __str__(self):
        return f"Faculty({self.name}, {self.faculty_id})"
    __repr__ = __str__


class Campus(Persistent):
    all_campuses = set()

    def __init__(self, name: str, campus_id: str):
        self.name = name
        self.campus_id = campus_id
        self.faculties = PersistentList()
        Campus.all_campuses.add(self)

    def add_faculty(self, faculty: Faculty):
        if faculty not in self.faculties:
            self.faculties.append(faculty)

    def get_faculties(self) -> List[Faculty]:
        return list(self.faculties)

    def __str__(self):
        return f"Campus({self.name}, {self.campus_id})"
    __repr__ = __str__
