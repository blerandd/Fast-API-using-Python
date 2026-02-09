from typing import List, Optional
from datetime import datetime, timezone
import os
import io
import csv

from fastapi import FastAPI, Depends, HTTPException, Query, Path, status, Request, Header
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .db import Base, engine, SessionLocal
from .models import TodoModel
from .schemas import (
    TodoCreate,
    TodoUpdate,
    TodoReplace,
    TodoStatusUpdate,
    TodoOut,
    TodoStats,
    HealthOut,
    Priority,
    SortBy,
    OrderBy,
    ExportFormat,
)

API_KEY = os.getenv("TODO_API_KEY", "name_here")


api = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_api_key(x_api_key: str = Header(default="", alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"ok": False, "error": "HTTPException", "detail": exc.detail, "path": str(request.url.path)},
    )


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"ok": False, "error": "ValidationError", "detail": exc.errors(), "path": str(request.url.path)},
    )


def get_or_404(db: Session, todo_id: int, include_deleted: bool = False) -> TodoModel:
    q = db.query(TodoModel).filter(TodoModel.todo_id == todo_id)
    if not include_deleted:
        q = q.filter(TodoModel.is_deleted == False)
    todo = q.first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@api.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        exists = db.query(TodoModel).filter(TodoModel.is_deleted == False).first()
        if not exists:
            now = datetime.now(timezone.utc)
            db.add_all(
                [
                    TodoModel(todo_name="Sports", todo_description="Go to the Gym", priority=int(Priority.MEDIUM), status="IN_PROGRESS", due_date=None),
                    TodoModel(todo_name="Clean house", todo_description="Cleaning the house thoroughly", priority=int(Priority.HIGH), status="NEW", due_date=None),
                    TodoModel(todo_name="Read", todo_description="Read chapter 5 of the book", priority=int(Priority.LOW), status="DONE", due_date=None),
                    TodoModel(todo_name="Work", todo_description="Complete project documentation", priority=int(Priority.MEDIUM), status="NEW", due_date=now),
                    TodoModel(todo_name="Study", todo_description="Prepare for upcoming exam", priority=int(Priority.LOW), status="NEW", due_date=None),
                ]
            )
            db.commit()
    finally:
        db.close()


@api.get("/health", response_model=HealthOut, tags=["System"])
def health():
    return {"status": "ok"}


@api.get("/todos", response_model=List[TodoOut], tags=["Todos"])
def list_todos(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    priority: Optional[Priority] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    q: Optional[str] = Query(None, min_length=1, max_length=100),
    overdue: bool = Query(False),
    sort_by: SortBy = Query("todo_id"),
    order: OrderBy = Query("asc"),
    include_deleted: bool = Query(False),
):
    query = db.query(TodoModel)

    if not include_deleted:
        query = query.filter(TodoModel.is_deleted == False)

    if priority is not None:
        query = query.filter(TodoModel.priority == int(priority))

    if status_filter is not None:
        query = query.filter(TodoModel.status == status_filter)

    if q:
        query = query.filter(
            or_(
                TodoModel.todo_name.ilike(f"%{q}%"),
                TodoModel.todo_description.ilike(f"%{q}%"),
            )
        )

    if overdue:
        now = datetime.now(timezone.utc)
        query = query.filter(TodoModel.due_date.isnot(None)).filter(TodoModel.due_date < now)

    sort_col = getattr(TodoModel, sort_by)
    query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())

    return query.offset(offset).limit(limit).all()


@api.get("/todos/export", tags=["Todos"])
def export_todos(
    db: Session = Depends(get_db),
    format: ExportFormat = Query("json"),
    include_deleted: bool = Query(False),
):
    query = db.query(TodoModel)
    if not include_deleted:
        query = query.filter(TodoModel.is_deleted == False)

    todos = query.order_by(TodoModel.todo_id.asc()).all()

    if format == "json":
        return [
            {
                "todo_id": t.todo_id,
                "todo_name": t.todo_name,
                "todo_description": t.todo_description,
                "priority": t.priority,
                "status": t.status,
                "due_date": t.due_date,
                "is_deleted": t.is_deleted,
                "created_at": t.created_at,
                "updated_at": t.updated_at,
            }
            for t in todos
        ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["todo_id", "todo_name", "todo_description", "priority", "status", "due_date", "is_deleted", "created_at", "updated_at"])
    for t in todos:
        writer.writerow(
            [
                t.todo_id,
                t.todo_name,
                t.todo_description,
                t.priority,
                t.status,
                t.due_date.isoformat() if t.due_date else "",
                t.is_deleted,
                t.created_at.isoformat() if t.created_at else "",
                t.updated_at.isoformat() if t.updated_at else "",
            ]
        )
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=todos.csv"})


@api.get("/todos/stats", response_model=TodoStats, tags=["Todos"])
def todos_stats(db: Session = Depends(get_db), include_deleted: bool = Query(False)):
    base = db.query(TodoModel)
    if not include_deleted:
        base = base.filter(TodoModel.is_deleted == False)

    total = base.count()
    high = base.filter(TodoModel.priority == int(Priority.HIGH)).count()
    medium = base.filter(TodoModel.priority == int(Priority.MEDIUM)).count()
    low = base.filter(TodoModel.priority == int(Priority.LOW)).count()

    return {"total": total, "high": high, "medium": medium, "low": low}


@api.get("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"])
def get_todo(
    todo_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return get_or_404(db, todo_id)


@api.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED, tags=["Todos"], dependencies=[Depends(require_api_key)])
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodoModel(
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=int(todo.priority),
        status=todo.status,
        due_date=todo.due_date,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@api.put("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"], dependencies=[Depends(require_api_key)])
def replace_todo(
    todo_id: int = Path(..., ge=1),
    payload: TodoReplace = ...,
    db: Session = Depends(get_db),
):
    todo = get_or_404(db, todo_id)
    todo.todo_name = payload.todo_name
    todo.todo_description = payload.todo_description
    todo.priority = int(payload.priority)
    todo.status = payload.status
    todo.due_date = payload.due_date
    db.commit()
    db.refresh(todo)
    return todo


@api.patch("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"], dependencies=[Depends(require_api_key)])
def update_todo(
    todo_id: int = Path(..., ge=1),
    payload: TodoUpdate = ...,
    db: Session = Depends(get_db),
):
    todo = get_or_404(db, todo_id)
    data = payload.model_dump(exclude_unset=True)

    if "todo_name" in data:
        todo.todo_name = data["todo_name"]
    if "todo_description" in data:
        todo.todo_description = data["todo_description"]
    if "priority" in data:
        todo.priority = int(data["priority"])
    if "status" in data:
        todo.status = data["status"]
    if "due_date" in data:
        todo.due_date = data["due_date"]

    db.commit()
    db.refresh(todo)
    return todo


@api.patch("/todos/{todo_id}/status", response_model=TodoOut, tags=["Todos"], dependencies=[Depends(require_api_key)])
def update_todo_status(
    todo_id: int = Path(..., ge=1),
    payload: TodoStatusUpdate = ...,
    db: Session = Depends(get_db),
):
    todo = get_or_404(db, todo_id)
    todo.status = payload.status
    db.commit()
    db.refresh(todo)
    return todo


@api.post("/todos/{todo_id}/restore", response_model=TodoOut, tags=["Todos"], dependencies=[Depends(require_api_key)])
def restore_todo(
    todo_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    todo = get_or_404(db, todo_id, include_deleted=True)
    todo.is_deleted = False
    db.commit()
    db.refresh(todo)
    return todo


@api.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"], dependencies=[Depends(require_api_key)])
def delete_todo(
    todo_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    todo = get_or_404(db, todo_id)
    todo.is_deleted = True
    db.commit()
    return
