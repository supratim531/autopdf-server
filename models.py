from database import Base

from sqlalchemy import Column, String


class User(Base):
  __tablename__ = "users"

  user_id = Column(String, primary_key=True, index=True)

  def __repr__(self):
    return f'<User(user_id="{self.user_id}")>'
