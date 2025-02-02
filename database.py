from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()

Base = declarative_base()
DB_URL = 'sqlite:///database.sqlite3'
# DB_URL = 'sqlite:////tmp/database.sqlite3'
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
  db = sessionlocal()

  try:
    yield db
  finally:
    db.close()
