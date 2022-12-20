# Проектная работа 9 спринта

Задания на спринт вы найдёте внутри тем.

[Ссылка на работу](https://github.com/xh4vm/analytics)

## Запуск сервиса аналитики
```
# Установка файлов переменных окружения
cp .env.example .env 

# Подготовка файлов-логов nginx
rm -rf ./nginx/static && cp -r ./nginx/static_defaults/ ./nginx/static

# Подготовка файлов-логов es-initer
rm -rf ./log_hub/es_initer/static && cp -r ./log_hub/es_initer/static_defaults/ ./log_hub/es_initer/static

# Подготовка файлов-логов feedbacks
mkdir -p ./backend/feedbacks/static && touch ./backend/feedbacks/static/info.log && touch ./backend/feedbacks/static/error.log

# Запуск проекта
make analytics
```

## Управление проектом 
Осуществлялось в [notion](https://obtainable-stinger-44c.notion.site/1fb8cf0aecb348b5b56f03c59865be3a?v=605f36748e354f83b93182ffccffff16)
