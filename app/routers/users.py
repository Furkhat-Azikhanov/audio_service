from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

# Схема для создания пользователя
class UserCreate(BaseModel):
    email: str
    is_superuser: bool = False

# Получить всех пользователей
@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

# Создать нового пользователя
@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(email=user.email, is_superuser=user.is_superuser)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Удалить пользователя по ID (допустим, только если is_superuser = True)
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": f"User {user_id} deleted"}
