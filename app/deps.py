from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.security import decode_token

security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> int:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token无效或已过期")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token无效")
    return int(user_id)


async def get_current_user_id_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[int]:
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload:
        return None
    user_id = payload.get("sub")
    return int(user_id) if user_id else None


async def get_current_admin_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> int:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无管理员权限")
    return int(payload["sub"])
