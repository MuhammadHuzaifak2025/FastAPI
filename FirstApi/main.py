from typing import Optional

from fastapi import FastAPI, Depends
import Models
from db import engine, SessionLocal
from sqlalchemy.orm import session
from pydantic import BaseModel, Field

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


class Todos(BaseModel):
    title: str
    Description: Optional[str]
    priority: int = Field(gt=0, lt=6, Description="Priority Must be bw 1 and 5")
    complete: bool


class Todolist(BaseModel):
    todo_list: list[Todos]


@app.get('/')
async def get_all_data(db: session = Depends(get_db)):
    return db.query(Models.Todos).all()


@app.get('/searchbyid/{id}')
async def get_all_data(id: str, db: session = Depends(get_db)):
    search_str = db.query(Models.Todos).filter(Models.Todos.id == id).first()
    return search_str


@app.post('/')
async def create_todo(todo: Todos, db: session = Depends(get_db)):
    todo_model = Models.Todos()
    todo_model.title = todo.title
    todo_model.Description = todo.Description
    todo_model.priority = todo.priority
    todo_model.Complete = todo.complete

    db.add(todo_model)
    db.commit()
    return {
        'status': 201,
        'transaction': 'SuccesFull'
    }


@app.post('/{todo_id}')
async def update_todo(todo_id: int, todo: Todos, db: session = Depends(get_db)):
    todo_model = db.query(Models.Todos).filter(Models.Todos.id == todo_id).first()
    # return {
    #     'status': todo_id,
    #     'transaction': todo_model
    # }
    todo_model.title = todo.title
    todo_model.Description = todo.Description
    todo_model.priority = todo.priority
    todo_model.Complete = todo.complete
    db.add(todo_model)
    db.commit()
    return {
        'status': 201,
        'transaction': 'SuccesFull'
    }


@app.post('/delete/{todo_id}')
async def delete_todo(todo_id: int, db: session = Depends(get_db)):
    db.query(Models.Todos).filter(Models.Todos.id == todo_id).delete()
    db.commit()
    return {
        'status': 201,
        'transaction': 'SuccesFully Deleted'
    }


@app.post('/Create_Todos')
async def create_todos(todos: Todolist, db: session = Depends(get_db)):
    models = []
    for e in todos.todo_list:
        todo_model = Models.Todos()
        todo_model.title = e.title
        todo_model.Description = e.Description
        todo_model.priority = e.priority
        todo_model.Complete = e.complete
        models.append(todo_model)
    db.add(models)
    db.commit()
    return "true"
