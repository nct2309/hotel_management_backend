from typing import List
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    
    description: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    features: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    badges: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    
    # id: 1,
    # name: "Deluxe Ocean View Suite",
    # description: "Experience luxury with a breathtaking view",
    # image: "/placeholder.svg?height=200&width=300",
    # price: 299,
    # features: ["King-size bed", "Up to 3 guests", "Free WiFi", "55\" 4K Smart TV", "Coffee machine"],
    # badges: ["Ocean View", "Non-smoking", "Free Cancellation"],