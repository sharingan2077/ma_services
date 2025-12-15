import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from fastapi import HTTPException
from app.services.advertisement_service import AdvertisementService
from app.models.advertisement import Advertisement, AdvertisementCreate, AdvertisementUpdate, AdvertisementStatus


class TestAdvertisementService:
    @pytest.fixture
    def advertisement_service(self):
        mock_repo = Mock()
        with patch.object(AdvertisementService, '__init__',
                          lambda self, repo: setattr(self, 'advertisement_repo', repo)):
            return AdvertisementService(mock_repo)

    def test_get_advertisements(self, advertisement_service):
        mock_ads = [
            Advertisement(
                id=uuid4(), title="Test Ad 1", description="Desc 1", price=100.0,
                category="test", status=AdvertisementStatus.DRAFT, author_id=uuid4(),
                created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
            )
        ]
        advertisement_service.advertisement_repo.get_advertisements.return_value = mock_ads

        result = advertisement_service.get_advertisements(0, 10)
        assert len(result) == 1
        assert result[0].title == "Test Ad 1"

    def test_create_advertisement(self, advertisement_service):
        user_id = uuid4()
        ad_data = AdvertisementCreate(
            title="New Ad", description="New Description", price=50.0, category="test"
        )

        mock_ad = Advertisement(
            id=uuid4(), title="New Ad", description="New Description", price=50.0,
            category="test", status=AdvertisementStatus.DRAFT, author_id=user_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
        )
        advertisement_service.advertisement_repo.create_advertisement.return_value = mock_ad

        result = advertisement_service.create_advertisement(ad_data, user_id)
        assert result.title == "New Ad"
        assert result.author_id == user_id
        advertisement_service.advertisement_repo.create_advertisement.assert_called_once()

    def test_update_advertisement_success(self, advertisement_service):
        user_id = uuid4()
        ad_id = uuid4()

        existing_ad = Advertisement(
            id=ad_id, title="Old Title", description="Old Desc", price=100.0,
            category="test", status=AdvertisementStatus.DRAFT, author_id=user_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
        )

        updated_ad = Advertisement(
            id=ad_id, title="New Title", description="Old Desc", price=100.0,
            category="test", status=AdvertisementStatus.DRAFT, author_id=user_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
        )

        advertisement_service.advertisement_repo.get_advertisement_by_id.return_value = existing_ad
        advertisement_service.advertisement_repo.update_advertisement.return_value = updated_ad

        update_data = AdvertisementUpdate(title="New Title")
        result = advertisement_service.update_advertisement(ad_id, update_data, user_id)

        assert result.title == "New Title"
        advertisement_service.advertisement_repo.update_advertisement.assert_called_once()

    def test_update_advertisement_not_owner(self, advertisement_service):
        ad_id = uuid4()
        owner_id = uuid4()
        other_user_id = uuid4()

        existing_ad = Advertisement(
            id=ad_id, title="Test Ad", description="Desc", price=100.0,
            category="test", status=AdvertisementStatus.DRAFT, author_id=owner_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
        )

        advertisement_service.advertisement_repo.get_advertisement_by_id.return_value = existing_ad

        update_data = AdvertisementUpdate(title="New Title")
        result = advertisement_service.update_advertisement(ad_id, update_data, other_user_id)

        assert result is None
        advertisement_service.advertisement_repo.update_advertisement.assert_not_called()

    def test_publish_advertisement_success(self, advertisement_service):
        user_id = uuid4()
        ad_id = uuid4()

        existing_ad = Advertisement(
            id=ad_id, title="Test Ad", description="Desc", price=100.0,
            category="test", status=AdvertisementStatus.DRAFT, author_id=user_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00"
        )

        published_ad = Advertisement(
            id=ad_id, title="Test Ad", description="Desc", price=100.0,
            category="test", status=AdvertisementStatus.PUBLISHED, author_id=user_id,
            created_at="2023-01-01T00:00:00", updated_at="2023-01-01T00:00:00",
            published_at="2023-01-01T00:00:00"
        )

        advertisement_service.advertisement_repo.get_advertisement_by_id.return_value = existing_ad
        advertisement_service.advertisement_repo.publish_advertisement.return_value = published_ad

        result = advertisement_service.publish_advertisement(ad_id, user_id)
        assert result.status == AdvertisementStatus.PUBLISHED
        advertisement_service.advertisement_repo.publish_advertisement.assert_called_once()