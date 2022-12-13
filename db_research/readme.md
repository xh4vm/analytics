# Выбор хранилища

В качестве хранилища для работы с лайками, рецензиями на фильмы и пользовательскими закладками было выбрано MongoDB.
Выбор был сделан исходя из следующий предпосылок.
1. Сущности рассматриваемой задачи имеют слабую связанность, работа с ними не требует построения сложных многоуровневых запросов к БД. Информация в сущностях удобно ложиться в JSON формат. Плюсом является простора добавления дополнительных полей в сущности. 
3. Сценарии задачи предполагают возможность подокументарного добавления, изменения и удаления записей в сущности. Выполнение высокоселективных запросов.
4. Для функционала задачи достаточно атомарного выполнения операций над документом.
5. Выбранная БД должна быть легко масштабирована и обеспечивать высокую отказоустойчивость.

## Схемы хранения данных

### Лайки пользователей. Коллекция likes.

      "$jsonSchema": {
        "bsonType": "object",
        "required": [ "user_id", "film_id", "rating", "created", "modified"
        ],
        "properties": {
          "user_id": {
            "bsonType": "string",
            "description": "User's UUID"
          },
          "film_id": {
            "bsonType": "string",
            "description": "Film's id"
          },
          "rating": {
            "bsonType": "int",
            "description": "Rating"
          },
          "created": {
            "bsonType": "date",
            "description": "Date of creation of the like"
          },
          "modified": {
            "bsonType": "date",
            "description": "Date of modification of the like"
          }
        }
      }

### Рецензии на фильмы. Коллекция reviews.

      "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "film_id", "text", "created", "modified"],
        "properties": {
          "user_id": {
            "bsonType": "string",
            "description": "User's UUID"
          },
          "film_id": {
            "bsonType": "string",
            "description": "Film's id"
          },
          "text": {
            "bsonType": "string",
            "description": "Text of review"
          },
          "created": {
            "bsonType": "date",
            "description": "Date of creation of the review"
          },
          "modified": {
            "bsonType": "date",
            "description": "Date of modification of the review"
          }
        }
      }

### Лайки на рецензии. Коллекция reviews_likes.

      "$jsonSchema": {
        "bsonType": "object",
        "required": ["review_id", "user_id", "rating", "created", "modified"],
        "properties": {
          "review_id": {
            "bsonType": "objectId",
            "description": "Review's UUID"
          },
          "user_id": {
            "bsonType": "string",
            "description": "User's id"
          },
          "rating": {
            "bsonType": "int",
            "description": "Rating of review"
          },
          "created": {
            "bsonType": "date",
            "description": "Date of creation of the review's like"
          },
          "modified": {
            "bsonType": "date",
            "description": "Date of modification of the review's like"
          }
        }
      }

### Пользовательские закладки. Коллекция bookmarks.

      "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "film_id", "created", "modified"],
        "properties": {
          "user_id": {
            "bsonType": "string",
            "description": "User's UUID"
          },
          "film_id": {
            "bsonType": "string",
            "description": "Film's id"
          },
          "created": {
            "bsonType": "date",
            "description": "Date of creation of the bookmark"
          },
          "modified": {
            "bsonType": "date",
            "description": "Date of modification of the bookmark"
          }
        }
      }

# Результаты тестирования скорости работы с хранилищем.

## Загрузка данных большого объёма.

| Размер dataset | Время          | Скорость з/с (с/з) | Время с индексом | Скорость с индексом з/с (с/з)  |
|----------------|----------------|--------------------|------------------|--------------------------------|
| 10k            | 0:00:10.193963 | 989 (0.001)        | 0:00:10.508541   | 952 (0.001)                    |
| 100k           | 0:01:41.030872 | 990 (0.001)        | 0:01:47.841425   | 927 (0.001)                    |
| 500k           | 0:08:35.905586 | 969 (0.001)        | 0:08:55.323631   | 934 (0.001)                    |
| 1m             | 0:17:41.582151 | 942 (0.001)        | 0:17:59.092349   | 927 (0,001)                    |


## Тестирование работы скорости операций над данными предусмотренных сценариями задачи

| Основные операции по сценариям                                        | Время выполнения |
|-----------------------------------------------------------------------|------------------|
| movies.likes.insert(one like)                                         | 0:00:00.004298   |
| movies.likes.find_filter(particular document: user_id, film_id)       | 0:00:00.002747   |
| movies.likes.find_filter(user's likes in a day)                       | 0:00:00.193883   |
| movies.reviews.insert(one review)                                     | 0:00:00.003987   |
| movies.reviews.find_filter(particular reviews: user_id, film_id)      | 0:00:00.002952   |
| movies.reviews.find_filter(all film's reviews)                        | 0:00:00.012972   |
| movies.reviews_likes.insert(one review's like)                        | 0:00:00.002760   |
| movies.bookmarks.insert(one review's like)                            | 0:00:00.003247   |
| movies.bookmarks.find_filter(particular bookmark: user_id, film_id)   | 0:00:00.001891   |
| movies.bookmarks.find_filter(all user's bookmarks)                    | 0:00:00.002011   |
| movies.likes.aggregate(average film's rating)                         | 0:00:00.663060   |
| movies.likes.update(particular document: user_id, film_id set rating) | 0:00:00.001763   |
| movies.likes.delete(particular document: _id)                         | 0:00:00.001846   |



| Поступление данных в реальном времени          | Результат | Время запуска команды       | Время выполнения | Дельта времени |
|------------------------------------------------|-----------|-----------------------------|------------------|----------------|
| movies.likes.count(film's like before insert)  | 19        | 2022-12-12 23:59:55.511903  |  0:00:00.001020  | -              |
| movies.likes.insert(one like)                  | 1         | 2022-12-12 23:59:55.513099  |  0:00:00.002571  | -              |
| movies.likes.count(film's like after insert)   | 20        | 2022-12-12 23:59:55.515952  |  0:00:00.001308  | 0,00159        |   


# Запуск окружения и скриптов исследования
## Поднять кластер mongodb
1. Запустить контейнеры: </br>
```make mongo```
2. Настроить кластер: </br>
```make mongo_cfg```
## Создать коллекции
1. Переименовать файл .env.example в .env
2. Активировать виртуальное окружение:
```make build_venv```
3. Создать коллекции:
```make create_coll_i:```
4. Загрузить данные:
```make load_data```
5. Записать полученные временные показания времени загрузки данных
6. Запустить замеры при работе с данными:
```make test_data```
7. Записать полученные данные