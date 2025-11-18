#!/bin/bash

# Запуск тестовой базы данных
docker-compose -f docker-compose.test.yml up -d

# Ждем пока база данных будет готова
sleep 5

# Запуск тестов
echo "Running unit tests..."
pytest tests/unit/ -v

echo "Running integration tests..."
pytest tests/integration/ -v

# Останавливаем тестовую базу данных
docker-compose -f docker-compose.test.yml down