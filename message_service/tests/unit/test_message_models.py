import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError
from app.models.message import Message, MessageCreate, MessageStatus


class TestMessageModels:
    def test_message_creation_valid(self):
        message_id = uuid4()
        sender_id = uuid4()
        receiver_id = uuid4()
        advertisement_id = uuid4()
        now = datetime.now(timezone.utc)

        message = Message(
            id=message_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            advertisement_id=advertisement_id,
            text="Hello, this is a test message",
            status=MessageStatus.SENT,
            created_at=now
        )

        assert message.id == message_id
        assert message.sender_id == sender_id
        assert message.text == "Hello, this is a test message"
        assert message.status == MessageStatus.SENT

    def test_message_create_valid(self):
        receiver_id = uuid4()
        advertisement_id = uuid4()

        message_data = MessageCreate(
            receiver_id=receiver_id,
            advertisement_id=advertisement_id,
            text="I'm interested in your advertisement"
        )

        assert message_data.receiver_id == receiver_id
        assert message_data.advertisement_id == advertisement_id
        assert message_data.text == "I'm interested in your advertisement"

    def test_message_create_invalid_uuid(self):
        with pytest.raises(ValidationError):
            MessageCreate(
                receiver_id="invalid-uuid",
                advertisement_id=uuid4(),
                text="Test message"
            )