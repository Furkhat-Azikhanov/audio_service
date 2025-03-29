
# 🎧 Audio Service

FastAPI-сервис для загрузки аудиофайлов с авторизацией через Яндекс. Хранение файлов локальное. Аутентификация запросов через внутренние JWT-токены. База данных — PostgreSQL 16, работает в Docker.

## 🚀 Возможности
- Авторизация через Яндекс OAuth
- Генерация внутреннего access_token (JWT)
- Получение/удаление пользователей (в том числе суперпользователем)
- Загрузка аудиофайлов (mp3, wav, ogg)
- Хранение файлов на локальной машине
- Получение списка загруженных файлов текущего пользователя

## 🧱 Технологии
- **FastAPI** (асинхронно)
- **PostgreSQL 16**
- **SQLAlchemy 2.0 + asyncpg**
- **Docker + docker-compose**
- **JWT-токены (python-jose)**
- **OAuth через Яндекс**

## 📦 Установка и запуск

### 1. Клонируй репозиторий
```bash
git clone https://github.com/ТВОЙ_ПОЛЬЗОВАТЕЛЬ/audio_service.git
cd audio_service
```

### 2. Создай файл `.env`
❗ Настоящий `.env` не пушится в репозиторий, создай сам рядом с `docker-compose.yml`

```
POSTGRES_DB=audio_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/audio_db
JWT_SECRET=supersecret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
YANDEX_OAUTH_CLIENT_ID=твоя_интеграция
YANDEX_OAUTH_CLIENT_SECRET=твой_секрет
YANDEX_OAUTH_REDIRECT_URI=http://localhost:8000/auth/yandex/callback
```
⚠️ Также можешь посмотреть `.env.example` для подсказки.

### 3. Собери и запусти через Docker
```bash
docker-compose up --build
```

### 4. Открой браузер
```
http://localhost:8000/docs
```

## 📂 Структура проекта
```
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── utils/
│   │   └── token.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── audio.py
│   └── audio_files/  # локально сохраняемые файлы
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Авторизация через Яндекс
1. Перейди по `/auth/yandex/login`
2. Авторизуйся через Яндекс
3. Получишь токен `access_token`
4. Используй его в заголовке:
```
Authorization: Bearer eyJhbGciOi...
```

## 🧪 Примеры запросов

### Загрузка файла:
```bash
curl -X POST "http://localhost:8000/audio/upload?name=песня" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@/путь/к/файлу.mp3;type=audio/mpeg"
```

### Получение списка:
```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/audio/
```

## 🛠️ TODO
* Авторизация через Яндекс
* Генерация JWT токена
* Эндпоинты пользователей
* Загрузка аудио
* Получение списка файлов
* Тесты (по желанию)
* CI/CD (по желанию)

## 👨‍💻 Автор
Разработано в рамках тестового задания Furkhat Azikhanov