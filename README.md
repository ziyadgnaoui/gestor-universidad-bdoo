# gestor-universidad-bdoo

University Management Mini-App (OODB) for the “Complementos de Bases de Datos” course  
Author: Ziyad Gnaoui

---

## Table of Contents

1. [Description](#description)  
2. [Features](#features)  
3. [Architecture & Technologies](#architecture--technologies)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Project Structure](#project-structure)  
7. [Tests](#tests)  

---

## Description

This is a **mini-application** that models a simple university management system on top of an **object-oriented database** (ZODB).  
You can create and list campuses, faculties, courses, professors and students, persist them automatically, and explore their relationships via a graphical interface.

---

## Features

- **CRUD-lite** for:  
  - Campuses  
  - Faculties  
  - Courses  
  - Professors  
  - Students (if you add a student with an existing ID, only their course list is updated)  
- **Automatic persistence** using ZODB  
- **Tkinter GUI** with tabs, modal forms and a dynamic inspector  
- **Reset Database** button to wipe all data and reload the original sample instances (from `instances.py`)

---

## Architecture & Technologies

- **Python 3.10+**  
- **ZODB** (Zope Object Database) for persistence  
- **Tkinter** for the user interface  
- **persistent.list.PersistentList** as the root container  
- **unittest** for automated tests  
- **`instances.py`** holds the sample objects used to reset the database

---

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/your-username/gestor-universidad-bdoo.git
   cd gestor-universidad-bdoo

2. (Optional) Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies:
    ``` bash
    pip install requirements.txt

## Usage

1. Start the application:
    ```bash
    python3 app.py

2. The window is organized into tabs:

        Students

        Courses

        Professors

        Faculties

3. Add a student via the “Add Student” button:

        Select one or more existing courses

        Or type a new course name into “Other course”

        If the student ID already exists, only their course list is updated

4. Reset the database at any time with the “Reset Database” button — this restores the original objects from instances.py.

## Project Structure

```bash
gestor-universidad-bdoo/
├── app.py                  # Application entry point
├── classes.py              # Domain model (Campus, Faculty, Course, Professor, Student)
├── instances.py            # Sample instances for reset
├── gui/
│   ├── main_window.py      # Main Tkinter Notebook interface
│   ├── forms.py            # Modal forms for adding objects
│   └── inspector.py        # Dynamic object inspector window
├── tests.py                # Unit tests covering logic & persistence
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Tests

Run the full test suite before committing:

```bash
python3 tests.py
```

All tests should pass.