from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from model.user import UserResponse

DATABASE_URL = "mysql+pymysql://root:Sqlroot007#@localhost/leaarndb?host=localhost?port=3306"

engine = create_engine(DATABASE_URL)
SessionLocal1 = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функція для отримання з'єднання з базою даних
def get_db():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

#це підключення css діректорії
app.mount("/static", StaticFiles(directory="static"), name="static")

#це підключення HTML файлів
templates = Jinja2Templates(directory="templates")

@app.get ("/", response_class=HTMLResponse)
async def read_root(request: Request):
    message = "Hello, Fast Api World!"
    return  templates.TemplateResponse("index.html", {"request": request, "message": message})

@app.get("/create_user/", response_class=HTMLResponse)
async def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("model/user.py")
def create_user(user: UserResponse, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(id=user.id, name=user.name)

def list_users(request: Request, db: Session = Depends(get_db)):
    UserResponse = db.query(UserResponse).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": UserResponse})