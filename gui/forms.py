# gui/forms.py

import tkinter as tk
from tkinter import ttk

class StudentForm(tk.Toplevel):
    def __init__(self, master, root):
        super().__init__(master)
        self.title("Add Student")
        self.result = None
        self.root = root

        # Name
        ttk.Label(self, text="Name       :").grid(row=0, column=0, sticky='e')
        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=0, column=1, padx=5, pady=2)

        # ID
        ttk.Label(self, text="Student ID :").grid(row=1, column=0, sticky='e')
        self.ent_id = ttk.Entry(self)
        self.ent_id.grid(row=1, column=1, padx=5, pady=2)

        # Year
        ttk.Label(self, text="Year       :").grid(row=2, column=0, sticky='e')
        self.spin_year = ttk.Spinbox(self, from_=1, to=10, width=5)
        self.spin_year.set(1)
        self.spin_year.grid(row=2, column=1, padx=5, pady=2, sticky='w')

        # Erasmus
        self.var_erasmus = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Erasmus", variable=self.var_erasmus).grid(row=3, column=1, sticky='w')

        # Faculty
        ttk.Label(self, text="Faculty    :").grid(row=4, column=0, sticky='e')
        fac_names = [f.name for f in root['faculties']]
        self.cmb_fac = ttk.Combobox(self, values=fac_names, state='readonly')
        if fac_names:
            self.cmb_fac.current(0)
        self.cmb_fac.grid(row=4, column=1, padx=5, pady=2, sticky='w')

        # Courses Listbox (multi-select)
        ttk.Label(self, text="Select Courses:").grid(row=5, column=0, sticky='ne')
        self.lst_courses = tk.Listbox(self, selectmode='multiple', height=6)
        for c in root['courses']:
            self.lst_courses.insert('end', c.name)
        self.lst_courses.grid(row=5, column=1, padx=5, pady=2, sticky='w')

        # Other course
        ttk.Label(self, text="Other course:").grid(row=6, column=0, sticky='e')
        self.ent_other = ttk.Entry(self)
        self.ent_other.grid(row=6, column=1, padx=5, pady=2, sticky='w')

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="OK",     command=self.on_ok).pack(side='right', padx=5)

    def on_ok(self):
        # Récupérer les valeurs
        name      = self.ent_name.get().strip()
        sid       = self.ent_id.get().strip()
        year      = int(self.spin_year.get())
        erasmus   = self.var_erasmus.get()
        fac_name  = self.cmb_fac.get()
        # trouver l'instance Faculty
        faculty   = next((f for f in self.root['faculties'] if f.name==fac_name), None)

        # courses sélectionnés
        sel_idxs  = self.lst_courses.curselection()
        courses   = [ self.lst_courses.get(i) for i in sel_idxs ]
        # autre cours
        other     = self.ent_other.get().strip()
        if other:
            courses.append(other)

        self.result = {
            'name':     name,
            'student_id': sid,
            'year':     year,
            'erasmus':  erasmus,
            'faculty':  faculty,
            'courses':  courses
        }
        self.destroy()


class CourseForm(tk.Toplevel):
    def __init__(self, master, root):
        super().__init__(master)
        self.title("Nouveau Course")
        self.result = None
        ttk.Label(self, text="Nom  :").grid(row=0,column=0)
        self.ent_name = ttk.Entry(self); self.ent_name.grid(row=0,column=1)
        ttk.Label(self, text="ID   :").grid(row=1,column=0)
        self.ent_id   = ttk.Entry(self); self.ent_id.grid(row=1,column=1)
        ttk.Button(self, text="Annuler", command=self.destroy).grid(row=2,column=0)
        ttk.Button(self, text="OK",      command=self.on_ok).grid(row=2,column=1)

    def on_ok(self):
        self.result = {
            'name':     self.ent_name.get().strip(),
            'course_id': self.ent_id.get().strip()
        }
        self.destroy()


class ProfessorForm(tk.Toplevel):
    def __init__(self, master, root):
        super().__init__(master)
        self.title("Nouveau Professor")
        self.result = None
        ttk.Label(self, text="Nom  :").grid(row=0,column=0)
        self.ent_name = ttk.Entry(self); self.ent_name.grid(row=0,column=1)
        ttk.Label(self, text="ID   :").grid(row=1,column=0)
        self.ent_id   = ttk.Entry(self); self.ent_id.grid(row=1,column=1)
        ttk.Button(self, text="Annuler", command=self.destroy).grid(row=2,column=0)
        ttk.Button(self, text="OK",      command=self.on_ok).grid(row=2,column=1)

    def on_ok(self):
        self.result = {
            'name':         self.ent_name.get().strip(),
            'professor_id': self.ent_id.get().strip(),
            'courses':      []  # plus tard, choisir dans root['courses']
        }
        self.destroy()

class FacultyForm(tk.Toplevel):
    def __init__(self, master, root):
        super().__init__(master)
        self.title("New Faculty")
        self.result = None
        self.root = root

        # Name
        ttk.Label(self, text="Name     :").grid(row=0, column=0, sticky='e')
        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=0, column=1, padx=5, pady=2)

        # ID
        ttk.Label(self, text="ID       :").grid(row=1, column=0, sticky='e')
        self.ent_id = ttk.Entry(self)
        self.ent_id.grid(row=1, column=1, padx=5, pady=2)

        # Campus (combobox)
        ttk.Label(self, text="Campus   :").grid(row=2, column=0, sticky='e')
        campus_names = [campus.name for campus in root['campuses']]
        self.cmb_campus = ttk.Combobox(self, values=campus_names, state='readonly')
        self.cmb_campus.grid(row=2, column=1, padx=5, pady=2)
        if campus_names:
            self.cmb_campus.current(0)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="OK",     command=self.on_ok).pack(side='right', padx=5)

    def on_ok(self):
        campus_name = self.cmb_campus.get()
        # find the Campus instance by name
        campus = next((c for c in self.root['campuses'] if c.name == campus_name), None)
        self.result = {
            'name':     self.ent_name.get().strip(),
            'faculty_id': self.ent_id.get().strip(),
            'campus':   campus
        }
        self.destroy()