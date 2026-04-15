from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_admin_id
from app.services import table as table_service
from app.utils.response import success, page_result

router = APIRouter(prefix="/table", tags=["管理-桌号"], dependencies=[Depends(get_current_admin_id)])


class TableCreateRequest(BaseModel):
    shop_id: int = 1
    table_no: str
    area: Optional[str] = None
    seats: int = 4


class TableBatchCreateRequest(BaseModel):
    shop_id: int = 1
    prefix: str = ""
    start: int = 1
    end: int = 10
    area: Optional[str] = None
    seats: int = 4


class TableUpdateRequest(BaseModel):
    id: int
    table_no: Optional[str] = None
    area: Optional[str] = None
    seats: Optional[int] = None
    status: Optional[int] = None


@router.get("/list")
async def get_tables(
    shop_id: int = Query(1),
    page: int = Query(1, alias="pageNo"),
    page_size: int = Query(50, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    data = await table_service.get_tables(db, shop_id, page, page_size)
    items = [
        {
            "id": t.id, "shopId": t.shop_id, "tableNo": t.table_no,
            "area": t.area, "seats": t.seats, "status": t.status,
            "createTime": t.create_time.isoformat() if t.create_time else None,
        }
        for t in data["list"]
    ]
    return page_result(items, data["total"], page, page_size)


@router.post("/create")
async def create_table(req: TableCreateRequest, db: AsyncSession = Depends(get_db)):
    tid = await table_service.create_table(db, req.shop_id, req.table_no, req.area, req.seats)
    return success({"id": tid})


@router.post("/batch-create")
async def batch_create(req: TableBatchCreateRequest, db: AsyncSession = Depends(get_db)):
    count = await table_service.batch_create_tables(
        db, req.shop_id, req.prefix, req.start, req.end, req.area, req.seats
    )
    return success({"count": count}, msg=f"成功创建{count}个桌号")


@router.put("/update")
async def update_table(req: TableUpdateRequest, db: AsyncSession = Depends(get_db)):
    await table_service.update_table(
        db, req.id, table_no=req.table_no, area=req.area, seats=req.seats, status=req.status
    )
    return success(msg="更新成功")


@router.delete("/delete")
async def delete_table(id: int = Query(...), db: AsyncSession = Depends(get_db)):
    await table_service.delete_table(db, id)
    return success(msg="删除成功")
