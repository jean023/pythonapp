from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()