from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.advertisement import AdvertisementDB
from app.models.advertisement import Advertisement  # УБРАТЬ AdvertisementStatus из импорта
from app.database import get_db
from datetime import datetime, timezone  # ДОБАВИТЬ импорт


class AdvertisementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_advertisements(self, skip: int = 0, limit: int = 100) -> list[Advertisement]:
        ads = self.db.query(AdvertisementDB).offset(skip).limit(limit).all()
        return [Advertisement(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            price=ad.price,
            category=ad.category,
            status=ad.status,  # ПРОСТО ad.status БЕЗ AdvertisementStatus()
            author_id=ad.author_id,
            created_at=ad.created_at,
            updated_at=ad.updated_at,
            published_at=ad.published_at
        ) for ad in ads]

    def get_advertisement_by_id(self, ad_id: UUID) -> Advertisement | None:
        ad = self.db.query(AdvertisementDB).filter(AdvertisementDB.id == ad_id).first()
        if ad:
            return Advertisement(
                id=ad.id,
                title=ad.title,
                description=ad.description,
                price=ad.price,
                category=ad.category,
                status=ad.status,  # ПРОСТО ad.status БЕЗ AdvertisementStatus()
                author_id=ad.author_id,
                created_at=ad.created_at,
                updated_at=ad.updated_at,
                published_at=ad.published_at
            )
        return None

    def create_advertisement(self, ad_data: dict, author_id: UUID) -> Advertisement:
        db_ad = AdvertisementDB(**ad_data, author_id=author_id, status='draft')
        self.db.add(db_ad)
        self.db.commit()
        self.db.refresh(db_ad)

        return Advertisement(
            id=db_ad.id,
            title=db_ad.title,
            description=db_ad.description,
            price=db_ad.price,
            category=db_ad.category,
            status=db_ad.status,  # Оставить как есть
            author_id=db_ad.author_id,
            created_at=db_ad.created_at,
            updated_at=db_ad.updated_at,
            published_at=db_ad.published_at
        )

    def update_advertisement(self, ad_id: UUID, update_data: dict) -> Advertisement | None:
        db_ad = self.db.query(AdvertisementDB).filter(AdvertisementDB.id == ad_id).first()
        if not db_ad:
            return None

        for key, value in update_data.items():
            if value is not None:
                setattr(db_ad, key, value)

        self.db.commit()
        self.db.refresh(db_ad)

        return Advertisement(
            id=db_ad.id,
            title=db_ad.title,
            description=db_ad.description,
            price=db_ad.price,
            category=db_ad.category,
            status=db_ad.status,  # ПРОСТО ad.status БЕЗ AdvertisementStatus()
            author_id=db_ad.author_id,
            created_at=db_ad.created_at,
            updated_at=db_ad.updated_at,
            published_at=db_ad.published_at
        )

    def publish_advertisement(self, ad_id: UUID) -> Advertisement | None:
        db_ad = self.db.query(AdvertisementDB).filter(AdvertisementDB.id == ad_id).first()
        if not db_ad:
            return None

        db_ad.status = 'published'
        db_ad.published_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(db_ad)

        return Advertisement(
            id=db_ad.id,
            title=db_ad.title,
            description=db_ad.description,
            price=db_ad.price,
            category=db_ad.category,
            status=db_ad.status,  # ПРОСТО ad.status БЕЗ AdvertisementStatus()
            author_id=db_ad.author_id,
            created_at=db_ad.created_at,
            updated_at=db_ad.updated_at,
            published_at=db_ad.published_at
        )

    def delete_advertisement(self, ad_id: UUID) -> bool:
        db_ad = self.db.query(AdvertisementDB).filter(AdvertisementDB.id == ad_id).first()
        if not db_ad:
            return False

        self.db.delete(db_ad)
        self.db.commit()
        return True