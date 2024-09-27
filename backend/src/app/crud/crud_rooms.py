from fastcrud import FastCRUD

from ..models.room import Room
from ..schemas.room import RoomCreate, RoomDelete, RoomUpdate, RoomUpdateInternal

CRUDRoom = FastCRUD[Room, RoomCreate, RoomUpdate, RoomUpdateInternal, RoomDelete]
crud_rooms = CRUDRoom(Room)
