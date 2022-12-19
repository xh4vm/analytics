#!/bin/bash 

uvicorn src.main:app --host 0.0.0.0 --port $PROJECT_FEEDBACKS_API_PORT --reload
# gunicorn src.main:app -k uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:$PROJECT_FEEDBACKS_API_PORT