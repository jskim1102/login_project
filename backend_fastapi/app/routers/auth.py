# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from google.oauth2 import id_token
from google.auth.transport import requests
import anyio

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.token import Token, GoogleToken
from app.services import user_service

router = APIRouter()

@router.post("/google", response_model=Token)
async def google_login(
    token_data: GoogleToken, 
    db: AsyncSession = Depends(get_db)
):
    try:
        # 동기 함수를 비동기 환경에서 안전하게 실행
        idinfo = await anyio.to_thread.run_sync(
            id_token.verify_oauth2_token,
            token_data.token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )
        
        if 'email' not in idinfo:
            raise HTTPException(status_code=400, detail="Google 토큰에서 이메일 정보를 찾을 수 없습니다.")

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 Google 토큰입니다.",
        )
    
    try:
        user = await user_service.create_or_get_google_user(db, google_user_info=idinfo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not user:
         raise HTTPException(
            status_code=500,
            detail="사용자를 찾거나 생성하는 데 실패했습니다.",
        )

    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}