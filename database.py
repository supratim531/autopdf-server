from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
DB_URL = 'sqlite:///database.sqlite3'
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
  db = sessionlocal()

  try:
    yield db
  finally:
    db.close()
