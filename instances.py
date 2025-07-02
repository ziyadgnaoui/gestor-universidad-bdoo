from classes import Course, Student, Professor, Faculty, Campus

#Creation of Campuses
RM = Campus("Reina Mercedes", "C01")
central = Campus("Rectorado", "C02")
san_bernardo = Campus("Ramón y Cajal", "C03")
cartuja = Campus("La Cartuja", "C04")

# Creation of Faculties
etsii = Faculty("ESCUELA TÉCNICA SUPERIOR DE INGENIERÍA INFORMÁTICA", "US01", campus=RM)
filologia = Faculty("FACULTAD DE FILOLOGÍA", "US02", campus=central)
tur_fin = Faculty("FACULTAD DE TURISMO Y FINANZAS", "US03", campus=san_bernardo)
derecho = Faculty("FACULTAD DE DERECHO", "US04", campus=san_bernardo)
etsi = Faculty("ESCUELA TÉCNICA SUPERIOR DE INGENIERÍA", "US05", campus=cartuja)
etsa = Faculty("ESCUELA TÉCNICA SUPERIOR DE ARQUITECTURA", "US06", campus=RM)
biologia = Faculty("FACULTAD DE BIOLOGÍA", "US07", campus=RM)
eco = Faculty("FACULTAD DE CIENCIAS ECONÓMICAS Y EMPRESARIALES", "US08", campus=san_bernardo)
matematicas = Faculty("FACULTAD DE MATEMÁTICAS", "US09", campus=RM)


#Creation of professors and courses


prof1 = Professor("Dr. Nieves", "P001", ["MVG"])
prof2 = Professor("Dr. Johnson", "P002", ["IA"])

# Asignaturas de la ETSII
CBD = Course("CBD", "C001")
SI = Course("SI", "C002")
IA = Course("IA", "C016")
GE = Course("GE", "C017")
MVG = Course("MVG", "C018")


prof3 = Professor("Dr. Octavio", "P003", [CBD])
prof4 = Professor("Dr. Maria Teresa", "P004")

prof4.add_course(CBD)

prof5 = Professor("Dr. Pilar", "P005", ["GE"])
prof6 = Professor("Dr. Isco", "P006", ["GE", CBD])

prof7 = Professor("Dr. Rocio", "P007", ["MVG", "SI"])
prof8 = Professor("Dr. Augustin", "P008", ["IA",SI])
prof9 = Professor("Dr. José Maria", "P009", ["MVG","IA", CBD])

# Asignaturas de la facultad de filología
Espanol = Course("Literatura Española", "C005")
Ingles = Course("English Litterature", "C006")

# Asignaturas de la ETSI
Elec = Course("Electrónicas", "C007")

# Asignaturas de la facultad de turismo y finanzas
Finanzas = Course("Finanzas", "C008")

# Asignaturas de la facultad de ciencias económicas
Marketing = Course("Marketing", "C009")
Com = Course("Comunicación", "C010")

# Asignaturas de la facultad de matemáticas
Optim = Course("Optimización", "C011")
Geom = Course("Geometría", "C012")
Maths = Course("Mathematics", "C003")
Python = Course("Introduction to Python", "C004")

# Asignaturas de la facultad de derecho
DE = Course("Derecho Empresarial", "C013")
RGPD = Course("RGPD", "C014")

# Asignaturas de la facultad de derecho
CO = Course("Química Orgánica", "C015")

#Creation of students

ziyad = Student("Ziyad", "S001", year=4, erasmus=True, courses=[CBD, SI, IA, GE, MVG], faculty=etsii)
bruno = Student("Bruno", "S002", year=4, erasmus=True, faculty=etsii)
franco = Student("Franco", "S003", year=4, erasmus=True, faculty=etsii)
simon = Student("Simon", "S004", year=3, erasmus=True, faculty=filologia)
mido = Student("Mido", "S005", faculty=tur_fin) 
samia = Student("Samia", "S006", year=2, faculty=eco)
alberto = Student("Alberto", "S007", year=3, faculty=etsi)
paloma = Student("Paloma", "S008", year=5, faculty=matematicas)
lotta = Student("Lotta", "S009", year=4, erasmus=True, faculty=derecho)
nisrine = Student("Nisrine", "S010", year=3, faculty=biologia)
pedro = Student("Pedro", "S011", year=5, faculty=etsa)

