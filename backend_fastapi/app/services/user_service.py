# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password # verify_password 임포트 추가

async def get_user_by_email(db: AsyncSession, email: str) -> User | None: 
    result = await db.execute(select(User).filter(User.email == email)) # 입력된 '이메일(email)'이 '기존 db(User.email)'에 있는지 확인비교, User는 DB 테이블과 연결된 SQLAlchemy 모델
    return result.scalars().first() # 기존 db(User.email)과 입력된 이메일(email)이 일치하면 User를 return, 일치하지 않으면 None을 return

async def create_user(db: AsyncSession, user: UserCreate) -> User: # UserCreate(Schema) : 사용자가 회원가입을 위해 이메일과 비밀번호를 JSON 형태로 API에 보내면, FastAPI는 이 데이터를 UserCreate 객체로 변환
    hashed_password = get_password_hash(user.password) # user.password는 순수하게 사용자가 입력한 비밀번호 문자열
    db_user = User(email=user.email, hashed_password=hashed_password) # DB에 저장하기 위한 User(DB) 모델 객체 db_user를 만듦
    db.add(db_user)
    await db.commit() # await : 비동기 함수 내부에서 사용하며, 시간이 걸리는 작업이 끝날때가지 함수를 잠시 일시정지
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """
    이메일과 비밀번호로 사용자를 인증합니다.
    성공 시 User 객체를, 실패 시 None을 반환합니다.
    """
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user