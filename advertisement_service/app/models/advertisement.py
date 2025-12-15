import enum
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator



class AdvertisementStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Advertisement(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    price: float
    category: str
    status: AdvertisementStatus
    author_id: UUID
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None


class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float
    category: str

    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None