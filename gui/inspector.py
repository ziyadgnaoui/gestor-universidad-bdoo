# gui/inspector.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import transaction

from classes import Student, Course, Professor, Faculty

class InspectorWindow(tk.Toplevel):
    def __init__(self, master, obj, root):
        super().__init__(master)
        self.obj = obj
        self.root = root
        self.title(f"Inspector: {type(obj).__name__}")
        self.resizable(False, False)

        # Attributes frame
        frm = ttk.LabelFrame(self, text="Attributes")
        frm.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tree_attr = ttk.Treeview(frm, columns=("attr","value"), show="headings", height=8)
        self.tree_attr.heading("attr", text="Attribute")
        self.tree_attr.heading("value", text="Value")
        self.tree_attr.column("attr", width=120, anchor="w")
        self.tree_attr.column("value", width=200, anchor="w")
        self.tree_attr.pack(expand=True, fill="both")
        self.populate_attributes()

        # Footer with dynamic buttons + delete
        footer = ttk.Frame(self)
        footer.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
        footer.columnconfigure(0, weight=1)

        # Dynamic add-buttons by type
        col = 0
        if isinstance(obj, Student):
            btn = ttk.Button(footer, text="Add Course", command=self.on_add_course_to_student)
            btn.grid(row=0, column=col, sticky="ew", padx=5); col += 1

        elif isinstance(obj, Course):
            btn1 = ttk.Button(footer, text="Add Student",   command=self.on_add_student_to_course)
            btn2 = ttk.Button(footer, text="Add Professor", command=self.on_add_professor_to_course)
            btn1.grid(row=0, column=col, sticky="ew", padx=5); col += 1
            btn2.grid(row=0, column=col, sticky="ew", padx=5); col += 1

        elif isinstance(obj, Professor):
            btn = ttk.Button(footer, text="Add Course", command=self.on_add_course_to_professor)
            btn.grid(row=0, column=col, sticky="ew", padx=5); col += 1

        # No dynamic add-button for Faculty

        # Delete button for all types
        del_btn = ttk.Button(footer, text="Delete", command=self.on_delete)
        del_btn.grid(row=0, column=col, sticky="ew", padx=5)

    def populate_attributes(self):
        for row in self.tree_attr.get_children():
            self.tree_attr.delete(row)
        for attr, val in vars(self.obj).items():
            self.tree_attr.insert("", "end", values=(attr, repr(val)))

    def on_add_course_to_student(self):
        name = simpledialog.askstring("Add Course", "Course name:")
        if not name: return
        course = next((c for c in self.root['courses'] if c.name == name), None)
        if not course:
            course = Course(name)
            self.root['courses'].append(course)
        self.obj.add_course(course)
        transaction.commit()
        self.populate_attributes()
        self.master.event_generate("<<DataChanged>>")

    def on_add_course_to_professor(self):
        name = simpledialog.askstring("Add Course", "Course name:")
        if not name: return
        course = next((c for c in self.root['courses'] if c.name == name), None)
        if not course:
            course = Course(name)
            self.root['courses'].append(course)
        self.obj.add_course(course)
        transaction.commit()
        self.populate_attributes()
        self.master.event_generate("<<DataChanged>>")

    def on_add_student_to_course(self):
        name = simpledialog.askstring("Add Student", "Student name:")
        if not name: return
        stud = next((s for s in self.root['students'] if s.name == name), None)
        if not stud:
            messagebox.showerror("Not found", f"No student named '{name}'")
            return
        self.obj.add_student(stud)
        transaction.commit()
        self.populate_attributes()
        self.master.event_generate("<<DataChanged>>")

    def on_add_professor_to_course(self):
        name = simpledialog.askstring("Add Professor", "Professor name:")
        if not name: return
        prof = next((p for p in self.root['professors'] if p.name == name), None)
        if not prof:
            messagebox.showerror("Not found", f"No professor named '{name}'")
            return
        self.obj.add_professor(prof)
        transaction.commit()
        self.populate_attributes()
        self.master.event_generate("<<DataChanged>>")

    def on_delete(self):
        """Delete this object and clean up all bidirectional links."""
        # Determine container key and inverse cleanup
        if isinstance(self.obj, Student):
            key = 'students'
            # remove student from all its courses
            for c in list(self.obj.courses):
                c.students.remove(self.obj)

        elif isinstance(self.obj, Course):
            key = 'courses'
            # remove course from all its students and professors
            for s in list(self.obj.students):
                s.courses.remove(self.obj)
            for p in list(self.obj.professors):
                p.courses.remove(self.obj)

        elif isinstance(self.obj, Professor):
            key = 'professors'
            # remove professor from all its courses
            for c in list(self.obj.courses):
                c.professors.remove(self.obj)

        elif isinstance(self.obj, Faculty):
            key = 'faculties'
            # dissociate faculty from its campus
            if hasattr(self.obj, 'campus') and self.obj.campus:
                self.obj.campus.faculties.remove(self.obj)
            # remove faculty reference from students
            for s in list(self.obj.students):
                s.faculty = None

        else:
            return

        # ask confirmation
        if not messagebox.askyesno("Delete",
                                   f"Are you sure you want to delete this {type(self.obj).__name__}?"):
            return

        # remove from root and commit
        try:
            self.root[key].remove(self.obj)
            transaction.commit()
            # notify main window to reload all tabs
            self.master.event_generate("<<DataChanged>>")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Could not delete: not found in database.")