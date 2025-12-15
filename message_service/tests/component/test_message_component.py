from uuid import uuid4
from unittest.mock import Mock
from fastapi.testclient import TestClient

# Компонентный тест 1: Проверка отправки и получения сообщений
def test_message_send_and_get_flow():
    from app.main import app
    from app.endpoints.message_router import get_message_service, get_current_user

    # Arrange
    test_user_id = uuid4()

    # Создаем mock сервиса
    mock_service = Mock()

    # Настраиваем mock сообщение
    mock_message = Mock()
    mock_message.id = uuid4()
    mock_message.sender_id = test_user_id
    mock_message.receiver_id = uuid4()
    mock_message.advertisement_id = uuid4()
    mock_message.text = "Test message"
    mock_message.status = "sent"
    mock_message.created_at = "2024-01-01T12:00:00"
    mock_message.read_at = None

    mock_message.model_dump = Mock(return_value={
        "id": str(mock_message.id),
        "sender_id": str(mock_message.sender_id),
        "receiver_id": str(mock_message.receiver_id),
        "advertisement_id": str(mock_message.advertisement_id),
        "text": mock_message.text,
        "status": mock_message.status,
        "created_at": mock_message.created_at,
        "read_at": mock_message.read_at
    })

    mock_message_list = Mock()
    mock_message_list.items = [mock_message]
    mock_message_list.total = 1
    mock_message_list.limit = 50
    mock_message_list.offset = 0

    mock_message_list.model_dump = Mock(return_value={
        "items": [mock_message.model_dump()],
        "total": 1,
        "limit": 50,
        "offset": 0
    })

    mock_service.send_message.return_value = mock_message
    mock_service.get_messages.return_value = mock_message_list

    # Переопределяем зависимости
    def mock_get_message_service():
        return mock_service

    def mock_get_current_user():
        return test_user_id

    # Сохраняем оригиналы
    original_service = app.dependency_overrides.get(get_message_service)
    original_user = app.dependency_overrides.get(get_current_user)

    app.dependency_overrides[get_message_service] = mock_get_message_service
    app.dependency_overrides[get_current_user] = mock_get_current_user

    try:
        # Act
        with TestClient(app) as client:
            # Отправка сообщения
            response = client.post(
                "/api/messages/",
                json={
                    "receiver_id": str(uuid4()),
                    "advertisement_id": str(uuid4()),
                    "text": "Test message"
                }
            )

            # Assert
            assert response.status_code == 201

            # Получение сообщений
            response = client.get("/api/messages/")
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 1

            # Проверяем вызовы сервиса
            assert mock_service.send_message.called
            assert mock_service.get_messages.called

    finally:
        # Восстанавливаем зависимости
        if original_service:
            app.dependency_overrides[get_message_service] = original_service
        else:
            app.dependency_overrides.pop(get_message_service, None)

        if original_user:
            app.dependency_overrides[get_current_user] = original_user
        else:
            app.dependency_overrides.pop(get_current_user, None)


# Компонентный тест 2: Проверка чтения сообщений и обработки ошибок
def test_read_message_flow():
    from app.main import app
    from app.endpoints.message_router import get_message_service, get_current_user

    # Arrange
    test_user_id = uuid4()
    message_id = uuid4()

    # Создаем mock сервиса
    mock_service = Mock()

    # Настраиваем mock сообщение
    mock_message = Mock()
    mock_message.id = message_id
    mock_message.sender_id = uuid4()
    mock_message.receiver_id = test_user_id
    mock_message.advertisement_id = uuid4()
    mock_message.text = "Test message"
    mock_message.status = "read"
    mock_message.created_at = "2024-01-01T12:00:00"
    mock_message.read_at = "2024-01-01T12:01:00"

    mock_message.model_dump = Mock(return_value={
        "id": str(mock_message.id),
        "sender_id": str(mock_message.sender_id),
        "receiver_id": str(mock_message.receiver_id),
        "advertisement_id": str(mock_message.advertisement_id),
        "text": mock_message.text,
        "status": mock_message.status,
        "created_at": mock_message.created_at,
        "read_at": mock_message.read_at
    })

    mock_service.read_message.return_value = mock_message

    # Переопределяем зависимости
    def mock_get_message_service():
        return mock_service

    def mock_get_current_user():
        return test_user_id

    # Сохраняем оригиналы
    original_service = app.dependency_overrides.get(get_message_service)
    original_user = app.dependency_overrides.get(get_current_user)

    app.dependency_overrides[get_message_service] = mock_get_message_service
    app.dependency_overrides[get_current_user] = mock_get_current_user

    try:
        # Act
        with TestClient(app) as client:
            # Успешное чтение
            response = client.post(f"/api/messages/{message_id}/read")
            assert response.status_code == 200

            # Проверяем вызов сервиса
            mock_service.read_message.assert_called_once_with(
                message_id, test_user_id
            )

            # Тест ошибки - сообщение не найдено
            mock_service.read_message.reset_mock()
            mock_service.read_message.return_value = None

            response = client.post(f"/api/messages/{uuid4()}/read")
            assert response.status_code == 404

    finally:
        # Восстанавливаем зависимости
        if original_service:
            app.dependency_overrides[get_message_service] = original_service
        else:
            app.dependency_overrides.pop(get_message_service, None)

        if original_user:
            app.dependency_overrides[get_current_user] = original_user
        else:
            app.dependency_overrides.pop(get_current_user, None)