import pytest
import os
import sys

# Добавляем корневую директорию проекта в Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

# Используем SQLite для тестов вместо PostgreSQL
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def engine():
    # Используем SQLite для тестов
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

    # Создаем таблицы
    Base.metadata.create_all(bind=engine)

    yield engine

    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=engine)
    # УБРАТЬ удаление файла - он может быть заблокирован
    # if os.path.exists("test.db"):
    #     os.remove("test.db")


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(session):
    from app.main import app
    #

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()