from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.message import MessageDB
from app.models.message import Message
from datetime import datetime, timezone

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_messages(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Message]:
        messages = self.db.query(MessageDB).filter(
            (MessageDB.sender_id == user_id) | (MessageDB.receiver_id == user_id)
        ).offset(skip).limit(limit).all()

        return [self._to_model(msg) for msg in messages]

    def get_messages_by_advertisement(self, advertisement_id: UUID, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Message]:
        messages = self.db.query(MessageDB).filter(
            MessageDB.advertisement_id == advertisement_id,
            (MessageDB.sender_id == user_id) | (MessageDB.receiver_id == user_id)
        ).offset(skip).limit(limit).all()

        return [self._to_model(msg) for msg in messages]

    def get_messages_by_interlocutor(self, interlocutor_id: UUID, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Message]:
        messages = self.db.query(MessageDB).filter(
            ((MessageDB.sender_id == user_id) & (MessageDB.receiver_id == interlocutor_id)) |
            ((MessageDB.sender_id == interlocutor_id) & (MessageDB.receiver_id == user_id))
        ).offset(skip).limit(limit).all()

        return [self._to_model(msg) for msg in messages]

    def get_message_by_id(self, message_id: UUID) -> Message | None:
        message = self.db.query(MessageDB).filter(MessageDB.id == message_id).first()
        return self._to_model(message) if message else None

    def create_message(self, message_data: dict, sender_id: UUID) -> Message:
        db_message = MessageDB(**message_data, sender_id=sender_id, status='sent')  # Явно указываем статус
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return self._to_model(db_message)

    def mark_as_read(self, message_id: UUID, user_id: UUID) -> Message | None:
        message = self.db.query(MessageDB).filter(
            MessageDB.id == message_id,
            MessageDB.receiver_id == user_id
        ).first()

        if not message:
            return None

        message.status = 'read'  # Используем строку
        message.read_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(message)
        return self._to_model(message)

    def _to_model(self, db_message: MessageDB) -> Message:
        return Message(
            id=db_message.id,
            sender_id=db_message.sender_id,
            receiver_id=db_message.receiver_id,
            advertisement_id=db_message.advertisement_id,
            text=db_message.text,
            status=db_message.status,  # Просто передаем строку
            created_at=db_message.created_at,
            read_at=db_message.read_at
        )