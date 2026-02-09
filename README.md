# ⚡ FastAPI Todo API (Python + SQLite)

A modern and well-structured RESTful API built with Python, FastAPI, and SQLAlchemy, delivering full CRUD functionality with persistent database storage.

The project applies real-world backend development principles such as clean architecture, robust database integration, advanced querying, soft delete mechanisms, statistics endpoints, data export capabilities, and automatically generated API documentation.

Built to showcase backend engineering skills, support portfolio projects, and serve as a practical foundation for scalable API development.
---

## 🚀 Features

### Core Features
- Create new Todo items
- Retrieve all Todos
- Retrieve a Todo by ID
- Update Todos (PUT and PATCH)
- Delete Todos (soft delete)
- Restore deleted Todos
- Persistent storage using SQLite
- Auto-generated API documentation (Swagger and ReDoc)

### Advanced Querying
- Pagination using offset and limit
- Filter by priority
- Filter by status
- Search Todos by keyword
- Sorting by multiple fields
- Ascending and descending ordering
- Include or exclude deleted Todos

### Extra Functionality
- Todos statistics endpoint
- Export Todos (JSON and CSV)
- Health check endpoint
- Enum-based priority system (LOW, MEDIUM, HIGH)
- Enum-based status system (NEW, IN_PROGRESS, DONE)

---

## 🧱 Tech Stack
- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

---

## 📁 Project Structure

app/
├── __init__.py
├── main.py
├── db.py
├── models.py
├── schemas.py
├── todos.db

---

## 📦 Installation

Create a virtual environment  
python -m venv venv

Activate the virtual environment  
macOS / Linux: source venv/bin/activate  
Windows: venv\Scripts\activate

Install dependencies  
pip install fastapi uvicorn sqlalchemy pydantic

---

## ▶️ Running the Application

If the FastAPI instance is defined as:  
api = FastAPI()

Run the application:  
uvicorn app.main:api --reload

The API will be available at:  
http://127.0.0.1:8000

---

## 📚 API Documentation

Swagger UI  
http://127.0.0.1:8000/docs

ReDoc  
http://127.0.0.1:8000/redoc

---

## 🔗 API Endpoints

System  
GET /health – Health check

Todos  
GET /todos – List Todos (filters, search, pagination, sorting)  
POST /todos – Create Todo  
GET /todos/{todo_id} – Get Todo by ID  
PUT /todos/{todo_id} – Replace Todo  
PATCH /todos/{todo_id} – Update Todo  
PATCH /todos/{todo_id}/status – Update Todo status  
DELETE /todos/{todo_id} – Soft delete Todo  
POST /todos/{todo_id}/restore – Restore deleted Todo  
GET /todos/stats – Todos statistics  
GET /todos/export – Export Todos (JSON or CSV)

---

## 📝 Example Request

Create Todo  
{
  "todo_name": "Study FastAPI",
  "todo_description": "Prepare for backend exam",
  "priority": 1,
  "status": "NEW"
}

Priority Values  
1 = HIGH  
2 = MEDIUM  
3 = LOW

---

## 📊 Statistics Endpoint

The /todos/stats endpoint returns:
- Total Todos
- High, Medium, and Low priority counts
- Option to include or exclude deleted Todos

---

## ⚠️ Notes
- Uses SQLite for persistent storage
- Database file: todos.db
- Data persists between server restarts

---

## 🚧 Future Improvements
- Authentication and authorization (JWT)
- Role-based access (Admin/User)
- Pagination metadata
- Unit and integration tests
- Docker support
- PostgreSQL / MySQL support

---

## 👤 Author

Blerand Cupi  
Computer Science and Technology Student  

FastAPI • Python • Backend Development  
