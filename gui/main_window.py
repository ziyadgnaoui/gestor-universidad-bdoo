# gui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
import transaction
import instances
import importlib

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

        # Bind a custom event so Inspector can request UI refresh
        master.bind("<<DataChanged>>", lambda e: self.load_all())

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

        # Reload fresh instances
        importlib.reload(instances)

        for key in ('campuses', 'faculties', 'courses', 'professors', 'students'):
            self.root[key].clear()

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
            self.tree_students.column(c, width=120, anchor='center')
        self.tree_students.pack(expand=True, fill='both')
        ttk.Button(frame, text="Add Student", command=self.on_add_student).pack(pady=5)
        self.tree_students.bind("<Double-1>", lambda e: self.inspect_selected("student"))

    def build_courses_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Courses")
        cols = ('ID','Name','Students','Professors')
        self.tree_courses = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_courses.heading(c, text=c)
            self.tree_courses.column(c, width=120, anchor='center')
        self.tree_courses.pack(expand=True, fill='both')
        ttk.Button(frame, text="Add Course", command=self.on_add_course).pack(pady=5)
        self.tree_courses.bind("<Double-1>", lambda e: self.inspect_selected("course"))

    def build_professors_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Professors")
        cols = ('ID','Name','Courses')
        self.tree_professors = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_professors.heading(c, text=c)
            self.tree_professors.column(c, width=120, anchor='center')
        self.tree_professors.pack(expand=True, fill='both')
        ttk.Button(frame, text="Add Professor", command=self.on_add_professor).pack(pady=5)
        self.tree_professors.bind("<Double-1>", lambda e: self.inspect_selected("professor"))

    def build_faculties_tab(self):
        frame = ttk.Frame(self)
        self.add(frame, text="Faculties")
        cols = ('ID','Name','Campus')
        self.tree_faculties = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            self.tree_faculties.heading(c, text=c)
            self.tree_faculties.column(c, width=150, anchor='center')
        self.tree_faculties.pack(expand=True, fill='both')
        ttk.Button(frame, text="Add Faculty", command=self.on_add_faculty).pack(pady=5)
        self.tree_faculties.bind("<Double-1>", lambda e: self.inspect_selected("faculty"))

    def load_all(self):
        self.load_students()
        self.load_courses()
        self.load_professors()
        self.load_faculties()

    def load_students(self):
        for i in self.tree_students.get_children():
            self.tree_students.delete(i)
        for s in self.root['students']:
            fac = s.faculty.name if hasattr(s,'faculty') and s.faculty else ''
            courses = ', '.join(c.name for c in s.get_courses())
            self.tree_students.insert('', 'end', values=(
                s.student_id, s.name, s.year,
                'Yes' if s.erasmus else 'No',
                fac, courses
            ))

    def load_courses(self):
        for i in self.tree_courses.get_children():
            self.tree_courses.delete(i)
        for c in self.root['courses']:
            studs = ', '.join(s.name for s in c.get_students())
            profs = ', '.join(p.name for p in c.get_professors())
            self.tree_courses.insert('', 'end', values=(
                c.course_id, c.name, studs, profs
            ))

    def load_professors(self):
        for i in self.tree_professors.get_children():
            self.tree_professors.delete(i)
        for p in self.root['professors']:
            courses = ', '.join(c.name for c in p.get_courses())
            self.tree_professors.insert('', 'end', values=(
                p.professor_id, p.name, courses
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
        exists = next((s for s in self.root['students']
                       if s.student_id == res['student_id']), None)
        if exists:
            messagebox.showwarning("Student exists",
                                   f"Student {res['student_id']} already exists.")
        else:
            new_stu = Student(**res)
            for c in new_stu.get_courses():
                if c not in self.root['courses']:
                    self.root['courses'].append(c)
            self.root['students'].append(new_stu)
            transaction.commit()
            self.load_students()
            self.load_courses()

    def on_add_course(self):
        dlg = CourseForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return
        res = dlg.result
        exists = next((c for c in self.root['courses']
                       if c.course_id == res['course_id']), None)
        if exists:
            messagebox.showwarning("Course exists",
                                   f"Course {res['course_id']} already exists.")
        else:
            self.root['courses'].append(Course(**res))
            transaction.commit()
            self.load_courses()

    def on_add_professor(self):
        dlg = ProfessorForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return
        res = dlg.result
        exists = next((p for p in self.root['professors']
                       if p.professor_id == res['professor_id']), None)
        if exists:
            messagebox.showwarning("Professor exists",
                                   f"Professor {res['professor_id']} already exists.")
        else:
            prof = Professor(**res)
            for c in prof.get_courses():
                if c not in self.root['courses']:
                    self.root['courses'].append(c)
            self.root['professors'].append(prof)
            transaction.commit()
            self.load_professors()
            self.load_courses()

    def on_add_faculty(self):
        dlg = FacultyForm(self.master, self.root)
        self.master.wait_window(dlg)
        if not dlg.result:
            return
        res = dlg.result
        exists = next((f for f in self.root['faculties']
                       if f.faculty_id == res['faculty_id']), None)
        if exists:
            messagebox.showwarning("Faculty exists",
                                   f"Faculty {res['faculty_id']} already exists.")
        else:
            self.root['faculties'].append(Faculty(**res))
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
        tree, coll = tree_map[kind]
        sel = tree.selection()
        if not sel:
            return
        obj = coll[tree.index(sel[0])]
        InspectorWindow(self.master, obj, self.root)
