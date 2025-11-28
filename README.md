# Структура

```
/
├── main.py             # эндпоинты
├── database.py         # подключение к бд
├── models.py           # иаблицы
├── schemas.py          # схемы Pydantic + валидация
├── security.py         # токены и пароль
├── requirements.txt    # зависимости
└── database.db         # файл с бд
```

## Как запустить

1.  **клонировать репозиторий:**
    ```bash
    git clone [ссылка на репозиторий, если был бы]
    cd API-
    ```
2.  **создать venv, установить зависимости**
    ```bash
    python -m venv venv
    # source venv/bin/activate 
    pip install -r requirements.txt
    ```
3.  **запуск**
    ```bash
    uvicorn main:app --reload
    ```