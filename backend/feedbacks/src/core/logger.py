LOG_DEFAULT_HANDLERS = ['info_rotating_file_handler', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'info': {
            'format': '%(asctime)s [%(levelname)s] LOGGER: "%(name)s" MODULE: "%(module)s" MESSAGE: "%(message)s"'
        },
        'error': {
            'format': '%(asctime)s [%(levelname)s] LOGGER: "%(name)s" PID: "%(process)d" MODULE: "%(module)s" LINE: %(lineno)s MESSAGE: "%(message)s"'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'info',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'info',
            'filename': '/var/log/feedbacks/info.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': '/var/log/feedbacks/error.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['info_rotating_file_handler', 'error_file_handler', ],
            'level': 'INFO',
        },
        'uvicorn.error': {
            'handlers': ['console', 'error_file_handler', ],
            'level': 'ERROR',
        }
    },
    'root': {
        'level': 'INFO',
        'formatter': 'info',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
