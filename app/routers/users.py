from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

from fastapi.security import OAuth2PasswordBearer
from app.utils.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_superuser": current_user.is_superuser,
    }
