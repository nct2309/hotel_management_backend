from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema
    
class RoomBase(BaseModel):
    name: Annotated[str, Field(examples=["Deluxe Ocean View Suite"])]
    description: Annotated[str, Field(examples=["Experience luxury with a breathtaking view"])]
    image: Annotated[str, Field(examples=["/placeholder.svg?height=200&width=300"])]
    price: Annotated[float, Field(examples=[299])]
    features: Annotated[list[str], Field(examples=[["King-size bed", "Up to 3 guests", "Free WiFi", "55\" 4K Smart TV", "Coffee machine"]])]
    badges: Annotated[list[str], Field(examples=[["Ocean View", "Non-smoking", "Free Cancellation"]])]


class Room(TimestampSchema, RoomBase, UUIDSchema, PersistentDeletion):
    pass

class RoomRead(BaseModel):
    id: int
    name: str
    description: str
    image: str
    price: float
    features: list[str]
    badges: list[str]
    
class RoomCreate(RoomBase):
    model_config = ConfigDict(extra="forbid")
    
class RoomUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: Annotated[str | None, Field(examples=["Deluxe Ocean View Suite"], default=None)]
    description: Annotated[str | None, Field(examples=["Experience luxury with a breathtaking view"], default=None)]
    image: Annotated[str | None, Field(examples=["/placeholder.svg?height=200&width=300"], default=None)]
    price: Annotated[float | None, Field(examples=[299], default=None)]
    features: Annotated[list[str] | None, Field(examples=[["King-size bed", "Up to 3 guests", "Free WiFi", "55\" 4K Smart TV", "Coffee machine"]], default=None)]
    badges: Annotated[list[str] | None, Field(examples=[["Ocean View", "Non-smoking", "Free Cancellation"]], default=None)]

class RoomUpdateInternal(RoomUpdate):
    updated_at: datetime
       
class RoomDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    is_deleted: bool
    deleted_at: datetime