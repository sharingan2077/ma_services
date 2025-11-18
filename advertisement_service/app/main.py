from fastapi import FastAPI
from app.endpoints.advertisement_router import advertisement_router
from app.database import engine, Base
import app.schemas.advertisement
from app.settings import settings

print(f"Database URL: {settings.postgres_url}")

# Просто создаем таблицы
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")

app = FastAPI(title="Advertisement Service", version="1.0.0")
app.include_router(advertisement_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Advertisement Service is running"}