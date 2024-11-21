from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User, SessionLocal, engine


app = FastAPI()


# dependency for getting db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create User
@app.post('/users/')
def create_user(name: str, description: str = None, db: Session = Depends(get_db)):
    new_user = User(name=name, description=description)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get users
@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


# update user
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, description: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(user.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.description = description
    db.commit()
    db.refresh(user)
    return user

#delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}