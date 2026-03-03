from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users")
def create_user(name: str, email: str):
    db: Session = SessionLocal()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@app.get("/users")
def get_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users