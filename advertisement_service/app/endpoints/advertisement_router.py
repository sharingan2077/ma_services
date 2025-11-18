from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.advertisement_service import AdvertisementService
from app.repositories.advertisement_repo import AdvertisementRepository
from app.models.advertisement import Advertisement, AdvertisementCreate, AdvertisementUpdate
from app.database import get_db
from sqlalchemy.orm import Session
import traceback

advertisement_router = APIRouter(prefix="/advertisements", tags=["Advertisements"])

def get_advertisement_service(db: Session = Depends(get_db)) -> AdvertisementService:
    repo = AdvertisementRepository(db)
    return AdvertisementService(repo)

# Заглушка для авторизации
def get_current_user() -> UUID:
    return UUID("12345678-1234-1234-1234-123456789abc")

@advertisement_router.get("/", response_model=list[Advertisement])
def get_advertisements(
    skip: int = 0,
    limit: int = 100,
    service: AdvertisementService = Depends(get_advertisement_service)
):
    try:
        return service.get_advertisements(skip, limit)
    except Exception as e:
        print(f"Error in get_advertisements: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@advertisement_router.get("/{ad_id}", response_model=Advertisement)
def get_advertisement(
    ad_id: UUID,
    service: AdvertisementService = Depends(get_advertisement_service)
):
    try:
        ad = service.get_advertisement(ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Advertisement not found")
        return ad
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_advertisement: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@advertisement_router.post("/", response_model=Advertisement, status_code=status.HTTP_201_CREATED)
def create_advertisement(
    ad_data: AdvertisementCreate,
    service: AdvertisementService = Depends(get_advertisement_service),
    user_id: UUID = Depends(get_current_user)
):
    try:
        return service.create_advertisement(ad_data, user_id)
    except Exception as e:
        print(f"Error in create_advertisement: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@advertisement_router.put("/{ad_id}", response_model=Advertisement)
def update_advertisement(
    ad_id: UUID,
    ad_data: AdvertisementUpdate,
    service: AdvertisementService = Depends(get_advertisement_service),
    user_id: UUID = Depends(get_current_user)
):
    try:
        ad = service.update_advertisement(ad_id, ad_data, user_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Advertisement not found or access denied")
        return ad
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update_advertisement: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@advertisement_router.post("/{ad_id}/publish", response_model=Advertisement)
def publish_advertisement(
    ad_id: UUID,
    service: AdvertisementService = Depends(get_advertisement_service),
    user_id: UUID = Depends(get_current_user)
):
    try:
        ad = service.publish_advertisement(ad_id, user_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Advertisement not found or access denied")
        return ad
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in publish_advertisement: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@advertisement_router.delete("/{ad_id}")
def delete_advertisement(
    ad_id: UUID,
    service: AdvertisementService = Depends(get_advertisement_service),
    user_id: UUID = Depends(get_current_user)
):
    try:
        success = service.delete_advertisement(ad_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Advertisement not found or access denied")
        return {"message": "Advertisement deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_advertisement: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")