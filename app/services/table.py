from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import StoreTable


async def get_tables(db: AsyncSession, shop_id: int = 1, page: int = 1, page_size: int = 50) -> dict:
    """获取桌号列表"""
    base = select(StoreTable).where(StoreTable.deleted == False, StoreTable.shop_id == shop_id)
    total = (await db.execute(select(func.count(StoreTable.id)).where(
        StoreTable.deleted == False, StoreTable.shop_id == shop_id
    ))).scalar()
    stmt = base.order_by(StoreTable.table_no).offset((page - 1) * page_size).limit(page_size)
    tables = (await db.execute(stmt)).scalars().all()
    return {"list": tables, "total": total}


async def create_table(db: AsyncSession, shop_id: int, table_no: str,
                       area: Optional[str] = None, seats: int = 4) -> int:
    t = StoreTable(shop_id=shop_id, table_no=table_no, area=area, seats=seats)
    db.add(t)
    await db.flush()
    return t.id


async def batch_create_tables(db: AsyncSession, shop_id: int, prefix: str,
                               start: int, end: int, area: Optional[str] = None, seats: int = 4) -> int:
    """批量创建桌号"""
    count = 0
    for i in range(start, end + 1):
        table_no = f"{prefix}{i}"
        t = StoreTable(shop_id=shop_id, table_no=table_no, area=area, seats=seats)
        db.add(t)
        count += 1
    await db.flush()
    return count


async def update_table(db: AsyncSession, table_id: int, **kwargs) -> None:
    stmt = select(StoreTable).where(StoreTable.id == table_id)
    result = await db.execute(stmt)
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="桌号不存在")
    for k, v in kwargs.items():
        if v is not None:
            setattr(t, k, v)
    await db.flush()


async def delete_table(db: AsyncSession, table_id: int) -> None:
    stmt = select(StoreTable).where(StoreTable.id == table_id)
    result = await db.execute(stmt)
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="桌号不存在")
    t.deleted = True
    await db.flush()
