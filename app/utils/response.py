from typing import Any, Optional


def success(data: Any = None, msg: str = "success") -> dict:
    return {"code": 0, "msg": msg, "data": data}


def error(msg: str = "error", code: int = 500, data: Any = None) -> dict:
    return {"code": code, "msg": msg, "data": data}


def page_result(items: list, total: int, page: int = 1, page_size: int = 10) -> dict:
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "list": items,
            "total": total,
            "page": page,
            "pageSize": page_size,
        },
    }
