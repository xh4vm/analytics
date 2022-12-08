# Проектная работа 9 спринта

Задания на спринт вы найдёте внутри тем.

## Запуск сервиса аналитики
```
# Установка файлов переменных окружения
cp .env.example .env 

# Подготовка файлов-логов nginx
rm -rf ./backend/nginx/static && cp -r ./backend/nginx/static_defaults/ ./backend/nginx/static

# Запуск проекта
make analytics
```

## Управление проектом 
Осуществлялось в [notion](https://obtainable-stinger-44c.notion.site/1fb8cf0aecb348b5b56f03c59865be3a?v=605f36748e354f83b93182ffccffff16)
