from database import Base

from sqlalchemy import Column, String


class User(Base):
  __tablename__ = "users"

  user_id = Column(String, primary_key=True, index=True)
  html_file_name = Column(String, unique=True, index=True)

  def __repr__(self):
    return f'<User(user_id="{self.user_id}", html_file_name="{self.html_file_name}")>'
