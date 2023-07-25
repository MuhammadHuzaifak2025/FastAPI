from sqlalchemy import Boolean, String, Integer, Column
from db import Base


class Todos(Base):
    __tablename__ = "Todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250))
    Description = Column(String(250))
    priority = Column(Integer)
    Complete = Column(Boolean, default=False)
