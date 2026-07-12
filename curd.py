from sqlalchemy.orm import session
from models import User,Habit

def create_user(db: session, username:str,password:str):
    user=User(username=username,password=password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user(db: session, username:str):
    return db.query(User).filter(User.username == username).first()

def create_habit(db: session, task: str, type: str, difficulty:int, owner_id:int):
    xp= 20 if difficulty >= 8 else 15 if difficulty >= 5 else 10

    habit = Habit(task = task, type=type, difficulty=difficulty, xp_reward=xp, owner_id=owner_id)

    db.add(habit)
    db.commit()
    db.refresh(habit)

    return habit

def delete_habit(db: session,habit_id:int):
    db.query(Habit).filter(Habit.id == habit_id).delete()
    db.commit()
    return  