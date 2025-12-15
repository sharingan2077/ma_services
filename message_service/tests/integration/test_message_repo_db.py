import pytest
from uuid import uuid4
from app.repositories.message_repo import MessageRepository
from app.models.message import MessageStatus


class TestMessageRepoIntegration:
    @pytest.fixture
    def message_repo(self, session):
        return MessageRepository(session)

    def test_create_and_retrieve_message(self, message_repo):
        sender_id = uuid4()
        receiver_id = uuid4()
        advertisement_id = uuid4()

        message_data = {
            "receiver_id": receiver_id,
            "advertisement_id": advertisement_id,
            "text": "Integration test message"
        }

        message = message_repo.create_message(message_data, sender_id)
        assert message.text == "Integration test message"
        assert message.sender_id == sender_id
        assert message.receiver_id == receiver_id
        assert message.status == "sent"

        # Retrieve by ID
        found_message = message_repo.get_message_by_id(message.id)
        assert found_message is not None
        assert found_message.text == "Integration test message"

    def test_get_messages_by_user(self, message_repo):
        user_id = uuid4()
        other_user_id = uuid4()
        advertisement_id = uuid4()

        # Create messages involving the user
        message_data1 = {"receiver_id": other_user_id, "advertisement_id": advertisement_id, "text": "Message 1"}
        message_data2 = {"receiver_id": user_id, "advertisement_id": advertisement_id, "text": "Message 2"}

        message_repo.create_message(message_data1, user_id)  # User is sender
        message_repo.create_message(message_data2, other_user_id)  # User is receiver

        messages = message_repo.get_messages(user_id, 0, 10)
        assert len(messages) == 2

    def test_mark_as_read(self, message_repo):
        sender_id = uuid4()
        receiver_id = uuid4()
        advertisement_id = uuid4()

        message_data = {
            "receiver_id": receiver_id,
            "advertisement_id": advertisement_id,
            "text": "Message to be read"
        }

        message = message_repo.create_message(message_data, sender_id)
        assert message.status == "sent"
        assert message.read_at is None

        # Mark as read by receiver
        read_message = message_repo.mark_as_read(message.id, receiver_id)
        assert read_message.status == "read"
        assert read_message.read_at is not None

        # Try to mark as read by non-receiver (should return None)
        not_receiver_result = message_repo.mark_as_read(message.id, uuid4())
        assert not_receiver_result is None

    def test_get_messages_by_advertisement(self, message_repo):
        user1_id = uuid4()
        user2_id = uuid4()
        advertisement_id = uuid4()
        other_advertisement_id = uuid4()

        # Create messages for specific advertisement
        message_data1 = {"receiver_id": user2_id, "advertisement_id": advertisement_id, "text": "Ad message 1"}
        message_data2 = {"receiver_id": user1_id, "advertisement_id": advertisement_id, "text": "Ad message 2"}
        message_data3 = {"receiver_id": user2_id, "advertisement_id": other_advertisement_id,
                         "text": "Other ad message"}

        message_repo.create_message(message_data1, user1_id)
        message_repo.create_message(message_data2, user2_id)
        message_repo.create_message(message_data3, user1_id)

        # Get messages for specific advertisement and user
        ad_messages = message_repo.get_messages_by_advertisement(advertisement_id, user1_id, 0, 10)
        assert len(ad_messages) == 2