import unittest
from classes import Student, Professor, Course, Faculty, Campus
from ZODB import DB
import transaction
from ZODB.DemoStorage import DemoStorage
from persistent.list import PersistentList

class TestUniversitySystem(unittest.TestCase):

    def setUp(self):
        # base in-memory storage to avoid file locks
        self.storage = DemoStorage()
        self.db      = DB(self.storage)
        self.conn    = self.db.open()
        self.root    = self.conn.root()

        # instantiate the persistent containers if needed
        if 'campuses'   not in self.root: self.root['campuses']   = PersistentList()
        if 'faculties'  not in self.root: self.root['faculties']  = PersistentList()
        if 'courses'    not in self.root: self.root['courses']    = PersistentList()
        if 'professors' not in self.root: self.root['professors'] = PersistentList()
        if 'students'   not in self.root: self.root['students']   = PersistentList()

        # create domain objects
        self.campus   = Campus("Main Campus", "C001")
        self.faculty  = Faculty("Faculty of CS", "F001", campus=self.campus)
        self.course1  = Course("AI", "AI001")
        self.course2  = Course("ML", "ML001")
        self.prof1    = Professor("Dr. Smith", "P001", courses=[self.course1, self.course2])
        self.prof2    = Professor("Dr. Jones", "P002", courses=[self.course2])
        self.student1 = Student("Alice", "S001", year=3, courses=[self.course1], erasmus=False, faculty=self.faculty)
        self.student2 = Student("Bob",   "S002", year=2, courses=[self.course2], erasmus=True,  faculty=self.faculty)

        # persist initial state
        self.root['campuses'].append(self.campus)
        self.root['faculties'].append(self.faculty)
        self.root['courses'].extend([self.course1, self.course2])
        self.root['professors'].extend([self.prof1, self.prof2])
        self.root['students'].extend([self.student1, self.student2])
        transaction.commit()

    def tearDown(self):
        self.conn.close()
        self.db.close()

    def test_initial_persistence(self):
        self.assertEqual(len(self.root['campuses']),   1)
        self.assertEqual(len(self.root['faculties']),  1)
        self.assertEqual(len(self.root['courses']),    2)
        self.assertEqual(len(self.root['professors']), 2)
        self.assertEqual(len(self.root['students']),   2)

    def test_new_persistence(self):
        self.student1.add_course(self.course2)
        transaction.commit()
        self.conn.close()
        self.db.close()
        
        self.assertIn(self.course2, self.root['students'][0].get_courses())



    def test_bidirectional_student_course(self):
        student3 = Student("Charlie", "S003", year=1, courses=[self.course1], erasmus=False, faculty=self.faculty)
        self.course1.add_student(student3)
        self.root['students'].append(student3)
        transaction.commit()

        self.assertIn(student3, self.course1.get_students())
        self.assertIn(self.course1, student3.get_courses())
        self.assertEqual(len(self.root['students']), 3)

    def test_bidirectional_professor_course(self):
        self.course1.add_professor(self.prof2)
        transaction.commit()

        self.assertIn(self.prof2, self.course1.get_professors())
        self.assertIn(self.course1, self.prof2.get_courses())

    def test_faculty_students(self):
        prev = len(self.faculty.get_students())
        self.faculty.add_student(self.student1)
        transaction.commit()
        self.assertEqual(len(self.faculty.get_students()), prev)

    def test_campus_faculties(self):
        fac2 = Faculty("Arts", "F002", campus=self.campus)
        self.root['faculties'].append(fac2)
        transaction.commit()
        self.assertIn(fac2, self.campus.get_faculties())
        self.assertEqual(len(self.root['faculties']), 2)

if __name__ == '__main__':
    unittest.main()
