from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQL_ALCHEMY_DATABASE_ALCHEMY = "sqlite:///./todos.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE_ALCHEMY,connect_args= {"check_same_thread" : False}
)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)
# seccionLocal = sessionmaker(autoflush= False, autocommit = False, bind=)
Base = declarative_base()

