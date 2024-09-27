from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_rooms import crud_rooms
from ...schemas.room import RoomCreate, RoomDelete, RoomRead, RoomUpdate, RoomUpdateInternal

router = APIRouter(tags=["rooms"])

@router.post("/room", response_model=RoomRead, status_code=201)
async def write_room(
    request: Request, room: RoomCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> RoomRead:
    name_row = await crud_rooms.exists(db=db, name=room.name)
    if name_row:
        raise DuplicateValueException("Room name is already registered")

    created_room: RoomRead = await crud_rooms.create(db=db, object=room)
    return created_room

@router.get("/rooms", response_model=PaginatedListResponse[RoomRead])
async def read_rooms(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    rooms_data = await crud_rooms.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=RoomRead,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=rooms_data, page=page, items_per_page=items_per_page)
    return response

@router.get("/room/{id}", response_model=RoomRead)
async def read_room(request: Request, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_room: RoomRead | None = await crud_rooms.get(
        db=db, schema_to_select=RoomRead, id=id, is_deleted=False
    )
    if db_room is None:
        raise NotFoundException("Room not found")

    return db_room

@router.patch("/room/{id}")
async def patch_room(
    request: Request,
    values: RoomUpdate,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_room = await crud_rooms.get(db=db, schema_to_select=RoomRead, id=id)
    if db_room is None:
        raise NotFoundException("Room not found")

    await crud_rooms.update(db=db, object=values, id=id)
    return {"message": "Room updated"}

@router.delete("/room/{id}")
async def erase_room(
    request: Request,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_room = await crud_rooms.get(db=db, schema_to_select=RoomRead, id=id)
    if not db_room:
        raise NotFoundException("Room not found")

    await crud_rooms.delete(db=db, id=id)
    return {"message": "Room deleted"}

