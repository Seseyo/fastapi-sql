import os

# import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL


DATABASE_URL = os.environ.get('DATABASE_URL')
print(DATABASE_URL)

engine = create_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()
