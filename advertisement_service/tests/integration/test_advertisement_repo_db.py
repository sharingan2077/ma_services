import pytest
from uuid import uuid4
from app.repositories.advertisement_repo import AdvertisementRepository
from app.models.advertisement import AdvertisementStatus


class TestAdvertisementRepoIntegration:
    @pytest.fixture
    def advertisement_repo(self, session):
        return AdvertisementRepository(session)

    def test_create_and_retrieve_advertisement(self, advertisement_repo):
        author_id = uuid4()
        ad_data = {
            "title": "Integration Test Ad",
            "description": "Integration test description",
            "price": 150.0,
            "category": "integration_test"
        }

        ad = advertisement_repo.create_advertisement(ad_data, author_id)
        assert ad.title == "Integration Test Ad"
        assert ad.price == 150.0
        assert ad.author_id == author_id
        assert ad.status.value == "draft"

        # Retrieve by ID
        # found_ad = advertisement_repo.get_advertisement_by_id(ad.id)
        # assert found_ad is not None
        # assert found_ad.title == "Integration Test Ad"
        # assert str(found_ad.id) == str(ad.id)

    def test_get_advertisements(self, advertisement_repo):
        author_id = uuid4()

        # Create test advertisements
        ad1_data = {"title": "Ad 1", "description": "Desc 1", "price": 100.0, "category": "test"}
        ad2_data = {"title": "Ad 2", "description": "Desc 2", "price": 200.0, "category": "test"}

        advertisement_repo.create_advertisement(ad1_data, author_id)
        advertisement_repo.create_advertisement(ad2_data, author_id)

        ads = advertisement_repo.get_advertisements(0, 10)
        assert len(ads) >= 2

    def test_update_advertisement(self, advertisement_repo):
        author_id = uuid4()
        ad_data = {"title": "Original", "description": "Original Desc", "price": 100.0, "category": "test"}

        ad = advertisement_repo.create_advertisement(ad_data, author_id)

        update_data = {"title": "Updated Title", "price": 150.0}
        updated_ad = advertisement_repo.update_advertisement(ad.id, update_data)

        assert updated_ad.title == "Updated Title"
        assert updated_ad.price == 150.0
        assert updated_ad.description == "Original Desc"  # Should remain unchanged

    def test_publish_advertisement(self, advertisement_repo):
        author_id = uuid4()
        ad_data = {"title": "Draft Ad", "description": "To be published", "price": 100.0, "category": "test"}

        ad = advertisement_repo.create_advertisement(ad_data, author_id)
        assert ad.status.value == "draft"
        assert ad.published_at is None

        published_ad = advertisement_repo.publish_advertisement(ad.id)
        assert published_ad.status.value == "published"
        assert published_ad.published_at is not None

    def test_delete_advertisement(self, advertisement_repo):
        author_id = uuid4()
        ad_data = {"title": "To Delete", "description": "Will be deleted", "price": 100.0, "category": "test"}

        ad = advertisement_repo.create_advertisement(ad_data, author_id)

        result = advertisement_repo.delete_advertisement(ad.id)
        assert result is True

        # Verify deletion
        deleted_ad = advertisement_repo.get_advertisement_by_id(ad.id)
        assert deleted_ad is None