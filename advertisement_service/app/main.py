from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator  # ДОБАВИТЬ
from app.endpoints.advertisement_router import advertisement_router
from app.database import engine, Base
import app.schemas.advertisement
from app.settings import settings

print(f"Database URL: {settings.postgres_url}")

# Ждем пока БД будет готова с повторными попытками
max_retries = 10
retry_delay = 3

for i in range(max_retries):
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        break
    except OperationalError as e:
        if i < max_retries - 1:
            print(f"Database not ready, retrying in {retry_delay} seconds... (attempt {i+1}/{max_retries})")
            time.sleep(retry_delay)
        else:
            print(f"Failed to create tables after {max_retries} attempts: {e}")
            # Не падаем, возможно БД будет позже


app = FastAPI(title="Advertisement Service", version="1.0.0")
app.include_router(advertisement_router, prefix="/api")

# НАСТРОЙКА МЕТРИК PROMETHEUS
instrumentator = Instrumentator().instrument(app)

@app.on_event("startup")
async def startup():
    instrumentator.expose(app)

@app.get("/")
def read_root():
    return {"message": "Advertisement Service is running"}

# Эндпоинт для проверки здоровья (для мониторинга)
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "advertisement_service"}