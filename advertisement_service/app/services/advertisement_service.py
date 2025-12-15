from uuid import UUID
from app.repositories.advertisement_repo import AdvertisementRepository
from app.models.advertisement import Advertisement, AdvertisementCreate, AdvertisementUpdate

class AdvertisementService:
    def __init__(self, advertisement_repo: AdvertisementRepository):
        self.advertisement_repo = advertisement_repo

    def get_advertisements(self, skip: int = 0, limit: int = 100) -> list[Advertisement]:
        return self.advertisement_repo.get_advertisements(skip, limit)

    def get_advertisement(self, ad_id: UUID) -> Advertisement | None:
        return self.advertisement_repo.get_advertisement_by_id(ad_id)

    def create_advertisement(self, ad_data: AdvertisementCreate, author_id: UUID) -> Advertisement:
        return self.advertisement_repo.create_advertisement(ad_data.model_dump(), author_id)

    def update_advertisement(self, ad_id: UUID, update_data: AdvertisementUpdate, user_id: UUID) -> Advertisement | None:
        ad = self.advertisement_repo.get_advertisement_by_id(ad_id)
        if not ad or ad.author_id != user_id:
            return None
        return self.advertisement_repo.update_advertisement(ad_id, update_data.model_dump(exclude_unset=True))

    def publish_advertisement(self, ad_id: UUID, user_id: UUID) -> Advertisement | None:
        ad = self.advertisement_repo.get_advertisement_by_id(ad_id)
        if not ad or ad.author_id != user_id:
            return None
        return self.advertisement_repo.publish_advertisement(ad_id)

    def delete_advertisement(self, ad_id: UUID, user_id: UUID) -> bool:
        ad = self.advertisement_repo.get_advertisement_by_id(ad_id)
        if not ad or ad.author_id != user_id:
            return False
        return self.advertisement_repo.delete_advertisement(ad_id)