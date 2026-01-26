# ⚡ FastAPI Todo API (Python)

A lightweight RESTful API built with **Python** and **FastAPI** that provides full **CRUD** functionality for managing Todo items.  
This project demonstrates modern backend development practices including request validation, clean routing, and structured data models using **Pydantic**.

The application uses **in-memory storage**, making it ideal for learning, academic projects, and rapid API prototyping.

---

## 🚀 Features

- Create new Todo items  
- Retrieve a Todo by ID  
- Retrieve all Todos  
- Limit results using query parameters  
- Update existing Todos (partial updates supported)  
- Delete Todos  
- Request and response validation with Pydantic  
- Priority system using Enum (**LOW**, **MEDIUM**, **HIGH**)  
- Auto-generated API documentation  

---

## 🧱 Tech Stack

- Python  
- FastAPI  
- Pydantic  
- Uvicorn  

---

## 📦 Installation

### Create virtual environment (recommended)

python -m venv venv

### Activate it

source venv/bin/activate    # macOS / Linux  
venv\Scripts\activate       # Windows  

### Install dependencies

pip install fastapi uvicorn

---

## ▶️ Running the Application

If the file is named `main.py` and the FastAPI instance is defined as:

api = FastAPI()

Run the application with:

uvicorn main:api --reload

The API will be available at:

http://127.0.0.1:8000

---

## 📚 API Documentation

FastAPI provides automatic interactive documentation:

- Swagger UI: http://127.0.0.1:8000/docs  
- ReDoc: http://127.0.0.1:8000/redoc  

---

## 🔗 API Endpoints

### Get all Todos

GET /todos  

Optional query parameter:

GET /todos?first_n=3

---

### Get Todo by ID

GET /todos/{todo_id}

---

### Create a new Todo

POST /todos

Request body example:

{
  "todo_name": "Study",
  "todo_description": "Prepare for upcoming exam",
  "priority": 1
}

Priority values:

1 → HIGH  
2 → MEDIUM  
3 → LOW  

---

### Update a Todo

PUT /todos/{todo_id}

Example:

{
  "todo_description": "Read chapter 6",
  "priority": 2
}

---

### Delete a Todo

DELETE /todos/{todo_id}

---

## 🧪 Sample Data

The application initializes with a predefined list of Todo items stored in memory, allowing immediate testing without additional setup.

---

## ⚠️ Limitations

- Data is stored only in memory  
- All data resets when the server restarts  
- Not intended for production use without persistent storage  

---

## 🚧 Future Improvements

- Database integration (SQLite / PostgreSQL / MySQL)  
- Authentication and authorization  
- Pagination and filtering  
- Unit and integration tests  

---

## 👤 Author

**Blerand Cupi**  
Computer Science & Technology Student  
FastAPI • Python • Backend Development
