# gui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
import transaction
from persistent.list import PersistentList
import instances

from classes import Student, Course, Professor, Faculty, Campus
from gui.forms import StudentForm, CourseForm, ProfessorForm, FacultyForm

class MainWindow(ttk.Notebook):
    def __init__(self, master, root):
        # Container for toolbar + notebook
        container = ttk.Frame(master)
        container.pack(expand=True, fill='both')

        # Toolbar with Reset button
        toolbar = ttk.Frame(container)
        toolbar.pack(fill='x')
        btn_reset = ttk.Button(toolbar, text="Reset Database", command=self.on_reset_db)
        btn_reset.pack(side='right', padx=5, pady=5)

        # The notebook itself
        super().__init__(container)
        self.pack(expand=True, fill='both')
        self.root = root

        # Build tabs
        self.build_students_tab()
        self.build_courses_tab()
        self.build_professors_tab()
        self.build_faculties_tab()
        self.load_all()

    def on_reset_db(self):
        if not messagebox.askyesno("Reset Database",
                                   "This will erase all data and reset the database. Continue?"):
            return

        for key in ('campuses', 'faculties', 'courses', 'professors', 'students'):
            self.root[key].clear()

        # re-inject everything dynamically
        for cls, key in ((Campus,    'campuses'),
                         (Faculty,   'faculties'),
                         (Course,    'courses'),
                         (Professor, 'professors'),
                         (Student,   'students')):
            items = [v for v in vars(instances).values() if isinstance(v, cls)]
            self.root[key].extend(items)

        transaction.commit()
        self.load_all()
        messagebox.showinfo("Reset Database", "Database has been reset successfully.")

    def build_students_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Students")

        cols = ('ID','Name','Year','Erasmus','Faculty','Courses')
        self.tree_students = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_students.heading(c, text=c)
            self.tree_students.column(c, width=100, anchor='center')
        self.tree_students.pack(expand=True, fill='both')
        self.tree_students.bind("<Double-1>", lambda e: self.inspect_selected("student"))

        ttk.Button(frame, text="Add Student", command=self.on_add_student).pack(pady=5)

    def build_courses_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Courses")

        cols = ('ID','Name','Students')
        self.tree_courses = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_courses.heading(c, text=c)
            self.tree_courses.column(c, width=100, anchor='center')
        self.tree_courses.pack(expand=True, fill='both')
        self.tree_courses.bind("<Double-1>", lambda e: self.inspect_selected("course"))

        ttk.Button(frame, text="Add Course", command=self.on_add_course).pack(pady=5)

    def build_professors_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Professors")

        cols = ('ID','Name','Courses')
        self.tree_professors = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_professors.heading(c, text=c)
            self.tree_professors.column(c, width=100, anchor='center')
        self.tree_professors.pack(expand=True, fill='both')
        self.tree_professors.bind("<Double-1>", lambda e: self.inspect_selected("professor"))

        ttk.Button(frame, text="Add Professor", command=self.on_add_professor).pack(pady=5)

    def build_faculties_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Faculties")

        cols = ('ID','Name','Campus')
        self.tree_faculties = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_faculties.heading(c, text=c)
            self.tree_faculties.column(c, width=120, anchor='center')
        self.tree_faculties.pack(expand=True, fill='both')
        self.tree_faculties.bind("<Double-1>", lambda e: self.inspect_selected("faculty"))

        ttk.Button(frame, text="Add Faculty", command=self.on_add_faculty).pack(pady=5)

    def load_all(self):
        self.load_students()
        self.load_courses()
        self.load_professors()
        self.load_faculties()

    def load_students(self):
        for i in self.tree_students.get_children():
            self.tree_students.delete(i)
        for s in self.root['students']:
            courses = ', '.join(c.name for c in s.get_courses())
            fac     = s.faculty.name if hasattr(s,'faculty') and s.faculty else ''
            self.tree_students.insert('', 'end', values=(
                s.student_id, s.name, s.year,
                'Yes' if s.erasmus else 'No', fac, courses
            ))

    def load_courses(self):
        for i in self.tree_courses.get_children():
            self.tree_courses.delete(i)
        for c in self.root['courses']:
            studs = ', '.join(s.name for s in c.get_students())
            self.tree_courses.insert('', 'end', values=(
                c.course_id, c.name, studs
            ))

    def load_professors(self):
        for i in self.tree_professors.get_children():
            self.tree_professors.delete(i)
        for p in self.root['professors']:
            crs = ', '.join(c.name for c in p.get_courses())
            self.tree_professors.insert('', 'end', values=(
                p.professor_id, p.name, crs
            ))

    def load_faculties(self):
        for i in self.tree_faculties.get_children():
            self.tree_faculties.delete(i)
        for f in self.root['faculties']:
            camp = f.campus.name if hasattr(f,'campus') and f.campus else ''
            self.tree_faculties.insert('', 'end', values=(
                f.faculty_id, f.name, camp
            ))

    def on_add_student(self):
        dlg = StudentForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return

        res = dlg.result
        # look for existing
        existing = next((s for s in self.root['students']
                         if s.student_id == res['student_id']), None)
        if existing:
            # just add new courses
            for name in res['courses']:
                # get or create Course object
                course = Course.all_courses.get(name) or Course(name)
                existing.add_course(course)
                if course not in self.root['courses']:
                    self.root['courses'].append(course)
        else:
            # create new Student (constructor will handle course strings)
            existing = Student(**res)
            # ensure root courses
            for course in existing.get_courses():
                if course not in self.root['courses']:
                    self.root['courses'].append(course)
            self.root['students'].append(existing)

        transaction.commit()
        self.load_students()
        self.load_courses()

    def on_add_course(self):
        dlg = CourseForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return

        res = dlg.result
        existing = next((c for c in self.root['courses']
                         if c.course_id == res['course_id']), None)
        if existing:
            existing.name = res['name']
        else:
            existing = Course(**res)
            self.root['courses'].append(existing)

        transaction.commit()
        self.load_courses()

    def on_add_professor(self):
        dlg = ProfessorForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return

        res = dlg.result
        existing = next((p for p in self.root['professors']
                         if p.professor_id == res['professor_id']), None)
        if existing:
            # update name
            existing.name = res['name']
            # add courses
            for c in res['courses']:
                course = Course.all_courses.get(c) or Course(c)
                existing.add_course(course)
                if course not in self.root['courses']:
                    self.root['courses'].append(course)
        else:
            existing = Professor(**res)
            # ensure root courses
            for course in existing.get_courses():
                if course not in self.root['courses']:
                    self.root['courses'].append(course)
            self.root['professors'].append(existing)

        transaction.commit()
        self.load_professors()
        self.load_courses()

    def on_add_faculty(self):
        dlg = FacultyForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return

        res = dlg.result
        existing = next((f for f in self.root['faculties']
                         if f.faculty_id == res['faculty_id']), None)
        if existing:
            existing.name = res['name']
            if existing.campus is not res['campus']:
                existing.campus = res['campus']
                res['campus'].add_faculty(existing)
        else:
            existing = Faculty(**res)
            self.root['faculties'].append(existing)

        transaction.commit()
        self.load_faculties()

    def inspect_selected(self, kind):
        from gui.inspector import InspectorWindow
        tree_map = {
            "student":   (self.tree_students,   self.root['students']),
            "course":    (self.tree_courses,    self.root['courses']),
            "professor": (self.tree_professors, self.root['professors']),
            "faculty":   (self.tree_faculties,  self.root['faculties']),
        }
        tree, col = tree_map[kind]
        sel = tree.selection()
        if not sel: return
        idx = tree.index(sel[0])
        InspectorWindow(self.master, col[idx], self.root)

