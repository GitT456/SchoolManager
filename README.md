# 🎓 School Manager System

School Manager System is a Python-based application designed to manage various aspects of a school, including students, employees, classrooms, subjects, and library resources.  
The project is built with a modular architecture and follows Object-Oriented Programming (OOP) principles to ensure scalability, maintainability, and clarity.

---

## 📌 Project Features

- Student management
- School employee management
- Classroom management
- Subject management
- Library members and items management
- Object-Oriented Design (OOP)
- SQLite database integration
- Modular UI layer
- Service layer for business logic
- Logging system for tracking activities
- Clean and extensible project structure

---

## 🏗️ Project Structure

```text
school_manager/
│
├── main.py
│
├── ui/
│   ├── ClassRoom_ui.py
│   ├── lib_item_ui.py
│   ├── member_ui.py
│   ├── SchoolEmployee_ui.py
│   ├── Student_ui.py
│   └── Subject_ui.py
│
├── models/
│   ├── ClassRoom.py
│   ├── lib_item.py
│   ├── member.py
│   ├── Person.py
│   ├── SchoolEmployee.py
│   ├── Student.py
│   └── Subject.py
│
├── services/
│   ├── Library_Service.py
│   └── School_Service.py
│
├── database/
│   ├── db.py
│   └── school.db
│
├── log/
│   └── School_Manager_System_log.txt
│
├── images/
│   └── background.png
│
├── venv312/
│
├── requirements.txt
│
└── README.md
```

---

## 🧠 Architecture Overview

This project follows a layered architecture similar to **MVC (Model–View–Controller)**:

- **Models** → Data structure and core entities  
- **UI** → User interaction layer  
- **Services** → Business logic  
- **Database** → Data persistence  

---

## ▶️ Entry Point

### `main.py`

The main entry point of the application.  
It initializes the system, connects UI components with services, and starts the program execution.

---

## 🎨 UI Layer (`ui/`)

This directory contains user interface modules responsible for interacting with users.

| File | Description |
|----|------------|
| Student_ui.py | Student management interface |
| SchoolEmployee_ui.py | School employee management |
| ClassRoom_ui.py | Classroom management |
| Subject_ui.py | Subject management |
| member_ui.py | Library member management |
| lib_item_ui.py | Library items management |

---

## 🧱 Models Layer (`models/`)

This directory contains core domain models implemented using OOP concepts.

| File | Description |
|----|------------|
| Person.py | Base class for people |
| Student.py | Student entity |
| SchoolEmployee.py | Employee entity |
| ClassRoom.py | Classroom entity |
| Subject.py | Subject entity |
| member.py | Library member |
| lib_item.py | Library item |

Each model encapsulates its own attributes and behaviors.

---

## ⚙️ Services Layer (`services/`)

Contains business logic and application rules.

| File | Description |
|----|------------|
| School_Service.py | School-related operations |
| Library_Service.py | Library-related operations |

Services act as a bridge between UI and database layers.

---

## 🗄️ Database Layer (`database/`)

Responsible for data persistence using SQLite.

| File | Description |
|----|------------|
| db.py | Database connection and queries |
| school.db | SQLite database file |

---

## 📝 Logging (`log/`)

- School_Manager_System_log.txt  
Used to record system activities, events, and errors for debugging and monitoring.

---

## 🖼️ Assets (`images/`)

Contains graphical assets used in the UI.

- background.png

---

## 🧪 Virtual Environment (`venv312/`)

A Python virtual environment used to manage project dependencies.

---

## 📦 Requirements

All required dependencies are listed in `requirements.txt`.

Example:
```txt
sqlite3
tkinter
```

Add any additional libraries here if the project grows.

---

## 🚀 How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/school_manager.git
cd school_manager
```

### 2️⃣ Activate virtual environment

**Windows**
```bash
venv312\Scripts\activate
```

**Linux / macOS**
```bash
source venv312/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application
```bash
python main.py
```

---

## 🔮 Future Improvements

- Authentication system (Login / Roles)
- Grading and exam management
- Parent management
- Advanced GUI (PyQt / CustomTkinter)
- Export reports (PDF / Excel)
- REST API integration

---

## 🧑‍💻 Technologies Used

- Python 3.12
- SQLite
- Object-Oriented Programming (OOP)
- Modular Architecture
- Tkinter (if used for UI)

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it for educational and personal purposes.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to submit issues or pull requests to improve the project.

---

### ⭐ If you like this project, don’t forget to give it a star on GitHub!
