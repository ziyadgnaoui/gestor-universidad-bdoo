import tkinter as tk
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction
from persistent.list import PersistentList

from classes import Student, Course, Professor, Faculty, Campus
import instances
from gui.main_window import MainWindow

def main():
    storage = FileStorage('university.fs')
    db      = DB(storage)
    conn    = db.open()
    root    = conn.root()

    # créer les containers si besoin
    for key in ('campuses','faculties','courses','professors','students'):
        if key not in root:
            root[key] = PersistentList()

    # injection initiale (une seule fois)
    if not root['campuses']:
        # campuses
        caps = [v for v in vars(instances).values() if isinstance(v, Campus)]
        root['campuses'].extend(caps)
        # faculties
        facs = [v for v in vars(instances).values() if isinstance(v, Faculty)]
        root['faculties'].extend(facs)
        # courses
        crs  = [v for v in vars(instances).values() if isinstance(v, Course)]
        root['courses'].extend(crs)
        # professors
        profs = [v for v in vars(instances).values() if isinstance(v, Professor)]
        root['professors'].extend(profs)
        # students
        studs = [v for v in vars(instances).values() if isinstance(v, Student)]
        root['students'].extend(studs)

        transaction.commit()

    root_tk = tk.Tk()
    root_tk.title("Gestion Université (BDOO)")
    MainWindow(root_tk, root)
    root_tk.mainloop()

    conn.close()
    db.close()

if __name__ == '__main__':
    main()

