from uuid import UUID
from app.repositories.message_repo import MessageRepository
from app.models.message import Message, MessageCreate, MessageList

class MessageService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    def get_messages(self, user_id: UUID, skip: int = 0, limit: int = 50) -> MessageList:
        messages = self.message_repo.get_messages(user_id, skip, limit)
        return MessageList(
            items=messages,
            total=len(messages),
            limit=limit,
            offset=skip
        )

    def get_messages_by_advertisement(self, advertisement_id: UUID, user_id: UUID, skip: int = 0, limit: int = 50) -> MessageList:
        messages = self.message_repo.get_messages_by_advertisement(advertisement_id, user_id, skip, limit)
        return MessageList(
            items=messages,
            total=len(messages),
            limit=limit,
            offset=skip
        )

    def get_messages_by_interlocutor(self, interlocutor_id: UUID, user_id: UUID, skip: int = 0, limit: int = 50) -> MessageList:
        messages = self.message_repo.get_messages_by_interlocutor(interlocutor_id, user_id, skip, limit)
        return MessageList(
            items=messages,
            total=len(messages),
            limit=limit,
            offset=skip
        )

    def send_message(self, message_data: MessageCreate, sender_id: UUID) -> Message:
        return self.message_repo.create_message(message_data.model_dump(), sender_id)

    def read_message(self, message_id: UUID, user_id: UUID) -> Message | None:
        return self.message_repo.mark_as_read(message_id, user_id)