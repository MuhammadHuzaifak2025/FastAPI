from fastapi import FastAPI, Depends
import Models
from db import engine, SessionLocal
from sqlalchemy.orm import session

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



@app.get('/')
async def get_all_data(db: session = Depends(get_db)):
    return db.query(Models.Todos).all()
@app.get('/searchbyid/{id}')
async def get_all_data(id: str, db: session = Depends(get_db)):
    search_str =  db.query(Models.Todos).filter(Models.Todos.id == id).first()
    return search_str
