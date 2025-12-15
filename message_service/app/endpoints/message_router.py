from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.services.message_service import MessageService
from app.repositories.message_repo import MessageRepository
from app.models.message import Message, MessageCreate, MessageList
from app.database import get_db
from sqlalchemy.orm import Session

message_router = APIRouter(prefix="/messages", tags=["Messages"])

def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    repo = MessageRepository(db)
    return MessageService(repo)

# Заглушка для авторизации
def get_current_user() -> UUID:
    return UUID("12345678-1234-1234-1234-123456789abc")

@message_router.get("/", response_model=MessageList)
def get_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: MessageService = Depends(get_message_service),
    user_id: UUID = Depends(get_current_user)
):
    return service.get_messages(user_id, skip, limit)

@message_router.get("/advertisement/{advertisement_id}", response_model=MessageList)
def get_messages_by_advertisement(
    advertisement_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: MessageService = Depends(get_message_service),
    user_id: UUID = Depends(get_current_user)
):
    return service.get_messages_by_advertisement(advertisement_id, user_id, skip, limit)

@message_router.get("/interlocutor/{interlocutor_id}", response_model=MessageList)
def get_messages_by_interlocutor(
    interlocutor_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service: MessageService = Depends(get_message_service),
    user_id: UUID = Depends(get_current_user)
):
    return service.get_messages_by_interlocutor(interlocutor_id, user_id, skip, limit)

@message_router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    service: MessageService = Depends(get_message_service),
    user_id: UUID = Depends(get_current_user)
):
    return service.send_message(message_data, user_id)

@message_router.post("/{message_id}/read", response_model=Message)
def read_message(
    message_id: UUID,
    service: MessageService = Depends(get_message_service),
    user_id: UUID = Depends(get_current_user)
):
    message = service.read_message(message_id, user_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found or access denied")
    return message