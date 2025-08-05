# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User, AuthProvider # AuthProvider 추가
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

async def get_user_by_email(db: AsyncSession, email: str) -> User | None: 
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email=email)
    if not user or not user.hashed_password: # 비밀번호가 없는 소셜 로그인 유저 제외
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# 이 함수의 내용을 아래 코드로 교체해주세요.
async def create_or_get_google_user(db: AsyncSession, google_user_info: dict) -> User:
    """
    구글 사용자 정보로 사용자를 찾거나 생성합니다.
    """
    email = google_user_info.get("email")
    user = await get_user_by_email(db, email=email)

    if user:
        if user.provider != AuthProvider.GOOGLE:
            raise Exception("이미 다른 방식으로 가입된 이메일입니다.")
        return user
    
    # 새로운 구글 유저 생성
    new_user = User(
        email=email,
        provider=AuthProvider.GOOGLE
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user