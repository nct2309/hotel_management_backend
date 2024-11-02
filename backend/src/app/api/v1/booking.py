from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Query
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_booking import crud_bookings
from ...schemas.booking import BookingCreate, BookingDelete, BookingRead, BookingUpdate, BookingUpdateInternal

router = APIRouter(tags=["bookings"])

@router.post("/booking", response_model=BookingRead, status_code=201)
async def write_booking(
    request: Request, booking: BookingCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> BookingRead:
    created_booking: BookingRead = await crud_bookings.create(db=db, object=booking)
    return created_booking

@router.get("/bookings", response_model=PaginatedListResponse[BookingRead])
async def read_bookings(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    bookings_data = await crud_bookings.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=BookingRead,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=bookings_data, page=page, items_per_page=items_per_page)
    return response

@router.get("/booking/{id}", response_model=BookingRead)
async def read_booking(request: Request, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_booking: BookingRead | None = await crud_bookings.get(
        db=db, schema_to_select=BookingRead, id=id, is_deleted=False
    )
    if db_booking is None:
        raise NotFoundException("Booking not found")

    return dict(db_booking)

@router.put("/booking/{id}", response_model=dict)
async def update_booking(
    request: Request, id: int, booking: BookingUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    updated_booking: BookingRead = await crud_bookings.update(db=db, id=id, object=booking)
    return {"message": "Booking updated successfully"}

@router.delete("/booking/{id}", response_model=dict)
async def delete_booking(
    request: Request, id: int, booking: BookingDelete, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    deleted_booking: BookingRead = await crud_bookings.delete(db=db, id=id, object=booking)
    return {"message": "Booking deleted successfully"}

# get all bookings of a user
@router.get("/user/{user_id}/bookings", response_model=PaginatedListResponse[BookingRead])
async def read_user_bookings(
    request: Request, user_id: int, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    bookings_data = await crud_bookings.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=BookingRead,
        is_deleted=False,
        user_id=user_id,
        sort_columns=["check_in"],
        sort_order="desc",
    )

    response: dict[str, Any] = paginated_response(crud_data=bookings_data, page=page, items_per_page=items_per_page)
    return response