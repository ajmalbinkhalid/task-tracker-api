from fastapi import APIRouter, Depends
from src.auth import get_current_user
from src import models
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth import get_current_user
from src import models

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    users = db.query(models.User).all()

    return users

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}