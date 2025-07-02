# gui/inspector.py

import tkinter as tk
from tkinter import ttk, messagebox
import transaction
import inspect

class InspectorWindow(tk.Toplevel):
    def __init__(self, master, obj, root):
        super().__init__(master)
        self.title(f"Inspector: {obj.__class__.__name__}")
        self.obj = obj
        self.root = root

        # ── ATTRIBUTES FRAME ──
        frm_attr = ttk.LabelFrame(self, text="Attributes")
        frm_attr.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_attr = ttk.Treeview(frm_attr, columns=("value",), show="headings")
        self.tree_attr.heading("value", text="Value")
        self.tree_attr.column("value", width=200)
        self.tree_attr.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frm_attr, orient="vertical", command=self.tree_attr.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_attr.configure(yscrollcommand=scrollbar.set)

        # ── METHODS FRAME ──
        frm_meth = ttk.LabelFrame(self, text="Methods")
        frm_meth.pack(fill="both", expand=True, padx=10, pady=5)

        self.lst_methods = tk.Listbox(frm_meth, height=6)
        self.lst_methods.pack(side="left", fill="both", expand=True)
        scrollbar2 = ttk.Scrollbar(frm_meth, orient="vertical", command=self.lst_methods.yview)
        scrollbar2.pack(side="right", fill="y")
        self.lst_methods.configure(yscrollcommand=scrollbar2.set)

        # ── DYNAMIC FIELD FRAME ──
        frm_add = ttk.LabelFrame(self, text="Add Dynamic Field")
        frm_add.pack(fill="x", expand=False, padx=10, pady=5)
        ttk.Label(frm_add, text="Name:").grid(row=0, column=0, sticky="e")
        self.ent_field = ttk.Entry(frm_add)
        self.ent_field.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(frm_add, text="Value:").grid(row=1, column=0, sticky="e")
        self.ent_value = ttk.Entry(frm_add)
        self.ent_value.grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(frm_add, text="Add", command=self.on_add_field).grid(row=2, column=0, columnspan=2, pady=5)

        # ── REFERENCES FRAME ──
        frm_nav = ttk.LabelFrame(self, text="Navigate References")
        frm_nav.pack(fill="both", expand=True, padx=10, pady=5)
        self.lst_refs = tk.Listbox(frm_nav, height=6)
        self.lst_refs.pack(side="left", fill="both", expand=True)
        scrollbar3 = ttk.Scrollbar(frm_nav, orient="vertical", command=self.lst_refs.yview)
        scrollbar3.pack(side="right", fill="y")
        self.lst_refs.configure(yscrollcommand=scrollbar3.set)

        ttk.Button(self, text="Inspect Selected Ref", command=self.on_inspect_ref).pack(pady=5)

        # Initial population
        self.populate()

    def populate(self):
        """Reload attributes, methods and references in the inspector."""
        # — Attributes —
        try:
            if hasattr(self, 'tree_attr') and self.tree_attr.winfo_exists():
                # clear old
                for row in self.tree_attr.get_children():
                    self.tree_attr.delete(row)
                # only objects with __dict__ have vars()
                attrs = vars(self.obj) if hasattr(self.obj, '__dict__') else {}
                for attr, val in attrs.items():
                    self.tree_attr.insert("", "end", text=attr, values=(repr(val),))
        except tk.TclError:
            # widget no longer exists
            pass

        # — Methods —
        self.lst_methods.delete(0, 'end')
        for name, func in inspect.getmembers(self.obj.__class__, predicate=inspect.isfunction):
            self.lst_methods.insert('end', name + '()')

        # — References —
        self.lst_refs.delete(0, 'end')
        attrs = vars(self.obj) if hasattr(self.obj, '__dict__') else {}
        for attr, val in attrs.items():
            # skip strings
            if hasattr(val, '__iter__') and not isinstance(val, (str, bytes)):
                disp = f"{attr}: {type(val).__name__}"
                self.lst_refs.insert('end', disp)
            elif hasattr(val, '__dict__'):
                disp = f"{attr}: {type(val).__name__}"
                self.lst_refs.insert('end', disp)

    def on_add_field(self):
        """Add a new dynamic field to the object and commit."""
        name = self.ent_field.get().strip()
        raw  = self.ent_value.get().strip()
        if not name:
            return
        setattr(self.obj, name, raw)
        transaction.commit()
        messagebox.showinfo("Field Added", f"Added field '{name}' = '{raw}'")
        self.populate()

    def on_inspect_ref(self):
        """Inspect the selected reference (either an iterable of objects or a single object)."""
        sel = self.lst_refs.curselection()
        if not sel:
            return
        entry = self.lst_refs.get(sel[0])
        attr  = entry.split(":",1)[0].strip()
        val   = getattr(self.obj, attr)
        # for collections of objects
        if hasattr(val, '__iter__') and not isinstance(val, (str, bytes)):
            for item in val:
                InspectorWindow(self, item, self.root)
        # single object
        elif hasattr(val, '__dict__'):
            InspectorWindow(self, val, self.root)
        # primitives are not inspectable further
