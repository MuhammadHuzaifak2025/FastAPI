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


class Todo(BaseModel):
    title: str
    Description: Optional[str]
    priority: int = Field(gt=0, lt=6, Description="Priority Must be bw 1 and 5")
    complete: bool


@app.get('/')
async def get_all_data(db: session = Depends(get_db)):
    return db.query(Models.Todos).all()


@app.get('/searchbyid/{id}')
async def get_all_data(id: str, db: session = Depends(get_db)):
    search_str = db.query(Models.Todos).filter(Models.Todos.id == id).first()
    return search_str


@app.post('/')
async def create_todo(todo: Todo, db: session = Depends(get_db)):
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
async def update_todo(todo_id: int, todo: Todo, db: session = Depends(get_db)):
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
