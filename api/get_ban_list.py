from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql import select

from libs.database import db
from libs.database.model import BannedQQList, BannedUUIDList
from libs.server import route
from util import BaseResponse, oauth2_scheme


class BannedQQ(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    qq: int
    banStartTime: int
    banEndTime: int
    banReason: str
    operater: int


class BannedQQResponse(BaseResponse):
    data: list[BannedQQ]


@route.get(
    "/api/get_banned_qq_list",
    response_model=BannedQQResponse,
    summary="获取所有被 Ban 的 QQ",
    tags=["封禁"],
)
async def get_banned_qq(token=Depends(oauth2_scheme)):
    ban_info = await db.select_all(select(BannedQQList))
    return BannedQQResponse(data=[_[0] for _ in ban_info])


class BannedUUID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    banStartTime: int
    banEndTime: int
    banReason: str
    operater: int


class BannedUUIDResponse(BaseResponse):
    data: list[BannedUUID]


@route.get(
    "/api/get_banned_uuid_list",
    response_model=BannedUUIDResponse,
    summary="获取所有被 Ban UUID",
    description="",
    tags=["封禁"],
)
async def get_banned_uuid(token=Depends(oauth2_scheme)):
    ban_info = await db.select_all(select(BannedUUIDList))
    return BannedUUIDResponse(data=[_[0] for _ in ban_info])
