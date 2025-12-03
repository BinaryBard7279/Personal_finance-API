from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional 
import security
import schemas
import models
from database import engine, get_db, Base

app = FastAPI(
    title="API для личных финансов",
    description="учет доходов и расходов",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# рега нового юзера
@app.post(
    "/register", 
    response_model=schemas.User,
    summary="регистрация",
    description="создает нового пользователя."
)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).filter(
            (models.User.username == user.username) | 
            (models.User.email == user.email)
        )
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        else:
            raise HTTPException(status_code=400, detail="Email already registered")

    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

# логин, получение токена
@app.post(
    "/login", 
    response_model=schemas.Token,
    summary="вход",
    description="проверяет логин и пароль, возвращает токен."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).filter(models.User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post(
    "/transactions", 
    response_model=schemas.Transaction,
    summary="создать транзакцию",
    description="добавляет новую запись о расходе или доходе."
)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_transaction = models.Transaction(
        **transaction.model_dump(),
        owner_id=current_user.id
    )
    
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    
    return db_transaction

@app.get(
    "/transactions", 
    response_model=list[schemas.Transaction],
    summary="получить список транзакций",
    description="возвращает список транзакций, можно фильтровать."
)
async def get_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    query = select(models.Transaction).filter(models.Transaction.owner_id == current_user.id)
    
    if category:
        query = query.filter(models.Transaction.category == category)

    if type:
        query = query.filter(models.Transaction.type == type)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    return transactions

@app.put(
    "/transactions/{transaction_id}", 
    response_model=schemas.Transaction,
    summary="обновить транзакцию",
    description="изменяет данные существующей транзакции."
)
async def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    result = await db.execute(
        select(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == current_user.id
        )
    )
    db_transaction = result.scalar_one_or_none()
    
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db_transaction.amount = transaction.amount
    db_transaction.category = transaction.category
    db_transaction.description = transaction.description
    db_transaction.date = transaction.date
    
    await db.commit()
    await db.refresh(db_transaction)
    
    return db_transaction

@app.delete(
    "/transactions/{transaction_id}", 
    summary="удалить транзакцию",
    description="удаляет транзакцию по ID."
)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    result = await db.execute(
        select(models.Transaction).filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == current_user.id
        )
    )
    db_transaction = result.scalar_one_or_none()
    
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    await db.delete(db_transaction)
    await db.commit()
    
    return {"message": "Transaction deleted successfully"}