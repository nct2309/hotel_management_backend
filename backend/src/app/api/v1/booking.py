from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Query
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_booking import crud_bookings
from ...crud.crud_rooms import crud_rooms
from ...schemas.booking import BookingCreate, BookingDelete, BookingRead, BookingUpdate, BookingUpdateInternal
from ...schemas.room import RoomRead, RoomUpdate

router = APIRouter(tags=["bookings"])

@router.post("/booking", response_model=BookingRead, status_code=201)
async def write_booking(
    request: Request, booking: BookingCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> BookingRead:
    """_summary_

    Args:
        request (Request): _description_
        booking (BookingCreate): _description_
        db (Annotated[AsyncSession, Depends): _description_

    Returns:
        BookingRead: _description_
    Further details:
    - If the booking status is confirmed, the room status will be updated to "booked".
    """
    created_booking: BookingRead = await crud_bookings.create(db=db, object=booking)
    
    if created_booking.status == "confirmed":
        # update room status to booked
        updated_room: RoomRead = await crud_rooms.update(db=db, id=created_booking.room_id, object=RoomUpdate(status="booked", from_date=created_booking.check_in, to_date=created_booking.check_out))

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

@router.post("/booking/{id}/cancel")
async def cancel_booking(
    request: Request, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    """_summary_

    Args:
        request (Request): _description_
        id (int): _description_
        db (Annotated[AsyncSession, Depends): _description_

    Raises:
        NotFoundException: _description_

    Returns:
        _type_: _description_
    Further details:
    - If the booking status is cancelled, the room status will be updated to "available".
    - If the booking status is pending or confirmed, the booking status will be updated to "cancelled".
    - If the booking status is checked_out, the booking status will not be updated.
    
    """
    booking: BookingRead = await crud_bookings.get(db=db, schema_to_select=BookingRead, id=id, is_deleted=False)
    if booking is None:
        raise NotFoundException("Booking not found")
    
    if booking.get("status") == "cancelled":
        return {
            "message": "Booking already cancelled"
        }
        
    if booking.get("status") == "pending" or booking.get("status") == "confirmed":
        updated_booking: BookingRead = await crud_bookings.update(db=db, id=id, object=BookingUpdate(status="cancelled"))
        
        # update room status to available
        updated_room: RoomRead = await crud_rooms.update(db=db, id=booking.get("room_id"), object=RoomUpdate(status="available", from_date=None, to_date=None))
        
        return {
            "message": "Booking cancelled successfully"
        }
        
    # booking status is checked_out    
    return {
        "message": "Booking already checked out"
    }