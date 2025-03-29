from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
import httpx
from app.config import settings
from app.models import User
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(prefix="/auth", tags=["Auth"])

YANDEX_AUTH_URL = (
    "https://oauth.yandex.ru/authorize?"
    f"response_type=code&client_id={settings.YANDEX_OAUTH_CLIENT_ID}"
)

# 1. Перенаправляем пользователя на Яндекс
@router.get("/yandex/login")
async def login_with_yandex():
    return RedirectResponse(url=YANDEX_AUTH_URL)

# 2. Обрабатываем ответ Яндекса
@router.get("/yandex/callback")
async def yandex_callback(request: Request, db: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Нет кода от Яндекса"}

    # Получаем access_token от Яндекса
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_OAUTH_CLIENT_ID,
                "client_secret": settings.YANDEX_OAUTH_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return {"error": "Не удалось получить токен от Яндекса"}

        # Получаем данные пользователя с Яндекса
        user_response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )
        user_data = user_response.json()
        email = user_data.get("default_email")

        if not email:
            return {"error": "Не удалось получить email"}

        # Проверяем: есть ли пользователь в БД
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        # Если нет — создаём
        if not user:
            user = User(email=email)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        return {
            "message": f"Успешный вход как {email}",
            "user_id": user.id,
            "email": user.email,
        }
