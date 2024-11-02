from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema
    
class RoomBase(BaseModel):
    name: Annotated[str, Field(examples=["Deluxe Ocean View Suite"])]
    description: Annotated[str, Field(examples=["Experience luxury with a breathtaking view"])]
    image_2d: Annotated[str, Field(examples=["/placeholder.svg?height=200&width=300"])] = ""
    image_3d: Annotated[str, Field(examples=["/placeholder.svg?height=200&width=300"])] = ""
    price: Annotated[float, Field(examples=[299])]
    feature_ids: Annotated[list[int], Field(examples=[[1, 2, 3]])]
    badge_ids: Annotated[list[int], Field(examples=[[1, 2, 3]])]


class Room(TimestampSchema, RoomBase, UUIDSchema, PersistentDeletion):
    pass

class RoomRead(BaseModel):
    id: int
    name: str
    description: str
    image_2d: str = ""
    image_3d: str = ""
    price: float
    feature_ids: list[int]
    badge_ids: list[int]

class RoomReadExternal(RoomRead):
    features: list[dict]
    badges: list[dict]
    
class RoomCreate(RoomBase):
    model_config = ConfigDict(extra="forbid")
    
class RoomUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: Annotated[str | None, Field(examples=["Deluxe Ocean View Suite"], default=None)]
    description: Annotated[str | None, Field(examples=["Experience luxury with a breathtaking view"], default=None)]
    image_2d: Annotated[str | None, Field(examples=["/placeholder.svg?height=200&width=300"], default=None)] = ""
    image_3d: Annotated[str | None, Field(examples=["/placeholder.svg?height=200&width=300"], default=None)] = ""
    price: Annotated[float | None, Field(examples=[299], default=None)]
    feature_ids: Annotated[list[int] | None, Field(examples=[[1, 2, 3]], default=None)]
    badge_ids: Annotated[list[int] | None, Field(examples=[[1, 2, 3]], default=None)]

class RoomUpdateInternal(RoomUpdate):
    updated_at: datetime
       
class RoomDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    is_deleted: bool
    deleted_at: datetime
    
class RoomFeatureBase(BaseModel):
    name: Annotated[str, Field(examples=["King-size bed"])]
    description: Annotated[str, Field(examples=["A large bed fit for a king"])]

class RoomFeatureDetail(RoomFeatureBase):
    id: int
    
class RoomBadgeBase(BaseModel):
    name: Annotated[str, Field(examples=["Ocean View"])]
    description: Annotated[str, Field(examples=["A room with a view of the ocean"])]
    
class RoomBadgeDetail(RoomBadgeBase):
    id: int