import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from app.models.advertisement import Advertisement, AdvertisementCreate, AdvertisementUpdate, AdvertisementStatus
from datetime import datetime, timezone


class TestAdvertisementModels:
    def test_advertisement_creation_valid(self):
        ad_id = uuid4()
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        ad = Advertisement(
            id=ad_id,
            title="Test Advertisement",
            description="Test Description",
            price=99.99,
            category="electronics",
            status=AdvertisementStatus.DRAFT,
            author_id=user_id,
            created_at=now,
            updated_at=now
        )

        assert ad.id == ad_id
        assert ad.title == "Test Advertisement"
        assert ad.price == 99.99
        assert ad.status == AdvertisementStatus.DRAFT

    def test_advertisement_create_valid(self):
        ad_data = AdvertisementCreate(
            title="New Ad",
            description="New Description",
            price=50.0,
            category="books"
        )

        assert ad_data.title == "New Ad"
        assert ad_data.description == "New Description"
        assert ad_data.price == 50.0
        assert ad_data.category == "books"

    def test_advertisement_update_valid(self):
        update_data = AdvertisementUpdate(
            title="Updated Title",
            price=75.0
        )

        assert update_data.title == "Updated Title"
        assert update_data.price == 75.0
        assert update_data.description is None

    def test_advertisement_create_invalid_price(self):
        with pytest.raises(ValidationError):
            AdvertisementCreate(
                title="Test Ad",
                description="Test Desc",
                price=-10.0,  # Invalid negative price
                category="test"
            )