from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from database import base

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True , nullable=False)
    password = Column(String, nullable = False)
    level = Column(Integer, default = 1)
    xp = Column(Integer, default=0)
    total_completed_tasks = Column(Integer, default = 0)
    habit = relationship("Habit", back_populates="owner")

class Habit(base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    type = Column(String)
    difficulty = Column(Integer)
    xp_reward = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="habit")