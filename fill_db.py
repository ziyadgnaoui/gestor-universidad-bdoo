import random
from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction

from classes import Student
from instances import etsii

DB_PATH = 'university.fs'
COURSE_NAMES = ["CBD", "IA", "SI", "Python", "GE", "MVG"]
NUM_STUDENTS = 100           

# List of common Spanish first and last names
FIRST_NAMES = [
    "Alejandro", "Beatriz", "Carlos", "Daniela", "Eduardo", "Francisca",
    "Gonzalo", "Helena", "Ignacio", "Javier", "Lucía", "María",
    "Nicolas", "Pablo", "Queralt", "Raúl", "Sofía", "Tomás",
    "Vicente", "Ximena", "Yolanda", "Zacarías"
]
LAST_NAMES = [
    "García", "Martínez", "López", "Sánchez", "Pérez", "Gómez",
    "Rodríguez", "Fernández", "Jiménez", "Ruiz", "Hernández", "Díaz",
    "Morales", "Álvarez", "Torres", "Romero", "Vargas", "Navarro"
]

def random_spanish_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"

def main():
    # Open the ZODB database
    storage = FileStorage(DB_PATH)
    db = DB(storage)
    conn = db.open()
    root = conn.root()

    # Ensure the 'students' container exists
    if 'students' not in root:
        from persistent.list import PersistentList
        root['students'] = PersistentList()

    # Collect the ETSII courses by name
    available = { c.name: c for c in root['courses'] if c.name in COURSE_NAMES }

    # Generate and append new students
    for i in range(1, NUM_STUDENTS+1):
        name = random_spanish_name()
        sid  = f"S{100 + i:03d}"  # e.g. S101, S102...
        # pick 1–4 random courses from the list
        chosen = random.sample(COURSE_NAMES, k=random.randint(1,4))
        courses = [ available[c] for c in chosen if c in available ]
        # random year and Erasmus flag
        year = random.randint(1,5)
        erasmus = random.choice([True, False])

        # avoid duplicate IDs
        if any(s.student_id == sid for s in root['students']):
            print(f"Skipping duplicate ID {sid}")
            continue

        stu = Student(name, sid, year=year, erasmus=erasmus, courses=courses,
                      faculty=etsii)
        root['students'].append(stu)
        print(f"Created {stu} with courses {[c.name for c in courses]}")

    # Commit and close
    transaction.commit()
    conn.close()
    db.close()
    print("Done. Database populated with auto-generated students.")

if __name__ == '__main__':
    main()
