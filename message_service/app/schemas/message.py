from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from datetime import datetime, timezone
from uuid import uuid4

class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sender_id = Column(UUID(as_uuid=True), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), nullable=False)
    advertisement_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(String, nullable=False)
    status = Column(String, default='sent')  # Просто String вместо ENUM
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    read_at = Column(DateTime, nullable=True)