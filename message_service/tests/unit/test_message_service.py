import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from fastapi import HTTPException
from app.services.message_service import MessageService
from app.models.message import Message, MessageCreate, MessageList, MessageStatus


class TestMessageService:
    @pytest.fixture
    def message_service(self):
        mock_repo = Mock()
        with patch.object(MessageService, '__init__', lambda self, repo: setattr(self, 'message_repo', repo)):
            return MessageService(mock_repo)

    def test_send_message_success(self, message_service):
        sender_id = uuid4()
        receiver_id = uuid4()
        advertisement_id = uuid4()

        message_data = MessageCreate(
            receiver_id=receiver_id,
            advertisement_id=advertisement_id,
            text="Hello, I'm interested in your ad!"
        )

        mock_message = Message(
            id=uuid4(),
            sender_id=sender_id,
            receiver_id=receiver_id,
            advertisement_id=advertisement_id,
            text="Hello, I'm interested in your ad!",
            status=MessageStatus.SENT,
            created_at="2023-01-01T00:00:00"
        )

        message_service.message_repo.create_message.return_value = mock_message

        result = message_service.send_message(message_data, sender_id)
        assert result.text == "Hello, I'm interested in your ad!"
        assert result.sender_id == sender_id
        assert result.status == MessageStatus.SENT
        message_service.message_repo.create_message.assert_called_once()

    def test_get_messages(self, message_service):
        user_id = uuid4()
        mock_messages = [
            Message(
                id=uuid4(), sender_id=user_id, receiver_id=uuid4(),
                advertisement_id=uuid4(), text="Test message 1",
                status=MessageStatus.SENT, created_at="2023-01-01T00:00:00"
            )
        ]

        message_service.message_repo.get_messages.return_value = mock_messages

        result = message_service.get_messages(user_id, 0, 10)
        assert isinstance(result, MessageList)
        assert len(result.items) == 1
        assert result.total == 1
        assert result.limit == 10
        assert result.offset == 0

    def test_read_message_success(self, message_service):
        message_id = uuid4()
        user_id = uuid4()

        mock_message = Message(
            id=message_id, sender_id=uuid4(), receiver_id=user_id,
            advertisement_id=uuid4(), text="Test message",
            status=MessageStatus.READ, created_at="2023-01-01T00:00:00",
            read_at="2023-01-01T00:01:00"
        )

        message_service.message_repo.mark_as_read.return_value = mock_message

        result = message_service.read_message(message_id, user_id)
        assert result.status == MessageStatus.READ
        assert result.read_at is not None
        message_service.message_repo.mark_as_read.assert_called_once_with(message_id, user_id)

    def test_read_message_not_receiver(self, message_service):
        message_id = uuid4()
        user_id = uuid4()  # Not the receiver

        message_service.message_repo.mark_as_read.return_value = None

        result = message_service.read_message(message_id, user_id)
        assert result is None