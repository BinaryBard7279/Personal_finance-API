# API для учета личных финансов - Доходы/расходы по категориям

FastAPI приложение для учёта личных финансов с JWT-аутентификацией.

## Структура

```
/
├── main.py             \# эндпоинты
├── database.py         \# подключение к бд
├── models.py           \# таблицы
├── schemas.py          \# схемы Pydantic
├── security.py         \# JWT и пароли
└── requirements.txt    \# зависимости

```

## Локальный запуск

1. **клонировать и установить**
```

git clone https://github.com/BinaryBard7279/Personal_finance-API.git
cd Personal_finance-API
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

```

2. **создать .env**
```

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/finance_db
SECRET_KEY=your_secret_key

```

3. **запуск**
```

uvicorn main:app --reload

```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## деплой на Render

**Live URL**: [https://personal-finance-api-7v4g.onrender.com/docs](https://personal-finance-api-7v4g.onrender.com/docs)

### Шаги

1. Переходим на [render.com](https://render.com)

2. Авторизуемся через GitHub

3. Dashboard → "+ New" → **Postgres**

4. Заполняем:
   - Name: `personal-finance-db`
   - Database: `finance_db`
   - Region: **Frankfurt** (ближе всего к России)
   - PostgreSQL version: 17 или 18
   - Instance type: **Free**

5. Create Database → ждем Status: **Available**

6. Листаем до раздела **Connections** → копируем **Internal Database URL**

7. "+ New" → **Web Service** → подключаем GitHub репозиторий

8. Заполняем:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Instance type: **Free**

9. **Environment Variables** → добавляем:
   - Key: `DATABASE_URL`
   - Value: Internal Database URL + **добавить `+asyncpg`**
   - Пример: `postgresql+asyncpg://user:pass@host:5432/db`
   
   Также добавить другие переменные из `.env` (например, `SECRET_KEY`)

10. Deploy Web Service → ждем "Your service is live 🎉"

Swagger доступен по ссылке + `/docs`
Free tier засыпает после 15 минут — первый запрос ~30 сек.