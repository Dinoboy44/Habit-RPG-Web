from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from database import engine,SessionLocal
from models import base,Habit,User
import curd;import random
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware,secret_key="gngneedshabitrpg@48#45")

base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory={"tampletes"})

@app.get('/')
def home(request: Request):
    quotes = ["Small habits create big results.",
              "Discipline beats motivation.",
              "Every quest begins with one step.",
              "Level up your life, one habit at a time."]
    
    quote = random.choice(quotes)

    return templates.TemplateResponse(request=request,name="index.html",context={"quote":quote})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(request=request, name="register.html")

@app.post("/register")
def register_user(username: str = Form(...),password: str = Form(...)):
    db = SessionLocal()
    curd.create_user(db, username, password)
    db.close()
    return {
        "message": "User Registered Successfully!"
    }

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
def login_user(request: Request,username: str = Form(...),password: str = Form(...)):
    db = SessionLocal()
    user = curd.get_user(db,username)
    db.close()
    if user is None:
        return {"message": "User Not Found"}
    
    if user.password != password:
        return {"message": "Incorrect Password"}

    request.session["user_id"] = user.id

    return RedirectResponse(url="/dashboard",status_code=303)

@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request: Request):
    userid = request.session.get("user_id")
    if not userid:
        return RedirectResponse("/login", status_code=303)
    db = SessionLocal()
    user = db.query(User).filter(User.id == userid).first()
    habits = db.query(Habit).filter(Habit.owner_id == userid).all()
    db.close()
    return templates.TemplateResponse(request= request,name="dashboard.html",context={"user" : user,"habits" : habits})

@app.post("/addhabit")
def add_habit(request: Request,task: str = Form(...),type: str = Form(...),difficulty: int = Form(...)):
    userid = request.session.get("user_id")
    db = SessionLocal()
    curd.create_habit(db,task,type,difficulty,userid)

    db.close()

    return RedirectResponse(url=f"/dashboard",status_code=303)

@app.post("/complete/{habit_id}")
def complete_habit(request: Request,habit_id: int):
    user_id = request.session.get("user_id")
    db = SessionLocal()
    habitt = db.query(Habit).filter(Habit.id == habit_id, Habit.owner_id == user_id).first()
    if habitt:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()

        if habit and not habit.completed:
            habit.completed = True
            user = db.query(User).filter(User.id == habit.owner_id).first()
            user.xp += habit.xp_reward
            user.total_completed_tasks += 1
            while user.xp >= user.level * 100:
                user.xp -= user.level * 100
                user.level += 1

            db.commit()
            db.close()
            return RedirectResponse(url=f"/dashboard",status_code=303)
        
        db.close()
        return RedirectResponse(url="/",status_code=303)

@app.post("/delete/{habit_id}")
def delete_habit(request: Request,habit_id: int):
    user_id = request.session.get("user_id")
    db = SessionLocal()
    
    habitt = db.query(Habit).filter(Habit.id == habit_id, Habit.owner_id == user_id).first()
    if habitt:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if habit is None:
            db.close()
            return {"error": "Habit not found"}
        curd.delete_habit(db,habit_id)
        db.close()
        return RedirectResponse(url=f"/dashboard",status_code=303)
    else: return RedirectResponse(url="/",status_code=303)

@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/",status_code=303)