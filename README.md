# Django DRF Project

## Запуск проекта через Docker Compose

### Требования
- Docker
- Docker Compose

### Команда для запуска проекта
```bash

# Создать .env файл
cp .env.example .env

# Запустить проект
docker-compose up -d --build
```
## Проверить работоспособность

### Проверка web

1. Открыть в браузере
http://localhost:8000

2. Проверить логи
```bash
docker-compose logs web
```

### Проверка PostgreSQL

1. Подключиться к БД


2. Посмотреть таблицы (в psql)
```bash
\dt
```

3. Выйти
```bash
\q
```

### Проверка Redis

1. Проверить соединение
```bash
docker-compose exec redis redis-cli ping
```
Должен ответить: PONG

### Проверка Celery Worker

1. Проверить логи
```bash
docker-compose logs celery_worker
```
2. Проверить статус
```bash
docker-compose ps | grep celery_worker
```

### Проверка Celery Beat

1. Проверить логи
```bash
docker-compose logs celery_beat
```

2. Проверить статус
```bash
docker-compose ps | grep celery_beat
```

### Проверить статус всех контейнеров
```bash
docker-compose ps
```

### Проверить логи всех сервисов
```bash
docker-compose logs -f
```

### Проверить использование ресурсов
```bash
docker stats
```

## Остановка проекта
```bash
docker-compose down -v
```