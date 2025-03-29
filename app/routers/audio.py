import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import AudioFile, User
from app.routers.users import get_current_user

router = APIRouter(prefix="/audio", tags=["Audio"])

UPLOAD_DIR = "app/audio_files"

# Загрузка файла
@router.post("/upload")
async def upload_audio(
    name: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Проверка типа файла
    if not file.filename.endswith((".mp3", ".wav", ".ogg")):
        raise HTTPException(status_code=400, detail="Invalid audio format")

    # Путь к файлу
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Сохраняем файл на диск
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    # Записываем в БД
    new_file = AudioFile(
        filename=name,
        filepath=file_location,
        user_id=current_user.id
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {"message": "Файл загружен", "id": new_file.id, "name": new_file.filename}


@router.get("/")
async def list_user_files(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AudioFile).where(AudioFile.user_id == current_user.id)
    )
    files = result.scalars().all()
    return [
        {
            "id": file.id,
            "name": file.filename,
            "path": file.filepath,
            "created_at": file.created_at,
        }
        for file in files
    ]
