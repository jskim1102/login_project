# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import user
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base # 모든 모델의 Base
from app.models import user as user_model # 테이블 생성을 위해 모델 임포트
from app.routers import user, auth

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Base.metadata.create_all -> base에 정의된 Base를 상속하는 models의 모델을 찾고, 그에 해당하는 테이블을 DB에 생성(이미 테이블이 있으면 X)

@asynccontextmanager
async def lifespan(app: FastAPI): # 서버 시작부터 종료까지 한번 실행(yield)
    print("서버 시작: DB 테이블 생성")
    await create_db_and_tables()
    yield
    print("서버 종료")

app = FastAPI(title="CV SaaS", version="1.0", lifespan=lifespan) 

# 허용할 출처(Origin) 목록입니다. 지금은 프론트엔드 개발 서버 주소만 추가합니다.
# origins = [
#     "http://localhost:5173",
# ]

# 개발 및 테스트를 위해 모든 출처를 허용
origins = [
    "http://deep-i.work:5174",
    "http://localhost:5174",
    "http://192.168.0.36:5174",
    "http://211.106.144.18:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins 목록에 있는 출처의 요청을 허용
    allow_credentials=True, # 요청에 쿠키를 포함하도록 허용
    allow_methods=["*"],    # 모든 HTTP 메소드(GET, POST 등)를 허용
    allow_headers=["*"],    # 모든 HTTP 헤더를 허용
)

app.include_router(user.router, prefix="/api/v1", tags=["Users"]) # router/user.py에 만들어 두었던 엔드포인트 설정
app.include_router(user.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CV SaaS API"}