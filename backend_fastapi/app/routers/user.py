# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token # Token 스키마 임포트
from app.services import user_service
from app.core.security import create_access_token # create_access_token 임포트
from app.core.config import settings
from app.db.session import get_db

router = APIRouter()

@router.post("/users/", response_model=UserRead, status_code=201) # 엔드포인트 설정
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)): # DB 연결 준비
    db_user = await user_service.get_user_by_email(db, email=user.email) # 이미 가입된 이메일인지 확인
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db=db, user=user) # response_model(UserRead)를 통해 클라이언트에게 전달

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}