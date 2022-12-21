#!/bin/bash 

# [dev-mode] Не получилось добиться автообновления проекта через использование gunicorn при изменении проекта
# uvicorn src.main:app --host 0.0.0.0 --port $PROJECT_FEEDBACKS_API_PORT --reload
# [prod-mode]
gunicorn src.main:app -k uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:$PROJECT_FEEDBACKS_API_PORT